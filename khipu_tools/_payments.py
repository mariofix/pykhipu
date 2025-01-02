from decimal import Decimal
from typing import ClassVar, Optional, TypeVar

from typing import Literal
from typing_extensions import Unpack

from khipu_tools._api_resource import APIResource
from khipu_tools._khipu_object import KhipuObject
from khipu_tools._request_options import RequestOptions

T = TypeVar("T", bound=KhipuObject)


class Payments(APIResource[T]):
    OBJECT_NAME: ClassVar[Literal["Payment"]] = "payments"
    OBJECT_PREFIX: ClassVar[Literal["v3"]] = "v3"

    class PaymentParams(RequestOptions):
        """
        Parametros de creacion de pago
        """

        amount: str
        """ El monto del cobro. Sin separador de miles y usando '.' como separador de decimales. Hasta 4 lugares decimales, dependiendo de la moneda. """
        currency: Literal["CLP", "CLF", "ARS", "PEN", "MXN", "USD", "EUR", "BOB", "COP"]
        """El código de moneda en formato ISO-4217."""
        subject: str
        """Motivo."""
        transaction_id: Optional[str]
        """Identificador propio de la transacción. Ej: número de factura u orden de compra."""
        custom: Optional[str]
        """Parámetro para enviar información personalizada de la transacción. Ej: documento XML con el detalle del carro de compra."""
        body: Optional[str]
        """Descripción del cobro."""
        bank_id: Optional[str]
        """Identificador del banco para usar en el pago."""
        return_url: Optional[str]
        """La dirección URL a donde enviar al cliente mientras el pago está siendo verificado."""
        cancel_url: Optional[str]
        """La dirección URL a donde enviar al cliente si decide no hacer hacer la transacción."""
        picture_url: Optional[str]
        """Una dirección URL de una foto de tu producto o servicio."""
        notify_url: Optional[str]
        """La dirección del web-service que utilizará khipu para notificar cuando el pago esté conciliado."""
        contract_url: Optional[str]
        """La dirección URL del archivo PDF con el contrato a firmar mediante este pago. El cobrador debe estar habilitado para este servicio y el campo fixed_payer_personal_identifier es obligatorio."""
        notify_api_version: Literal["3.0"]
        """Versión de la API de notificaciones para recibir avisos por web-service. Solo está soportada la version 3.0. para versiones anteriores pyeden usar la libreria pykhipu"""
        expires_date: Optional[str]
        """Fecha máxima para ejecutar el pago (en formato ISO-8601). El cliente podrá realizar varios intentos de pago hasta dicha fecha. Cada intento tiene un plazo individual de 3 horas para su ejecución."""
        send_email: Optional[bool]
        """Si es True, se enviará una solicitud de cobro al correo especificado en payer_email."""
        payer_name: Optional[str]
        """Nombre del pagador. Es obligatorio cuando send_email es true."""
        payer_email: Optional[str]
        """Correo del pagador. Es obligatorio cuando send_email es true."""
        send_reminders: Optional[bool]
        """Si es true, se enviarán recordatorios de cobro."""
        responsible_user_email: Optional[str]
        """Correo electrónico del responsable de este cobro, debe corresponder a un usuario Khipu con permisos para cobrar usando esta cuenta de cobro."""
        fixed_payer_personal_identifier: Optional[str]
        """Identificador personal. Si se especifica, solo podrá ser pagado usando ese identificador."""
        integrator_fee: Optional[str]
        """Comisión para el integrador. Sólo es válido si la cuenta de cobro tiene una cuenta de integrador asociada."""
        collect_account_uuid: Optional[str]
        """Para cuentas de cobro con más cuenta propia. Permite elegir la cuenta donde debe ocurrir la transferencia."""
        confirm_timeout_date: Optional[str]
        """Fecha de rendición del cobro. Es también la fecha final para poder reembolsar el cobro. Formato ISO-8601."""
        mandatory_payment_method: Optional[str]
        """El cobro sólo se podrá pagar utilizando el medio de pago especificado. Los posibles valores para este campo se encuentran en el campo id de la respuesta del endpoint /api/3.0/merchants/paymentMethods."""
        psp_client_merchant_name: Optional[str]
        """Nombre del comercio final para quien un proveedor de servicios de pago procesa un pago. Requerido para transacciones de clientes PSP; no aplicable para otros."""

    class PaymentCreateResponse(KhipuObject):
        payment_id: str
        """Identificador único del pago, es una cadena alfanumérica de 12 caracteres. Como este identificador es único, se puede usar, por ejemplo, para evitar procesar una notificación repetida. (Khipu espera un código 200 al notificar un pago, si esto no ocurre se reintenta hasta por dos días)."""
        payment_url: str
        """URL principal del pago, si el usuario no ha elegido previamente un método de pago se le muestran las opciones."""
        simplified_transfer_url: str
        """URL de pago simplificado."""
        transfer_url: str
        """URL de pago normal."""
        app_url: str
        """URL para invocar el pago desde un dispositivo móvil usando la APP de Khipu."""
        ready_for_terminal: bool
        """Es true si el pago ya cuenta con todos los datos necesarios para abrir directamente la aplicación de pagos Khipu."""

    class PaymentInfo(RequestOptions):
        payment_id: str
        """Identificador del pago"""

    class PaymentRefundResponse(KhipuObject):
        message: str
        """Mensaje a desplegar al usuario."""

    payment_id: str
    """Identificador único del pago, es una cadena alfanumérica de 12 caracteres. Como este identificador es único, se puede usar, por ejemplo, para evitar procesar una notificación repetida. (Khipu espera un código 200 al notificar un pago, si esto no ocurre se reintenta hasta por dos días)."""
    payment_url: str
    """URL principal del pago, si el usuario no ha elegido previamente un método de pago se le muestran las opciones."""
    simplified_transfer_url: str
    """URL de pago simplificado."""
    transfer_url: str
    """URL de pago normal."""
    app_url: str
    """URL para invocar el pago desde un dispositivo móvil usando la APP de Khipu."""
    ready_for_terminal: bool
    """Es true si el pago ya cuenta con todos los datos necesarios para abrir directamente la aplicación de pagos Khipu."""
    notification_token: str
    """Cadena de caracteres alfanuméricos que identifican unicamente al pago, es el identificador que el servidor de Khipu enviará al servidor del comercio cuando notifique que un pago está conciliado."""
    receiver_id: int
    """Identificador único de una cuenta de cobro."""
    conciliation_date: str
    """Fecha y hora de conciliación del pago. Formato ISO-8601."""
    subject: str
    """Motivo del pago."""
    amount: Decimal
    """El monto del cobro."""
    currency: str
    """El código de moneda en formato ISO-4217."""
    status: Literal["pending", "verifying", "done"]
    """Estado del pago, puede ser pending (el pagador aún no comienza a pagar), verifying (se está verificando el pago) o done, cuando el pago ya está confirmado."""
    status_detail: Literal[
        "pending",
        "normal",
        "marked-paid-by-receiver",
        "rejected-by-payer",
        "marked-as-abuse",
        "reversed",
    ]
    """Detalle del estado del pago: pending (el pagador aún no comienza a pagar), normal (el pago fue verificado y fue cancelado por algún medio de pago estándar), marked-paid-by-receiver (el cobrador marcó el cobro como pagado por otro medio), rejected-by-payer (el pagador declaró que no pagará), marked-as-abuse (el pagador declaró que no pagará y que el cobro fue no solicitado), y reversed (el pago fue anulado por el comercio, el dinero fue devuelto al pagador)."""
    body: str
    """Detalle del cobro."""
    picture_url: str
    """URL con imagen del cobro."""
    receipt_url: str
    """URL del comprobante de pago."""
    return_url: str
    """URL donde se redirige al pagador luego que termina el pago."""
    cancel_url: str
    """URL donde se redirige al pagador luego de que desiste hacer el pago."""
    notify_url: str
    """URL del webservice donde se notificará el pago."""
    notify_api_version: Literal["3,0"]
    """Versión de la API de notificación."""
    expires_date: str
    """Fecha máxima para ejecutar el pago (en formato ISO-8601). El cliente podrá realizar varios intentos de pago hasta dicha fecha. Cada intento tiene un plazo individual de 3 horas para su ejecución."""
    attachment_urls: list[str]
    """Arreglo de URLs de archivos adjuntos al pago."""
    bank: str
    """Nombre del banco seleccionado por el pagador."""
    bank_id: str
    """Identificador del banco seleccionado por el pagador."""
    payer_name: str
    """Nombre del pagador."""
    payer_email: str
    """Correo electrónico del pagador."""
    personal_identifier: str
    """Identificador personal del pagador."""
    bank_account_number: str
    """Número de cuenta bancaria del pagador."""
    out_of_date_conciliation: bool
    """Es true si la conciliación del pago fue hecha luego de la fecha de expiración."""
    transaction_id: str
    """Identificador del pago asignado por el cobrador."""
    custom: str
    """Campo genérico que asigna el cobrador al momento de hacer el pago."""
    responsible_user_email: str
    """Correo electrónico de la persona responsable del pago."""
    send_reminders: bool
    """Es true cuando este es un cobro por correo electrónico y Khipu enviará recordatorios."""
    send_email: bool
    """Es true cuando Khipu enviará el cobro por correo electrónico."""
    payment_method: Literal["regular_transfer", "simplified_transfer", "not_available"]
    """Método de pago usado por el pagador, puede ser regular_transfer (transferencia normal) o simplified_transfer (transferencia simplificada)."""
    funds_source: Literal["debit", "prepaid", "credit", "not-available", ""]
    """Origen de fondos usado por el pagador, puede ser debit para pago con débito, prepaid para pago con prepago, credit para pago con crédito, o vacío en el caso de que se haya pagado mediante transferencia bancaria."""
    discount: int
    """Monto a descontar del valor pagado."""
    third_party_authorization_details: str
    """Ignorar este campo."""

    @classmethod
    def create(cls, **params: Unpack["Payments.PaymentParams"]) -> KhipuObject["Payments.PaymentCreateResponse"]:
        """
        Crea un pago en Khipu y obtiene las URLs para redirección al usuario para que complete el pago.
        """
        result = cls._static_request(
            "post",
            cls.class_url(),
            params=params,
        )
        if not isinstance(result, KhipuObject):
            raise TypeError("Expected KhipuObject object from API, got %s" % (type(result).__name__))

        return result

    @classmethod
    def get(cls, **params: Unpack["Payments.PaymentInfo"]) -> KhipuObject["Payments"]:
        """
        Información completa del pago. Datos con los que fue creado y el estado actual del pago.
        """
        result = cls._static_request(
            "get",
            f"{cls.class_url()}/{params['payment_id']}",
        )
        if not isinstance(result, KhipuObject):
            raise TypeError("Expected KhipuObject object from API, got %s" % (type(result).__name__))

        return result

    @classmethod
    def delete(cls, **params: Unpack["Payments.PaymentInfo"]) -> bool:
        """
        Borrar un pago. Solo se pueden borrar pagos que estén pendientes de pagar. Esta operación no puede deshacerse.
        """
        result = cls._static_request(
            "delete",
            f"{cls.class_url()}/{params['payment_id']}",
        )

        return result

    @classmethod
    def refund(cls, **params: Unpack["Payments.PaymentInfo"]) -> KhipuObject["Payments.PaymentRefundResponse"]:
        """
        Reembolsa total o parcialmente el monto de un pago. Esta operación solo se puede realizar en los comercios que
        recauden en cuenta Khipu y antes de la rendición de los fondos correspondientes.
        """
        result = cls._static_request(
            "post",
            f"{cls.class_url()}/{params['payment_id']}/refunds",
            params=params,
        )
        if not isinstance(result, KhipuObject):
            raise TypeError("Expected KhipuObject object from API, got %s" % (type(result).__name__))

        return result
