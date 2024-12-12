# API de django-payments-chile

Este documento proporciona una visión general de los diferentes proveedores de pago disponibles en django-payments-chile. Cada proveedor tiene su propia implementación y configuración específica.

Para obtener detalles sobre cada proveedor, consulte los siguientes enlaces:

- [FlowProvider](flow-provider.md)
- [KhipuProvider](khipu-provider.md)
- [KlapProvider](klap-provider.md)
- [KushkiProvider](kushki-provider.md)
- [OneclickProvider](oneclick-provider.md)
- [PagofacilProvider](pagofacil-provider.md)
- [PaykuProvider](payku-provider.md)
- [WebpayProvider](webpay-provider.md)

Cada enlace lo llevará a una documentación detallada sobre la implementación y uso de ese proveedor específico.

## FlowProvider

El FlowProvider es una implementación para integrar la pasarela de pagos Flow en django-payments-chile.

### Métodos principales

- `__init__(self, **kwargs)`: Inicializa el proveedor con las configuraciones necesarias.
- `get_form(self, payment, data=None)`: Retorna el formulario para iniciar el proceso de pago.
- `process_data(self, payment, request)`: Procesa los datos recibidos de Flow después de un pago.

#### Configuración

Para utilizar FlowProvider, añada la siguiente configuración a `PAYMENT_VARIANTS` en su archivo `settings.py`:

```python
PAYMENT_VARIANTS = {
    "flow": ("django_payments_chile.FlowProvider", {
        "api_key": "su_api_key",
        "api_secret": "su_api_secret",
        "api_endpoint": "sandbox",  # Cambie a "live" para producción
        "api_medio": 9,  # 9 indica todos los medios de pago
    })
}
```

#### Uso

Para crear un pago utilizando FlowProvider:

```python
from django_payments import get_payment_model

Payment = get_payment_model()
payment = Payment.objects.create(
    variant='flow',  # Debe coincidir con la clave en PAYMENT_VARIANTS
    amount=1000,
    currency='CLP',
    description='Descripción del pago'
)
```

Consulte la [documentación de Flow](https://www.flow.cl/docs) para más detalles sobre la integración y opciones disponibles.

## API

::: django_payments_chile.FlowProvider
