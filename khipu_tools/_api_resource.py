from collections.abc import Mapping
from typing import Any, ClassVar, Generic, Optional, TypeVar

from khipu_tools._api_requestor import _APIRequestor
from khipu_tools._base_address import BaseAddress
from khipu_tools._khipu_object import KhipuObject
from khipu_tools._request_options import extract_options_from_dict

T = TypeVar("T", bound=KhipuObject)


class APIResource(KhipuObject, Generic[T]):
    OBJECT_NAME: ClassVar[str]
    OBJECT_PREFIX: ClassVar[str]

    @classmethod
    def class_url(cls) -> str:
        if cls == APIResource:
            raise NotImplementedError(
                "APIResource is an abstract class.  You should perform "
                "actions on its subclasses (e.g. Payment, Predict, etc)"
            )
        # Namespaces are separated in object names with periods (.) and in URLs
        # with forward slashes (/), so replace the former with the latter.
        base = cls.OBJECT_NAME.replace(".", "/")
        return f"/{cls.OBJECT_PREFIX}/{base}"

    @classmethod
    def _static_request(
        cls,
        method_,
        url_,
        params: Optional[Mapping[str, Any]] = None,
        *,
        base_address: BaseAddress = "api",
    ):
        request_options, request_params = extract_options_from_dict(params)
        return _APIRequestor._global_instance().request(
            method_,
            url_,
            params=request_params,
            options=request_options,
            base_address=base_address,
        )
