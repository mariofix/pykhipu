from typing import ClassVar, TypeVar

from typing_extensions import Literal

from khipu_tools._khipu_object import KhipuObject
from khipu_tools._api_resource import APIResource

T = TypeVar("T", bound=KhipuObject)


class BankItem:
    bank_id: str
    name: str
    message: str
    min_amount: int
    type: Literal["Persona", "Empresa"]
    parent: str
    logo_url: str


class Banks(APIResource[T]):
    OBJECT_NAME: ClassVar[Literal["banks"]] = "banks"
    OBJECT_PREFIX: ClassVar[Literal["v3"]] = "v3"

    banks: list[BankItem]

    @classmethod
    def get(cls) -> KhipuObject["Banks"]:
        """
        Este método obtiene la lista de bancos que se pueden utilizar para pagar en esta cuenta de cobro.
        """
        result = cls._static_request(
            "get",
            cls.class_url(),
        )
        if not isinstance(result, KhipuObject):
            raise TypeError(
                "Expected KhipuObject object from API, got %s" % (type(result).__name__)
            )

        return result
