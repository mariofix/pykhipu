# Khipu Tools

:warning: :warning: Proyecto en desarrollo activo :warning: :warning:

Un cliente de Python simple y eficiente para conectarse con los servicios de Khipu, facilitando transacciones e integraciones financieras.

## Características

- Conexión directa con la API de Khipu (soporte para API v3 en adelante)
- Soporte para pagos instantáneos (gracias a [fixmycode/pykhipu](https://github.com/fixmycode/pykhipu))
- Soporte para pagos automáticos
- Implementación ligera y fácil de usar
- Manejo de errores y excepciones

## Requisitos Previos

- Python 3.9+
- Credenciales de Khipu

## Uso Básico

```python
from khipu_tools import KhipuClient

# Inicializar cliente
client = KhipuClient(api_key, secret)

# Crear un cobro
payment = client.create_payment(
    amount=1000,
    subject="Servicio de ejemplo"
)
```

## Licencia

MIT License
