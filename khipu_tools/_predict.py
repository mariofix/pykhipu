from typing import ClassVar, TypeVar, Literal

from typing_extensions import Unpack


from khipu_tools._api_resource import APIResource
from khipu_tools._khipu_object import KhipuObject
from khipu_tools._request_options import RequestOptions

T = TypeVar("T", bound=KhipuObject)


class Predict(APIResource[T]):
    OBJECT_NAME: ClassVar[Literal["predict"]] = "predict"
    OBJECT_PREFIX: ClassVar[Literal["v3"]] = "v3"

    class PredictParams(RequestOptions):
        payer_email: str
        """Correo electrónico del pagador"""
        bank_id: str
        """Identificador del banco de origen"""
        amount: str
        """Monto del pago"""
        currency: str
        """Moneda en formato ISO-4217"""

    result: Literal[
        "ok",
        "new_destinatary_amount_exceeded",
        "max_amount_exceeded",
        "new_destinatary_cool_down",
        "not_available_account",
    ]
    """El resultado de la predicción."""
    max_amount: int
    """El monto máximo posible para transferir."""
    cool_down_date: str
    """Fecha de término para la restricción de monto en formato ISO-8601"""
    new_destinatary_max_amount: str
    """Monto máximo para transferir a un nuevo destinatario."""

    @classmethod
    def get(cls, **params: Unpack["Predict.PredictParams"]) -> KhipuObject["Predict"]:
        """
        Predicción acerca del resultado de un pago, si podrá o no funcionar.
        Información adicional como máximo posible de transferir a un nuevo destinatario.
        """
        result = cls._static_request(
            "get",
            cls.class_url(),
            params=params,
        )
        if not isinstance(result, KhipuObject):
            raise TypeError("Expected KhipuObject object from API, got %s" % (type(result).__name__))

        return result
