import time
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import json
import os

LOG_FILE = "sat_logs.json"


def log(event, data):
    """Agrega un evento al log JSON."""
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        except:
            logs = []

    logs.append({
        "evento": event,
        "data": data,
        "timestamp": time.time()
    })

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)


class Module:
    def __init__(self, name, fn, interval=1, timeout=2):
        self.name = name
        self.fn = fn
        self.interval = interval
        self.timeout = timeout
        self.enabled = True
        self.next_run = datetime.now()

    def schedule_next(self):
        self.next_run = datetime.now() + timedelta(seconds=self.interval)


class Bus:
    def __init__(self, max_workers=5):
        self.modules = {}
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.running = False

    def register(self, module: Module):
        self.modules[module.name] = module
        log("module_registered", {
            "module": module.name,
            "interval": module.interval,
            "timeout": module.timeout
        })
        print(f"[BUS] Registered module: {module.name}")

    def unregister(self, name):
        if name in self.modules:
            del self.modules[name]
            log("module_unregistered", {"module": name})

    def run_once(self, module: Module):
        """Ejecuta módulo con timeout."""
        future = self.executor.submit(module.fn)

        try:
            result = future.result(timeout=module.timeout)
            log("module_result", {"module": module.name, "result": result})
            return result

        except TimeoutError:
            try:
                future.cancel()
            except:
                pass
            log("module_timeout", {"module": module.name})
            print(f"[BUS] Timeout: {module.name}")
            return None

        except Exception as e:
            print(f"[BUS] Error running {module.name}: {e}")
            log("module_error", {"module": module.name, "error": str(e)})
            return None

    def start(self):
        print("[BUS] Starting main loop.")
        self.running = True

        try:
            while self.running:
                now = datetime.now()

                for m in list(self.modules.values()):
                    if m.enabled and now >= m.next_run:
                        print(f"[BUS] Running {m.name} ...")
                        self.run_once(m)
                        m.schedule_next()

                time.sleep(0.2)

        except KeyboardInterrupt:
            print("[BUS] KeyboardInterrupt: stopping")

        finally:
            self.shutdown()

    def shutdown(self):
        print("[BUS] Shutting down executor …")
        self.running = False
        try:
            self.executor.shutdown(wait=False)
        except Exception as e:
            print("[BUS] shutdown error:", e)

        log("bus_stopped", {})
