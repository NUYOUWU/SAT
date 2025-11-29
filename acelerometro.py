import json
import subprocess
import time

def leer_acelerometro():
    try:
        salida = subprocess.check_output(
            ["termux-sensor", "-s", "ACCELEROMETER", "-n", "1"],
            stderr=subprocess.STDOUT
        ).decode("utf-8")

        datos = json.loads(salida)

        if "ACCELEROMETER" not in datos:
            return None

        valores = datos["ACCELEROMETER"]["values"]

        if len(valores) != 3:
            return None

        x, y, z = valores

        # Magnitud total del vector √(x² + y² + z²)
        total = (x**2 + y**2 + z**2) ** 0.5

        return total, (x, y, z)

    except Exception:
        return None


def ciclo_acelerometro():
    print("\n⟲ Ciclo acelerómetro iniciado...")

    while True:
        lectura = leer_acelerometro()

        if lectura is None:
            print("… sin lectura")
        else:
            total, (x, y, z) = lectura
            print(f"Total: {total:.2f}  |  X:{x:.2f} Y:{y:.2f} Z:{z:.2f}")

        time.sleep(0.4)
