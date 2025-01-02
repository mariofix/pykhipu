import json
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, ClassVar, Optional, cast
from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit

from typing import Literal
from typing_extensions import Unpack

# breaking circular dependency
import khipu_tools
import khipu_tools._error as error
from khipu_tools._api_mode import ApiMode
from khipu_tools._base_address import BaseAddress
from khipu_tools._encode import _api_encode, _json_encode_date_callback
from khipu_tools._http_client import (
    HTTPClient,
    new_default_http_client,
    new_http_client_async_fallback,
)
from khipu_tools._khipu_response import KhipuResponse
from khipu_tools._request_options import RequestOptions, merge_options
from khipu_tools._requestor_options import RequestorOptions, _GlobalRequestorOptions
from khipu_tools._util import (
    _convert_to_khipu_object,
    get_api_mode,
    log_debug,
    log_info,
)

if TYPE_CHECKING:
    from khipu_tools._khipu_object import KhipuObject

HttpVerb = Literal["get", "post", "delete"]

# Lazily initialized
_default_proxy: Optional[str] = None


class _APIRequestor:
    _instance: ClassVar["_APIRequestor|None"] = None

    def __init__(
        self,
        options: Optional[RequestorOptions] = None,
        client: Optional[HTTPClient] = None,
    ):
        if options is None:
            options = RequestorOptions()
        self._options = options
        self._client = client

    def _get_http_client(self) -> HTTPClient:
        client = self._client
        if client is None:
            global _default_proxy

            if not khipu_tools.default_http_client:
                kwargs = {
                    "verify_ssl_certs": False,
                    "proxy": None,
                }
                khipu_tools.default_http_client = new_default_http_client(
                    async_fallback_client=new_http_client_async_fallback(**kwargs),
                    **kwargs,
                )
                _default_proxy = None
            elif None is not _default_proxy:
                import warnings

                warnings.warn(
                    "khipu_tools.proxy was updated after sending a "
                    "request - this is a no-op. To use a different proxy, "
                    "set khipu_tools.default_http_client to a new client "
                    "configured with the proxy."
                )

            assert khipu_tools.default_http_client is not None
            return khipu_tools.default_http_client
        return client

    def _replace_options(self, options: Optional[RequestOptions]) -> "_APIRequestor":
        options = options or {}
        new_options = self._options.to_dict()
        for key in [
            "api_key",
        ]:
            if key in options and options[key] is not None:
                new_options[key] = options[key]
        return _APIRequestor(options=RequestorOptions(**new_options), client=self._client)

    @property
    def api_key(self):
        return self._options.api_key

    @property
    def base_addresses(self):
        return self._options.base_addresses

    @classmethod
    def _global_instance(cls):
        if cls._instance is None:
            cls._instance = cls(options=_GlobalRequestorOptions(), client=None)
        return cls._instance

    @staticmethod
    def _global_with_options(
        **params: Unpack[RequestOptions],
    ) -> "_APIRequestor":
        return _APIRequestor._global_instance()._replace_options(params)

    @classmethod
    def _format_app_info(cls, info):
        str = info["name"]
        if info["version"]:
            str += "/{}".format(info["version"])
        if info["url"]:
            str += " ({})".format(info["url"])
        return str

    def request(
        self,
        method: str,
        url: str,
        params: Optional[Mapping[str, Any]] = None,
        options: Optional[RequestOptions] = None,
        *,
        base_address: BaseAddress,
    ) -> "KhipuObject":
        api_mode = get_api_mode(url)
        requestor = self._replace_options(options)
        rbody, rcode, rheaders = requestor.request_raw(
            method.lower(),
            url,
            params,
            api_mode=api_mode,
            base_address=base_address,
        )
        resp = requestor._interpret_response(rbody, rcode, rheaders, api_mode)

        obj = _convert_to_khipu_object(
            resp=resp,
            params=params,
            requestor=requestor,
            api_mode=api_mode,
        )

        return obj

    def request_headers(self, method: HttpVerb, api_mode: ApiMode, options: RequestOptions):
        user_agent = f"khipu_tools/{khipu_tools.VERSION}"
        if khipu_tools.app_info:
            user_agent += " " + self._format_app_info(khipu_tools.app_info)

        headers: dict[str, str] = {
            "User-Agent": user_agent,
            "x-api-key": options.get("api_key"),
        }

        headers["Content-Type"] = "application/json"

        return headers

    def _args_for_request_with_retries(
        self,
        method: str,
        url: str,
        params: Optional[Mapping[str, Any]] = None,
        options: Optional[RequestOptions] = None,
        *,
        base_address: BaseAddress,
        api_mode: ApiMode,
    ):
        """
        Mechanism for issuing an API call.  Used by request_raw and request_raw_async.
        """
        request_options = merge_options(self._options, options)

        if request_options.get("api_key") is None:
            raise error.AuthenticationError("No API key provided.")

        abs_url = "{}{}".format(
            self._options.base_addresses.get(base_address),
            url,
        )

        params = params or {}
        if params and (method == "get" or method == "delete"):
            # if we're sending params in the querystring, then we have to make sure we're not
            # duplicating anything we got back from the server already (like in a list iterator)
            # so, we parse the querystring the server sends back so we can merge with
            # what we (or the user) are trying to send
            existing_params = {}
            for k, v in parse_qs(urlsplit(url).query).items():
                # note: server sends back "expand[]" but users supply "expand", so we
                # strip the brackets from the key name
                if k.endswith("[]"):
                    existing_params[k[:-2]] = v
                else:
                    # all querystrings are pulled out as lists.
                    # We want to keep the querystrings that actually are lists, but flatten
                    # the ones that are single values
                    existing_params[k] = v[0] if len(v) == 1 else v

            params = {
                **existing_params,
                # user_supplied params take precedence over server params
                **params,
            }

        encoded_params = urlencode(list(_api_encode(params or {}, api_mode)))

        # Don't use strict form encoding by changing the square bracket control
        # characters back to their literals. This is fine by the server, and
        # makes these parameter strings easier to read.
        encoded_params = encoded_params.replace("%5B", "[").replace("%5D", "]")

        encoded_body = json.dumps(params or {}, default=_json_encode_date_callback)

        supplied_headers = None
        if "headers" in request_options and request_options["headers"] is not None:
            supplied_headers = dict(request_options["headers"])

        headers = self.request_headers(
            # this cast is safe because the blocks below validate that `method` is one of the allowed values
            cast(HttpVerb, method),
            api_mode,
            request_options,
        )

        if method == "get" or method == "delete":
            if params:
                # if we're sending query params, we've already merged the incoming ones with the server's "url"
                # so we can overwrite the whole thing
                scheme, netloc, path, _, fragment = urlsplit(abs_url)

                abs_url = urlunsplit((scheme, netloc, path, encoded_params, fragment))
            post_data = None
        elif method == "post":
            post_data = encoded_body
            print(f"_api_requestor.py:399> {post_data=}")
        else:
            raise error.APIConnectionError(f"Unrecognized HTTP method {method!r}.")

        if supplied_headers is not None:
            for key, value in supplied_headers.items():
                headers[key] = value

        return (
            # Actual args
            method,
            abs_url,
            headers,
            post_data,
            # For logging
            encoded_params,
            khipu_tools._ApiVersion.CURRENT,
        )

    def request_raw(
        self,
        method: str,
        url: str,
        params: Optional[Mapping[str, Any]] = None,
        options: Optional[RequestOptions] = None,
        *,
        base_address: BaseAddress,
        api_mode: ApiMode,
    ) -> tuple[object, int, Mapping[str, str]]:
        (
            method,
            abs_url,
            headers,
            post_data,
            encoded_params,
            api_version,
        ) = self._args_for_request_with_retries(
            method,
            url,
            params,
            options,
            base_address=base_address,
            api_mode=api_mode,
        )

        log_info("Request to Khipu api", method=method, url=abs_url)
        log_debug(
            "Payload",
            post_data=encoded_params,
            api_version=api_version,
            api_mode=api_mode,
        )

        (rcontent, rcode, rheaders) = self._get_http_client().request_with_retries(
            method,
            abs_url,
            headers,
            post_data,
        )
        log_info("Khipu API response", path=abs_url, response_code=rcode)
        log_debug("API response body", body=rcontent)

        return rcontent, rcode, rheaders

    def _interpret_response(
        self,
        rbody: object,
        rcode: int,
        rheaders: Mapping[str, str],
        api_mode: ApiMode,
    ) -> KhipuResponse:

        try:
            resp = KhipuResponse(
                cast(str, rbody),
                rcode,
                rheaders,
            )
        except Exception:
            raise error.APIError(
                f"Invalid response body from API: {rcode} -- " f"HTTP response  was: {rbody})",
                cast(bytes, rbody),
                rcode,
                cast(bytes, rbody),
                rheaders,
            )
        return resp
