# Pagos Automáticos

Es muy sencillo habilitar el proceso de Pago Automático a tus clientes, sólo necesitas utilizar la API de Suscripción para solicitar un nuevo ID de Suscripción, para asociarlo al servicio que vas a cobrar a tu cliente de forma recurrente. Cuando el cliente finalice el proceso de firma en su banco, recibirá una notificación en la URL de devolución de llamada que proporcionó al solicitar el ID de suscripción.

Tras una confirmación positiva, puede empezar a utilizar la API de cobro para enviar sus solicitudes de pago automático. La parte restante del proceso es asíncrona y se le notificará cuando finalice el proceso de conciliación.

## Crear Subscripción

```py
import khipu_tools

khipu_tools.api_key = "khipu-apiv3-key
khipu_tools.AutomaticPayments.create(
    name="Service XYZ Id 11.222.333-0",
    email="personal.email@gmail.com",
    max_amount=1000,
    currency="CLP",
    notify_url="https://my-domain.biz/subscription-notify-api",
    return_url="https://my-domain.biz/subscription-result",
    cancel_url="https://my-domain.biz/subscription-cancel"
)
```

```json
{
  "subscription_id": "13a0f1aa-5e47-4894-aa8b-282dd19593ec",
  "redirect_url": "https://khipu.com/pac-manager/13a0f1aa-5e47-4894-aa8b-282dd19593ec"
}
```

## Obtener información de una subscripción

```py
import khipu_tools

khipu_tools.api_key = "khipu-apiv3-key
khipu_tools.AutomaticPayments.get(payment_id="13a0f1aa-5e47-4894-aa8b-282dd19593ec")
```

Respuesta

```json
{
  "subscription_id": "13a0f1aa-5e47-4894-aa8b-282dd19593ec",
  "status": "SIGNED",
  "developer": false,
  "customer_bank_code": "8",
  "service_reference": "My Merchant name"
}
```
