# sat_system.py
from bus import Bus, Module
import adapters
import time
import json
from datetime import datetime

class SATSystem:
    def __init__(self):
        self.bus = Bus(max_workers=5)
        self.setup_modules()
        
    def setup_modules(self):
        """Configura todos los módulos con timeout de 20 segundos"""
        
        # Módulo de Batería - cada 5 minutos
        battery_module = Module(
            name="battery_monitor",
            fn=self.battery_check,
            interval=300,  # 5 minutos
            timeout=20
        )
        
        # Módulo de Proximidad - cada 3 segundos
        proximity_module = Module(
            name="proximity_sensor", 
            fn=self.proximity_check,
            interval=3,
            timeout=20
        )
        
        # Módulo de Acelerómetro - cada 2 segundos
        accelerometer_module = Module(
            name="accelerometer_sensor",
            fn=self.accelerometer_check,
            interval=2,
            timeout=20
        )
        
        # Módulo de Salud del Sistema - cada 30 segundos
        health_module = Module(
            name="system_health",
            fn=self.system_health_check,
            interval=30,
            timeout=20
        )
        
        # Registrar todos los módulos
        self.bus.register(battery_module)
        self.bus.register(proximity_module)
        self.bus.register(accelerometer_module)
        self.bus.register(health_module)
        
    def battery_check(self):
        """Verifica el estado de la batería"""
        try:
            result = adapters.battery_read_once()
            
            # Verificar si es batería baja
            if result.get("ok") and result.get("percentage", 100) < 25:
                self.send_alert("battery_low", f"Batería al {result['percentage']}%")
                
            return {
                "type": "battery",
                "data": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "type": "battery_error", 
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def proximity_check(self):
        """Verifica el sensor de proximidad"""
        try:
            result = adapters.prox_read_once()
            
            # Si hay objeto cercano (valor 0)
            if result.get("ok") and result.get("estado") == 0:
                self.send_alert("proximity_detected", "Objeto detectado cerca")
                
            return {
                "type": "proximity",
                "data": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "type": "proximity_error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def accelerometer_check(self):
        """Verifica el acelerómetro para detectar movimiento"""
        try:
            result = adapters.accel_read_once()
            
            # Detectar movimiento brusco (total > 15)
            if result.get("ok") and result.get("total", 0) > 15:
                self.send_alert("high_movement", f"Movimiento detectado: {result['total']:.2f}")
                
            return {
                "type": "accelerometer", 
                "data": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "type": "accelerometer_error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def system_health_check(self):
        """Verifica el estado general del sistema"""
        try:
            # Simular una verificación de salud
            health_data = {
                "status": "healthy",
                "modules_running": len(self.bus.modules),
                "timestamp": datetime.now().isoformat()
            }
            
            return {
                "type": "system_health",
                "data": health_data
            }
            
        except Exception as e:
            return {
                "type": "health_check_error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def send_alert(self, alert_type, message):
        """Envía alertas/notificaciones"""
        print(f"🚨 ALERTA [{alert_type}]: {message}")
        
        # Aquí podrías agregar:
        # - Notificación con termux-notification
        # - Envío por Telegram
        # - Log en archivo especial de alertas
        
        try:
            import os
            os.system(f'termux-notification --title "SAT Alert" --content "{message}"')
        except:
            pass  # Si falla, solo imprimimos en consola
    
    def start_system(self):
        """Inicia todo el sistema SAT"""
        print("=" * 50)
        print("🚀 INICIANDO SISTEMA SAT MEJORADO")
        print("⏰ Timeout configurado: 20 segundos por módulo")
        print("📊 Módulos activos:")
        for name, module in self.bus.modules.items():
            print(f"   • {name} (cada {module.interval}s)")
        print("=" * 50)
        
        try:
            self.bus.start()
        except KeyboardInterrupt:
            print("\n🛑 Sistema detenido por el usuario")
        except Exception as e:
            print(f"\n❌ Error en el sistema: {e}")
        finally:
            print("👋 Sistema SAT finalizado")

# Función de prueba para módulo lento (simula timeout)
def slow_module_test():
    """Módulo de prueba que se demora 25 segundos (excede timeout)"""
    print("[TEST] Iniciando módulo lento (25 segundos)...")
    time.sleep(25)
    return {"message": "Este mensaje nunca debería llegar"}

def main():
    """Función principal"""
    
    # Opción: agregar módulo de prueba lento
    import sys
    if "--test-timeout" in sys.argv:
        system = SATSystem()
        
        # Agregar módulo de prueba que excede timeout
        slow_module = Module(
            name="slow_test_module",
            fn=slow_module_test,
            interval=30,
            timeout=20
        )
        system.bus.register(slow_module)
        print("🧪 Módulo de prueba de timeout agregado")
        
        system.start_system()
    
    else:
        # Ejecución normal
        system = SATSystem()
        system.start_system()

if __name__ == "__main__":
    main()
