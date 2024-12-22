# Pagos Instantáneos

La API de Khipu para crear y recibir pagos permite a cobradores (individuos u organizaciones), que tengan una cuenta de cobro activa en Khipu, generar cobros.

El proceso de creación, pago y validación es el siguiente:

* El cobrador genera un cobro usando la API y despliega un botón para la compra.
* El pagador pincha el botón de pago en el sitio web, o un enlace de pago en un correo electrónico u otro medio y paga utilizando Khipu.
* El pagador es redireccionado a la página de retorno definida por el cobrador donde se debe indicar que el pago está en verificación (o a la página de fracaso en el caso que no se haya podido hacer el pago).
* Unos momentos después Khipu verifica la transacción y notifica al pagador por correo electrónico. Además, se notifica al comercio por correo electrónico y/o por la invocación de un web service.
* El cobrador valida la notificación de pago y entrega el bien transado al pagador (o descarta la notificación si es inválida)

## Obtener Bancos

```py
import khipu_tools

khipu_tools.api_key = "khipu-apiv3-key
khipu_tools.Banks.get()
```

Este método obtiene el listado de bancos asociado a la cuenta.

```json
{
  "banks": [
    {
      "bank_id": "Bawdf",
      "logo_url": "https://s3.amazonaws.com/static.khipu.com/logos/bancos/chile/demobank-icon.png",
      "message": "Este es un banco de pruebas. Las transacciones no son reales.",
      "min_amount": "200.0000",
      "name": "DemoBank",
      "parent": "",
      "type": "Persona"
    }
  ]
}
```

## Crear Pago

Crea un pago en Khipu y obtiene las URLs para redirección al usuario para que complete el pago.

```py
import khipu_tools

khipu_tools.api_key = "khipu-apiv3-key
khipu_tools.Payments.create(amount=10000, currency="CLP", subject="Pago de prueba")
```

El listado completo de variables se encuentra descrita en la [api de khipu](https://docs.khipu.com/openapi/es/v1/instant-payment/openapi/operation/postPayment/)

Respuesta

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

## Obtener información de un Pago

Información completa del pago. Datos con los que fue creado y el estado actual del pago.

```py
import khipu_tools

khipu_tools.api_key = "khipu-apiv3-key
khipu_tools.Payments.get(payment_id="gqzdy6chjne9")
```

Respuesta

```json
{
  "payment_id": "gqzdy6chjne9",
  "payment_url": "https://khipu.com/payment/info/gqzdy6chjne9",
  "simplified_transfer_url": "https://app.khipu.com/payment/simplified/gqzdy6chjne9",
  "transfer_url": "https://khipu.com/payment/manual/gqzdy6chjne9",
  "app_url": "khipu:///pos/gqzdy6chjne9",
  "ready_for_terminal": false,
  "notification_token": "9dec8aa176c5223026919b3b5579a4776923e646ff3be686b9e6b62ec042e91f",
  "receiver_id": 985101,
  "conciliation_date": "2017-03-01T13:00:00.000Z",
  "subject": "Test",
  "amount": 1000,
  "currency": "CLP",
  "status": "done",
  "status_detail": "normal",
  "body": "Test",
  "picture_url": "https://micomercio.com/picture_url",
  "receipt_url": "https://micomercio.com/order/receipt_url",
  "return_url": "https://micomercio.com/order/return_url",
  "cancel_url": "https://micomercio.com/order/cancel_url",
  "notify_url": "https://micomercio.com/webhook/notify_url",
  "notify_api_version": "3.0",
  "expires_date": "2023-12-31T15:45:00-04:00",
  "attachment_urls": [
    "https://micomercio.com/attachment1.pdf"
  ],
  "bank": "Banco de Chile (Edwards Citi)",
  "bank_id": "dfFbF",
  "payer_name": "Nombre Pagador",
  "payer_email": "pagador@email.com",
  "personal_identifier": "11.000.111-9",
  "bank_account_number": "001120490689",
  "out_of_date_conciliation": true,
  "transaction_id": "zwo3wqz6uulcvajt",
  "custom": "<xml>...</xml>",
  "responsible_user_email": "responsible@email.com",
  "send_reminders": true,
  "send_email": true,
  "payment_method": "simplified_transfer",
  "funds_source": "debit",
  "discount": 0,
  "third_party_authorization_details": "string"
}
```

## Eliminar Pago

Borrar un pago. Solo se pueden borrar pagos que estén pendientes de pagar. Esta operación no puede deshacerse.

```py
import khipu_tools

khipu_tools.api_key = "khipu-apiv3-key
khipu_tools.Payments.delete(payment_id="gqzdy6chjne9")
```

Respuesta

```json
{
  "message": "Message"
}
```

## Predecir Pago

Predicción acerca del resultado de un pago, si podrá o no funcionar. Información adicional como máximo posible de transferir a un nuevo destinatario.

```py
import khipu_tools

khipu_tools.api_key = "khipu-apiv3-key
khipu_tools.Predict.get(
    payer_email="pagador@email.com",
    amount="5000000",
    currency="CLP",
    bank_id="Bawdf",
)
```

Respuesta

```json
{
  "result": "ok",
  "max_amount": 5000000,
  "cool_down_date": "2024-06-21T11:23:09.123Z",
  "new_destinatary_max_amount": 100000
}
```

## Medios de Pago

Obtiene el listado de medios de pago disponible para una cuenta de cobrador.

```py
import khipu_tools

khipu_tools.api_key = "khipu-apiv3-key
khipu_tools.Payments.methods(cuenta_cobro="12345")
```

Respuesta

```json
{
  "paymentMethods": [
    {
      "id": "simplified_transfer",
      "name": "simplified_transfer",
      "logo_url": "https://s3.amazonaws.com/static.khipu.com/buttons/2015/150x50-transparent.png"
    }
  ]
}
```
