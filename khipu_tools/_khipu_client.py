from typing import Any, Dict, Optional, Union

from khipu_tools import DEFAULT_API_BASE
from khipu_tools._api_mode import ApiMode
from khipu_tools._api_requestor import _APIRequestor
from khipu_tools._client_options import _ClientOptions
from khipu_tools._error import AuthenticationError
from khipu_tools._http_client import (
    HTTPClient,
    new_default_http_client,
    new_http_client_async_fallback,
)
from khipu_tools._khipu_object import KhipuObject
from khipu_tools._khipu_response import KhipuResponse
from khipu_tools._request_options import extract_options_from_dict
from khipu_tools._requestor_options import BaseAddresses, RequestorOptions
from khipu_tools._util import _convert_to_khipu_object, get_api_mode


class KhipuClient:
    def __init__(
        self,
        api_key: str,
        *,
        base_addresses: BaseAddresses = {},
        http_client: Optional[HTTPClient] = None,
    ):
        # The types forbid this, but let's give users without types a friendly error.
        if api_key is None:  # pyright: ignore[reportUnnecessaryComparison]
            raise AuthenticationError("No API key provided.")

        base_addresses = {
            "api": DEFAULT_API_BASE,
            **base_addresses,
        }

        requestor_options = RequestorOptions(
            api_key=api_key,
            base_addresses=base_addresses,
        )

        if http_client is None:
            http_client = new_default_http_client(
                async_fallback_client=new_http_client_async_fallback(),
            )

        self._requestor = _APIRequestor(
            options=requestor_options,
            client=http_client,
        )

        self._options = _ClientOptions()

    def construct_event(
        self,
        payload: Union[bytes, str],
        sig_header: str,
        secret: str,
        tolerance: int = 30,
    ) -> "Event":

        return True

    def raw_request(self, method_: str, url_: str, **params):
        params = params.copy()
        options, params = extract_options_from_dict(params)
        api_mode = get_api_mode(url_)
        base_address = params.pop("api")

        rbody, rcode, rheaders = self._requestor.request_raw(
            method_,
            url_,
            params=params,
            options=options,
            base_address=base_address,
            api_mode=api_mode,
            usage=["raw_request"],
        )

        return self._requestor._interpret_response(rbody, rcode, rheaders, api_mode)

    def deserialize(
        self,
        resp: Union[KhipuResponse, dict[str, Any]],
        params: Optional[dict[str, Any]] = None,
        *,
        api_mode: ApiMode,
    ) -> KhipuObject:
        return _convert_to_khipu_object(
            resp=resp,
            params=params,
            requestor=self._requestor,
            api_mode=api_mode,
        )
