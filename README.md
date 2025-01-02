# Khipu Tools

## Proyecto en Desarrollo

Este proyecto está en desarrollo activo. Las funcionalidades y API pueden cambiar sin previo aviso.

## Descripción

Khipu Tools es una librería en Python pensada para que integrar los servicios de Khipu en tus proyectos sea sencillo y directo. Ideal para gestionar transacciones y pagos desde tu código.

## Características

- **Conexión directa con la API de Khipu**: Compatible con la versión 3 en adelante de la API.
- **Pagos instantáneos**: Basado en [fixmycode/pykhipu](https://github.com/fixmycode/pykhipu).
- **Pagos automáticos**: Simplifica transacciones recurrentes.
- **Diseño amigable**: Fácil de usar y ligero.
- **Manejo de errores**: Robusto y preparado para entornos reales.

## Instalación

Puedes instalar Khipu Tools desde PyPI:

```bash
pip install khipu-tools
```

## Requisitos Previos

- **Python 3.9 o superior**.
- **Credenciales de Khipu**: Necesitarás tu `API Key` proporcionada por Khipu.

## Uso Básico

Ejemplo de cómo crear un pago utilizando Khipu Tools:

```python
import khipu_tools

# Configura tu API Key de Khipu
khipu_tools.api_key = "tu-api-key"

# Crear un pago
pago = khipu_tools.Payments.create(
    amount=5000,
    currency="CLP",
    subject="Pago de Prueba"
)

print(pago)
```

Salida esperada:

```json
{
  "payment_id": "gqzdy6chjne9",
  "payment_url": "https://khipu.com/payment/info/gqzdy6chjne9",
  "simplified_transfer_url": "https://app.khipu.com/payment/simplified/gqzdy6chjne9",
  "transfer_url": "https://khipu.com/payment/manual/gqzdy6chjne9",
  "app_url": "khipu:///pos/gqzdy6chjne9",
  "ready_for_terminal": false
}
```

## Documentación Completa

Próximamente se incluirá una documentación más extensa sobre todas las funcionalidades disponibles.

## Contribuciones

¡Las contribuciones son bienvenidas! Por favor, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama con un nombre descriptivo para tu cambio.
3. Envía un Pull Request describiendo los cambios.

## Licencia

Este proyecto está licenciado bajo la [MIT License](LICENSE).

---

Este proyecto no está patrocinado ni asociado con Khipu.
