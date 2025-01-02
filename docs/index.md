# Documentación de Khipu Tools

Khipu Tools es una librería en Python pensada para facilitar la integración con los servicios de Khipu. Este proyecto ofrece funcionalidades clave para manejar transacciones financieras, enfocándose en simplicidad, eficiencia y robustez.

![PyPI - Status](https://img.shields.io/pypi/status/khipu-tools)
[![Downloads](https://pepy.tech/badge/khipu-tools)](https://pepy.tech/project/khipu-tools)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/fde07768d1714b0b93c6addd5e13bb7f)](https://app.codacy.com/gh/mariofix/khipu-tools/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/fde07768d1714b0b93c6addd5e13bb7f)](https://app.codacy.com/gh/mariofix/khipu-tools/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/mariofix/khipu-tools/main.svg)](https://results.pre-commit.ci/latest/github/mariofix/khipu-tools/main)
[![Tests & Coverage](https://github.com/mariofix/khipu-tools/actions/workflows/tests_coverage.yml/badge.svg?branch=main)](https://github.com/mariofix/khipu-tools/actions/workflows/tests_coverage.yml)
![PyPI](https://img.shields.io/pypi/v/khipu-tools)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/khipu-tools)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/khipu-tools)
![PyPI - License](https://img.shields.io/pypi/l/khipu-tools)

## Características Destacadas

### Pagos Instantáneos

Los pagos instantáneos son una de las funcionalidades principales de Khipu Tools. Esta funcionalidad permite generar y gestionar pagos al instante con un diseño que optimiza la simplicidad y velocidad.

**Ejemplo de código:**

```python
import khipu_tools

khipu_tools.api_key = "tu-api-key"

pago = khipu_tools.Payments.create(
    amount=5000,
    currency="CLP",
    subject="Pago de Prueba"
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
    pago = khipu_tools.Payments.create(
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
