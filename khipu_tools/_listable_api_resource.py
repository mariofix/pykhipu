from typing import TypeVar

from khipu_tools._api_resource import APIResource
from khipu_tools._khipu_object import KhipuObject
from khipu_tools._list_object import ListObject

T = TypeVar("T", bound=KhipuObject)

# TODO(major): 1704 - remove this class and all internal usages. `.list` is already inlined into the resource classes.
# Although we should inline .auto_paging_iter into the resource classes as well.


class ListableAPIResource(APIResource[T]):
    @classmethod
    def auto_paging_iter(cls, **params):
        return cls.list(**params).auto_paging_iter()

    @classmethod
    def list(cls, **params) -> ListObject[T]:
        result = cls._static_request(
            "get",
            cls.class_url(),
            params=params,
        )

        if not isinstance(result, ListObject):
            raise TypeError(f"Expected list object from API, got {type(result).__name__}")

        return result
