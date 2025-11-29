from bus import Bus, Module
import time
import random

def test_mod1():
    print("[MOD1] Ejecutando...")
    return {"valor": random.randint(1, 100)}

def test_mod2():
    print("[MOD2] Ejecutando...")
    time.sleep(0.5)
    return "ok"

def test_lento():
    print("[LENTO] Esto debería dar timeout...")
    time.sleep(5)     # excede timeout
    return "nunca llega"

bus = Bus(max_workers=3)

bus.register(Module("rapido", test_mod1, interval=1, timeout=1))
bus.register(Module("medio", test_mod2, interval=2, timeout=1))
bus.register(Module("lento", test_lento, interval=3, timeout=1))

bus.start()
