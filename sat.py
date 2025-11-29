import os, json, datetime




LOG = "sat_logs.json"

def log(event, data=""):
    entrada = {
        "timestamp": str(datetime.datetime.now()),
        "event": event,
        "data": data
    }

    if not os.path.exists(LOG):
        with open(LOG, "w") as f:
            json.dump([entrada], f, indent=4)
    else:
        with open(LOG, "r") as f:
            logs = json.load(f)
        logs.append(entrada)
        with open(LOG, "w") as f:
            json.dump(logs, f, indent=4)

def leer_bateria():
    salida = os.popen("termux-battery-status").read()
    return json.loads(salida)

def accion_notificacion(mensaje):
    os.system(f'termux-notification --title "SAT" --content "{mensaje}"')

def main():
    bateria = leer_bateria()
    nivel = bateria["percentage"]

    log("lectura_bateria", {"nivel": nivel})

    if nivel < 25:
        accion_notificacion(f"Batería baja ({nivel}%). Modo ahorro recomendado.")
        log("accion", "notificacion_bateria_baja")

        try:
            ciclo_proximidad()
        except Exception as e:
            log("error_ciclo_proximidad", {"error": str(e)})

if __name__ == "__main__":
    main()
