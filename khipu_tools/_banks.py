from typing import ClassVar, TypeVar

from typing import Literal

from khipu_tools._khipu_object import KhipuObject
from khipu_tools._api_resource import APIResource

T = TypeVar("T", bound=KhipuObject)


class BankItem:
    """
    Informacion de banco
    """

    bank_id: str
    """Identificador del banco."""
    name: str
    """Nombre del banco."""
    message: str
    """Mensaje con particularidades del banco."""
    min_amount: int
    """Monto mínimo que acepta el banco en un pago"""
    type: Literal["Persona", "Empresa"]
    """Tipo de banco."""
    parent: str
    """Identificador del banco padre (si un banco tiene banca personas y empresas, el primero será el padre del segundo)."""
    logo_url: str
    """URL del logo del banco."""


class Banks(APIResource[T]):
    OBJECT_NAME: ClassVar[Literal["banks"]] = "banks"
    OBJECT_PREFIX: ClassVar[Literal["v3"]] = "v3"

    banks: list[BankItem]
    """Listado con Bancos registrados"""

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
            raise TypeError("Expected KhipuObject object from API, got %s" % (type(result).__name__))

        return result
