# Documentación de Khipu Tools

Khipu Tools es una librería en Python pensada para facilitar la integración con los servicios de Khipu. Este proyecto ofrece funcionalidades clave para manejar transacciones financieras, enfocándose en simplicidad, eficiencia y robustez.

![PyPI - Status](https://img.shields.io/pypi/status/django-payments-chile)
[![Downloads](https://pepy.tech/badge/django-payments-chile)](https://pepy.tech/project/django-payments-chile)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/fde07768d1714b0b93c6addd5e13bb7f)](https://app.codacy.com/gh/mariofix/django-payments-chile/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/fde07768d1714b0b93c6addd5e13bb7f)](https://app.codacy.com/gh/mariofix/django-payments-chile/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/mariofix/django-payments-chile/main.svg)](https://results.pre-commit.ci/latest/github/mariofix/django-payments-chile/main)
[![Tests & Coverage](https://github.com/mariofix/django-payments-chile/actions/workflows/tests_coverage.yml/badge.svg?branch=main)](https://github.com/mariofix/django-payments-chile/actions/workflows/tests_coverage.yml)
![PyPI](https://img.shields.io/pypi/v/django-payments-chile)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-payments-chile)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/django-payments-chile)
![PyPI - License](https://img.shields.io/pypi/l/django-payments-chile)

## Características Destacadas

### Pagos Instantáneos

Los pagos instantáneos son una de las funcionalidades principales de Khipu Tools. Esta funcionalidad permite generar y gestionar pagos al instante con un diseño que optimiza la simplicidad y velocidad.

#### Basado en pykhipu

Esta funcionalidad aprovecha las bases establecidas por [fixmycode/pykhipu](https://github.com/fixmycode/pykhipu), garantizando integración con la API de Khipu de manera confiable y eficiente.

**Ejemplo de código:**

```python
import khipu_tools

khipu_tools.api_key = "tu-api-key"

pago = khipu_tools.InstantPayments.create(
    amount=5000,
    currency="CLP",
    subject="Pago Instantáneo de Prueba"
)

print(pago)
```

Salida

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

### Pagos Automáticos

La funcionalidad de pagos automáticos está diseñada para simplificar las transacciones recurrentes o programadas, permitiendo automatizar procesos financieros sin complicaciones.

**Ejemplo de código:**

```python
import khipu_tools

khipu_tools.api_key = "tu-api-key"

pago_automatico = khipu_tools.AutomaticPayments.schedule(
    amount=10000,
    currency="CLP",
    subject="Pago Recurrente",
    recurrence="monthly"
)

print(pago_automatico)
```

### Manejo de Errores

El manejo de errores está implementado para garantizar la robustez del sistema, permitiendo identificar y gestionar problemas de manera efectiva.

**Ejemplo de código con manejo de errores:**

```python
import khipu_tools

khipu_tools.api_key = "tu-api-key"

try:
    pago = khipu_tools.InstantPayments.create(
        amount=5000,
        currency="CLP",
        subject="Pago con Manejo de Errores"
    )
except Exception as e:
    print(f"Error al crear el pago: {e}")
else:
    print(pago)
{
  "payment_id": "gqzdy6chjne9",
  "payment_url": "https://khipu.com/payment/info/gqzdy6chjne9",
  "simplified_transfer_url": "https://app.khipu.com/payment/simplified/gqzdy6chjne9",
  "transfer_url": "https://khipu.com/payment/manual/gqzdy6chjne9",
  "app_url": "khipu:///pos/gqzdy6chjne9",
  "ready_for_terminal": false
}
```

## Licencia

Este proyecto esta licenciado bajo MIT. `khipu-tools` no está patrocinado ni asociado con Khipu.
