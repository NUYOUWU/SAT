from tamper_detection import TamperDetection
import time

detector = TamperDetection()

print("🛡️ Módulo Tamper Detection activo")

while True:
    if detector.check():
        print("⚠️ ALERTA: Manipulación detectada")
    time.sleep(0.5)
