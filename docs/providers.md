# Proveedores de Django-Payments-Chile

Django-Payments utiliza el concepto de proveedores y variantes para establecer conexiones con diferentes pasarelas de pago. Este documento describe la instalación y configuración de los proveedores disponibles en el proyecto django-payments-chile.

## Instalación general

Para instalar todos los proveedores, ejecuta:

```shell
pip install django-payments-chile[todos]
```

## Proveedores disponibles

### Flow

#### Instalación

Opción 1: Instalación específica

```shell
pip install django-payments-chile[flow]
```

Opción 2: Instalación manual

```shell
pip install pyflowcl
```

#### Configuración

No es necesario agregar el módulo en `INSTALLED_APPS`. Añade la siguiente configuración a `PAYMENT_VARIANTS` en tu archivo `settings.py`:

```python
PAYMENT_VARIANTS = {
    "flow": ("django_payments_chile.FlowProvider", {
        "api_key": "flow_key",
        "api_secret": "flow_secret",
        "api_endpoint": "sandbox",  # "live" o "sandbox"
        "api_medio": 9,  # 9 indica todos los medios de pago
    })
}
```

### Khipu

#### Instalación

Opción 1: Instalación específica

```shell
pip install django-payments-chile[khipu]
```

Opción 2: Instalación manual

```shell
pip install pykhipu
```

#### Configuración

No es necesario agregar el módulo en `INSTALLED_APPS`. Añade la siguiente configuración a `PAYMENT_VARIANTS` en tu archivo `settings.py`:

```python
PAYMENT_VARIANTS = {
    "khipu": ("django_payments_chile.KhipuProvider", {
        "receiver_id": 1,
        "secret": "qwertyasdf0123456789",
        "user_notification": "1.3",
        "bank_id": "qwe123"
    })
}
```

### Payku

#### Instalación

No se requiere instalación adicional.

#### Configuración

Añade la siguiente configuración a `PAYMENT_VARIANTS` en tu archivo `settings.py`:

```python
PAYMENT_VARIANTS = {
    "payku": ("django_payments_chile.PaykuProvider", {
        "token_publico": "token_publico",
        "token_privado": "token_privado",
        "site": "sandbox",  # "production" o "sandbox"
    })
}
```

## Notas adicionales

-   Asegúrate de reemplazar los valores de ejemplo (como "flow_key", "flow_secret", etc.) con tus credenciales reales proporcionadas por cada proveedor de pagos.
-   Para entornos de producción, cambia los valores de "api_endpoint" y "site" a "live" o "production" según corresponda.
-   Consulta la documentación oficial de cada proveedor para obtener información detallada sobre opciones de configuración adicionales y mejores prácticas de implementación.
