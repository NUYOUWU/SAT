# 🛡️ SAT – Sistema de Alerta Termux

SAT es un **framework experimental de seguridad y monitoreo basado en eventos**, diseñado para ejecutarse en entornos **Android + Termux**, incluso en dispositivos antiguos o con recursos limitados.

El proyecto prioriza **arquitectura simple, control local y observabilidad**, antes que dependencias pesadas o soluciones cerradas.

---

## 🎯 Objetivo

Construir una base modular que permita:
- Detectar eventos del entorno (sensores, estado del sistema)
- Centralizar la comunicación mediante un **bus de eventos**
- Registrar actividad en **logs estructurados**
- Servir como núcleo para futuros módulos de seguridad y alerta

---

## 🧩 Arquitectura (visión actual)

- **Bus de eventos**
  - Comunicación desacoplada entre módulos
- **Módulos de sensores**
  - Acelerómetro
  - Proximidad
- **Sistema de logs**
  - Registro persistente en formato JSON
- **Scripts de prueba**
  - Validación individual de módulos

La arquitectura está pensada para crecer sin romper compatibilidad.

---

## 📁 Estructura del proyecto

SAT/ ├── sat.py 
# Núcleo del sistema ├── bus.py
# Bus de eventos base ├── sat_bus.py
# Implementación del bus para SAT ├── adapters.py
# Adaptadores / abstracciones ├── acelerometro.py
# Módulo de acelerómetro ├── proximidad.py
# Módulo de proximidad ├── probar_acelerometro.py  
# Pruebas del acelerómetro ├── probar_proximidad.py
# Pruebas del sensor de proximidad ├── probar_bus.py
# Pruebas del bus de eventos ├── sat_logs.json           
# Logs estructurados └── README.md


---

## ⚙️ Requisitos

- Android
- Termux
- Python 3.x
- (Opcional) Termux:API para sensores

---

## 🚧 Estado del proyecto

🔧 **En desarrollo activo**

Este repositorio representa una **base funcional**, no un producto final.  
La prioridad actual es:
- Estabilidad del bus
- Claridad de los eventos
- Consolidación de módulos existentes

---

## 🧠 Filosofía

SAT no busca ser “completo” rápidamente.  
Busca ser **comprensible, extensible y controlable**.

Primero estructura.  
Luego complejidad.

---

## 📌 Autor

Proyecto desarrollado por **NUYO / NUYOUWU**  
Uso experimental y educativo.

---

## ⚠️ Nota

Este software se provee **sin garantías**.  
Úsalo bajo tu propia responsabilidad.
