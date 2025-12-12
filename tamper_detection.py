from acelerometro import leer_acelerometro
from proximidad import leer_proximidad
from sat_logs import log_event
import time


class TamperDetection:
    def __init__(self, threshold=2.5):
        self.threshold = threshold
        self.last_proximity = None

    def check(self):
        lectura_accel = leer_acelerometro()
        prox = leer_proximidad()

        if lectura_accel is None or prox is None:
            return False

        total, (x, y, z) = lectura_accel

        if self.last_proximity is None:
            self.last_proximity = prox
            return False

        if prox != self.last_proximity and total > self.threshold:
            log_event("tamper_alert", {
                "total": total,
                "x": x,
                "y": y,
                "z": z,
                "proximity": prox
            })
            return True

        self.last_proximity = prox
        return False
