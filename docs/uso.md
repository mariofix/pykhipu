# Introducción a `django-payments-chile`

`django-payments-chile` es una extensión para `django-payments`, una biblioteca que proporciona una interfaz universal para procesar pagos en aplicaciones Django. Este proyecto añade soporte específico para varios proveedores de pagos chilenos como Flow, Khipu, Webpay, y otros.

Al ser una extensión de `django-payments`, su objetivo es facilitar la integración de múltiples proveedores de pago sin necesidad de que desarrolles un sistema desde cero para cada uno.

!!! note "TL;DR"
    Si prefieres ver una implementación de ejemplo y comenzar rápidamente, puedes clonar el [Repositorio de ejemplo](https://github.com/mariofix/django-payments-chile/tree/main/ejemplo):

## Requisitos

Antes de empezar, asegúrate de tener lo siguiente:

- **Python** instalado en tu sistema.
- **Django** para gestionar la aplicación web.
- **django-payments** como el núcleo para gestionar los pagos.
- **django-payments-chile** para integrar proveedores de pago en Chile.

## Instalación

### Instalación con Poetry

1. Crea un nuevo proyecto y entorno virtual con Poetry:

    ```bash
    poetry new mi-tienda
    cd mi-tienda
    poetry env use python3.10  # Reemplaza con la versión de Python que prefieras
    ```

2. Instala Django, `django-payments` y `django-payments-chile`:

    ```bash
    poetry add django django-payments django-payments-chile
    poetry install
    ```

!!! note
    Al instalar `django-payments-chile`, sus dependencias, como `django-payments` y `django`, se instalarán automáticamente.

## Configuración del Proyecto

### Crear el Proyecto

Inicia un nuevo proyecto de Django y una aplicación para gestionar los pagos:

```bash
poetry run django-admin startproject tienda .
poetry run django-admin startapp pagos
```

### Modificar `settings.py`

Abre el archivo `settings.py` de tu proyecto y agrega las siguientes configuraciones de `django-payments`:

```python
INSTALLED_APPS = [
    # Otras aplicaciones de tu proyecto...
    "payments",  # Core de django-payments
    "pagos",  # Tu app personalizada para manejar pagos
]

# Configuración de django-payments
PAYMENT_HOST = 'mi-tienda.cl'  # Reemplaza con tu dominio
PAYMENT_USES_SSL = True  # Usa True si tienes HTTPS, False en caso contrario
PAYMENT_MODEL = 'pagos.modelos.Pago'  # Modelo personalizado para pagos

# Configuración para proveedores chilenos (ejemplo con Flow)
PAYMENT_VARIANTS = {
    "flow": ("django_payments_chile.FlowProvider", {
        "api_key": "tu_api_key_de_flow",
        "api_secret": "tu_api_secret_de_flow",
    })
}
```

!!! note
    Asegúrate de reemplazar `'mi-tienda.cl'`, `'tu_api_key_de_flow'` y `'tu_api_secret_de_flow'` con tus datos reales.

### Modificar `urls.py`

Incluye las rutas necesarias en el archivo `urls.py` de tu proyecto o aplicación:

```python
from django.urls import include, path

urlpatterns = [
    # Otras rutas...
    path('payments/', include('payments.urls')),
]
```

## Creación del Modelo de Pago

Crea el modelo de pago en el archivo `pagos/modelos.py`, que gestionará los pagos y las redirecciones según el éxito o fracaso de los mismos:

```python
from django.conf import settings
from payments.models import BasePayment

class Pago(BasePayment):
    def get_failure_url(self) -> str:
        # Redirige a esta URL si el pago falla
        return f"https://{settings.PAYMENT_HOST}/payments/{self.pk}/failure"

    def get_success_url(self) -> str:
        # Redirige a esta URL si el pago es exitoso
        return f"https://{settings.PAYMENT_HOST}/payments/{self.pk}/success"
```

## Implementación en las Vistas

Usa `django-payments` en tus vistas para procesar pagos con los distintos proveedores. Aquí tienes un ejemplo de cómo crear y procesar un pago:

```python
from django.shortcuts import redirect
from payments import get_payment_model

def crear_pago(request):
    Payment = get_payment_model()
    payment = Payment.objects.create(
        variant='flow',  # Debe coincidir con el nombre en PAYMENT_VARIANTS
        description="Pago por Orden #123",
        total=10000,  # Monto en centavos (100 pesos)
        currency='CLP',
        billing_first_name='Juan',
        billing_last_name='Pérez',
        billing_email='juan.perez@example.com',
    )
    # Redirige al usuario a la URL del proveedor de pagos
    return redirect(payment.get_process_url())
```

## Consejos Finales

- **Pruebas**: Asegúrate de probar la implementación en un entorno de desarrollo antes de desplegarla en producción.
- **Seguridad**: No subas tus claves de API o secretos a repositorios públicos. Utiliza archivos de entorno o servicios seguros para gestionarlos.
- **Documentación Adicional**: Consulta la documentación oficial de [django-payments](https://django-payments.readthedocs.io/) para conocer todas las opciones y configuraciones avanzadas.
- **Soporte**: Si tienes dudas o problemas [haz tu pregunta](https://github.com/mariofix/django-payments-chile/discussions).
