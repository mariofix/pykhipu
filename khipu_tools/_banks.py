from typing import ClassVar

from typing_extensions import Literal, Unpack

from khipu_tools._khipu_object import KhipuObject
from khipu_tools._list_object import ListObject
from khipu_tools._listable_api_resource import ListableAPIResource


class BankItem:
    bank_id: str
    name: str
    message: str
    min_amount: int
    type: Literal["Persona", "Empresa"]
    parent: str
    logo_url: str


class Banks(ListableAPIResource["Banks"]):
    OBJECT_NAME: ClassVar[Literal["banks"]] = "banks"

    banks: list[BankItem]

    @classmethod
    def getBanks(cls, params=None) -> KhipuObject["Banks"]:
        """
        Este método obtiene la lista de bancos que se pueden utilizar para pagar en esta cuenta de cobro.
        """
        result = cls._static_request(
            "get",
            cls.class_url(),
        )
        if not isinstance(result, KhipuObject):
            raise TypeError(
                "Expected BankObject object from API, got %s" % (type(result).__name__)
            )

        return result

    @classmethod
    def list(cls, **params: Unpack["Banks"]) -> ListObject["Banks"]:
        """
        Lists all Country Spec objects available in the API.
        """
        result = cls._static_request(
            "get",
            cls.class_url(),
            params=params,
        )
        if not isinstance(result, ListObject):
            raise TypeError(
                "Expected list object from API, got %s" % (type(result).__name__)
            )

        return result

    @classmethod
    async def list_async(cls, **params: Unpack["Banks"]) -> ListObject["Banks"]:
        """
        Lists all Country Spec objects available in the API.
        """
        result = await cls._static_request_async(
            "get",
            cls.class_url(),
            params=params,
        )
        if not isinstance(result, ListObject):
            raise TypeError(
                "Expected list object from API, got %s" % (type(result).__name__)
            )

        return result
