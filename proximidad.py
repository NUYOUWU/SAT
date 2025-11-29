import subprocess
import json
import time
import os
import traceback

LOG_FILE = "sat_logs.json"


def guardar_log(data):
    """Guarda eventos en un JSON creciente."""
    logs = []

    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        except:
            logs = []  # archivo corrupto → se reinicia

    logs.append(data)

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)


def registrar_error(tipo, detalle):
    """Guarda errores en el log."""
    guardar_log({
        "evento": "error",
        "tipo": tipo,
        "detalle": detalle,
        "timestamp": time.time()
    })


def leer_proximidad():
    """Lee el sensor de proximidad 1 sola vez."""
    try:
        salida = subprocess.check_output(
            ["termux-sensor", "-s", "proximity-tp", "-n", "1"],
            stderr=subprocess.STDOUT
        )

        datos = json.loads(salida.decode().strip())
        distancia = datos["proximity-tp"]["values"][0]

        return distancia

    except Exception as e:
        print(f"[ERROR] No se pudo leer el sensor: {e}")
        registrar_error("lectura_proximidad", str(e))
        return None


def ciclo_proximidad(duracion=10, intervalo=0.5):
    """
    Ejecuta el ciclo por 10 segundos. Guarda logs y alerta.
    Maneja Ctrl+C y errores inesperados.
    """
    print("⟲ Ciclo de proximidad iniciado (modo temporal)...")
    inicio = time.time()

    try:
        while time.time() - inicio < duracion:
            lectura = leer_proximidad()

            if lectura is not None:
                print(f"[ALERTA] Proximidad detectada: {lectura}")

                guardar_log({
                    "sensor": "proximidad",
                    "valor": lectura,
                    "timestamp": time.time()
                })

            time.sleep(intervalo)

        print("✔ Finalizado: Ciclo de proximidad detenido automáticamente.")

    except KeyboardInterrupt:
        # Control elegante del Ctrl + C
        print("\n⚠ La aplicación se ha detenido inesperadamente (Ctrl+C).")
        registrar_error("interrupcion_usuario", "Programa detenido por Ctrl+C")

    except Exception as e:
        # Errores inesperados
        print("\n❌ ERROR FATAL: La aplicación se cerró inesperadamente.")
        print("Detalle:", str(e))

        registrar_error("error_fatal", traceback.format_exc())
