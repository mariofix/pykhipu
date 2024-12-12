# django-payments-chile

`django-payments-chile` es una extensión para `django-payments`, una biblioteca que proporciona una interfaz universal para procesar pagos en aplicaciones Django. Este proyecto añade soporte específico para varios proveedores de pagos chilenos como Flow, Khipu, Webpay, y otros.

![PyPI - Status](https://img.shields.io/pypi/status/django-payments-flow)
[![Downloads](https://pepy.tech/badge/django-payments-flow)](https://pepy.tech/project/django-payments-flow)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/7dc3c8d6fe844fdaa1de0cb86c242934)](https://app.codacy.com/gh/mariofix/django-payments-flow/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/7dc3c8d6fe844fdaa1de0cb86c242934)](https://app.codacy.com/gh/mariofix/django-payments-flow/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/mariofix/django-payments-flow/main.svg)](https://results.pre-commit.ci/latest/github/mariofix/django-payments-flow/main)
![PyPI](https://img.shields.io/pypi/v/django-payments-flow)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-payments-flow)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/django-payments-flow)
![PyPI - License](https://img.shields.io/pypi/l/django-payments-flow)

## Características

- Soporte para múltiples proveedores de pago en un solo proyecto.
- API consistente para crear, procesar y verificar transacciones.
- Fácil configuración y personalización.
- Documentación clara para desarrolladores.
- Soporte para eventos de éxito, fallo, y reembolsos de pagos.

## Inicio rápido

### Instalación

```bash
pip install django-payments-chile[todos]
```

Adicionalmente puedes instalar los extras para cada integrador:

- **flow**: Instala extras para Flow.
- **khipu**: Instala extras para Khipu.
- **todos**: Instala todos los extras.

### Configuración

En tu archivo `settings.py`, configura los proveedores de pago que vas a utilizar:

```python
PAYMENT_VARIANTS = {
    'flow': ('payments_chile.flow.FlowProvider', {
        'api_key': 'tu_api_key_flow',
        'secret': 'tu_secret_flow',
    }),
    'webpay': ('payments_chile.webpay.WebpayProvider', {
        'commerce_code': 'tu_commerce_code_webpay',
        'api_key': 'tu_api_key_webpay',
    }),
    # Otros proveedores como khipu, klap, etc.
}
```

### Creación de un nuevo pago

Con django-payments ya configurado, puedes crear un nuevo pago utilizando los métodos nativos de la librería:

```python
from payments import get_payment_model

Payment = get_payment_model()

payment = Payment.objects.create(
    variant='flow',  # o 'webpay', 'khipu', debe coincidir con el indice en PAYMENT_VARIANTS
    description="Pago por Orden #123",
    total=10000,
    currency='CLP',
    billing_first_name='Juan',
    billing_last_name='Pérez',
    billing_email='juan.perez@example.com',
)

# Redirige al usuario al proveedor de pagos
redirect_url = payment.get_process_url()
return redirect(redirect_url)
```

Para más detalles sobre el flujo de pago y las respuestas de los proveedores, consulta la sección [configuración](configuration.md).

## Proveedores soportados

- Flow
- Khipu
- Klap
- Kushki
- Payku
- Webpay
- Onepay

Consulta la documentación para aprender cómo integrarlos.
