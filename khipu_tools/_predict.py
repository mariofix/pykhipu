from typing import ClassVar, TypeVar

from typing_extensions import Literal, Unpack

from khipu_tools._api_resource import APIResource
from khipu_tools._khipu_object import KhipuObject
from khipu_tools._request_options import RequestOptions

T = TypeVar("T", bound=KhipuObject)


class Predict(APIResource[T]):
    OBJECT_NAME: ClassVar[Literal["predict"]] = "predict"
    OBJECT_PREFIX: ClassVar[Literal["v3"]] = "v3"

    class PredictParams(RequestOptions):
        payer_email: str
        bank_id: str
        amount: str
        currency: str

    result: str
    max_amount: int
    cool_down_date: str
    new_destinatary_max_amount: str

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
            raise TypeError(
                "Expected SripeObject object from API, got %s" % (type(result).__name__)
            )

        return result
