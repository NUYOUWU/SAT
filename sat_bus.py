# sat_bus.py
from bus import Bus, Module, log
import adapters

def build_and_run():
    b = Bus(max_workers=5)

    # Módulos: name, fn, interval(s), timeout(s)
    battery_mod = Module("battery", adapters.battery_read_once, interval=300, timeout=5)
    proxim_mod = Module("proximity", adapters.prox_read_once, interval=2, timeout=2)
    accel_mod = Module("accelerometer", adapters.accel_read_once, interval=1, timeout=2)

    b.register(battery_mod)
    b.register(proxim_mod)
    b.register(accel_mod)

    # ejemplo: desactivar proximidad temporalmente:
    # b.modules['proximity'].enabled = False

    b.start()

if __name__ == "__main__":
    build_and_run()
