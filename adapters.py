# adapters.py
# Estos adaptadores envuelven las funciones que tienes en proximidad.py y sat.py
# y normalizan la salida para que el Bus la registre.

import os
import json
import subprocess
import time

# IMPORTAR tus módulos si quieres usar funciones internas
# from proximidad import ciclo_proximidad  # NO llamar ciclo_proximidad si es loop infinito
# from sat import leer_bateria, accion_notificacion, log  # si los tienes

# En lugar de llamar a loops infinitos, adaptadores deben hacer UNA lectura y devolver resultado.

def prox_read_once():
    """
    Leer proximidad UNA vez. Debe devolver dict o None.
    Basado en la versión moderna de proximidad.py que devuelve lista/valor.
    """
    try:
        salida = subprocess.check_output(["termux-sensor", "-s", "proximity-tp", "-n", "1"], stderr=subprocess.STDOUT)
        datos = json.loads(salida.decode())
        valores = datos.get("proximity-tp", {}).get("values")
        if not valores:
            return {"ok": False, "reason": "no-values"}
        estado = valores[0]
        return {"ok": True, "estado": int(estado), "values": valores}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def battery_read_once():
    """
    Lee la batería UNA vez usando termux-battery-status
    """
    try:
        raw = os.popen("termux-battery-status").read()
        data = json.loads(raw)
        return {"ok": True, "percentage": data.get("percentage"), "status": data}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def accel_read_once():
    try:
        salida = subprocess.check_output(["termux-sensor", "-s", "ACCELEROMETER", "-n", "1"], stderr=subprocess.STDOUT)
        datos = json.loads(salida.decode())
        vals = datos.get("ACCELEROMETER", {}).get("values")
        if not vals or len(vals) < 3:
            return {"ok": False, "reason": "invalid-values"}
        x, y, z = vals[0], vals[1], vals[2]
        total = (x*x + y*y + z*z) ** 0.5
        return {"ok": True, "x": x, "y": y, "z": z, "total": total}
    except Exception as e:
        return {"ok": False, "error": str(e)}
