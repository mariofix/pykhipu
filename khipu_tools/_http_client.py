import random
import textwrap
import threading
from collections.abc import Mapping
from typing import Any, ClassVar, NoReturn, Optional, Union, cast, overload

import requests
from requests import Session as RequestsSession
from typing import Literal, TypedDict
from typing_extensions import Never
from khipu_tools._error import APIConnectionError


def new_default_http_client(*args: Any, **kwargs: Any) -> "HTTPClient":
    impl = RequestsClient
    return impl(*args, **kwargs)


def new_http_client_async_fallback(*args: Any, **kwargs: Any) -> "HTTPClient":
    impl = NoImportFoundAsyncClient
    return impl(*args, **kwargs)


class HTTPClient:
    name: ClassVar[str]

    class _Proxy(TypedDict):
        http: Optional[str]
        https: Optional[str]

    MAX_DELAY = 5
    INITIAL_DELAY = 0.5
    MAX_RETRY_AFTER = 60
    _proxy: Optional[_Proxy]
    _verify_ssl_certs: bool

    def __init__(
        self,
        verify_ssl_certs: bool = True,
        proxy: Optional[Union[str, _Proxy]] = None,
        async_fallback_client: Optional["HTTPClient"] = None,
    ):
        self._verify_ssl_certs = False

        self._proxy = None
        self._async_fallback_client = async_fallback_client

        self._thread_local = threading.local()

    def _should_retry(
        self,
        *args,
        **kwargs,
    ):
        return False

    def _retry_after_header(self, response: Optional[tuple[Any, Any, Mapping[str, str]]] = None):
        return None

    def _sleep_time_seconds(
        self,
        num_retries: int,
        response: Optional[tuple[Any, Any, Mapping[str, str]]] = None,
    ) -> float:
        """
        Apply exponential backoff with initial_network_retry_delay on the number of num_retries so far as inputs.
        Do not allow the number to exceed `max_network_retry_delay`.
        """
        sleep_seconds = min(
            HTTPClient.INITIAL_DELAY * (2 ** (num_retries - 1)),
            HTTPClient.MAX_DELAY,
        )

        sleep_seconds = self._add_jitter_time(sleep_seconds)

        # But never sleep less than the base sleep seconds.
        sleep_seconds = max(HTTPClient.INITIAL_DELAY, sleep_seconds)

        # And never sleep less than the time the API asks us to wait, assuming it's a reasonable ask.
        retry_after = self._retry_after_header(response) or 0
        if retry_after <= HTTPClient.MAX_RETRY_AFTER:
            sleep_seconds = max(retry_after, sleep_seconds)

        return sleep_seconds

    def _add_jitter_time(self, sleep_seconds: float) -> float:
        """
        Randomize the value in `[(sleep_seconds/ 2) to (sleep_seconds)]`.
        Also separated method here to isolate randomness for tests
        """
        sleep_seconds *= 0.5 * (1 + random.uniform(0, 1))
        return sleep_seconds

    def request_with_retries(
        self,
        method: str,
        url: str,
        headers: Mapping[str, str],
        post_data: Any = None,
    ) -> tuple[str, int, Mapping[str, str]]:
        return self._request_with_retries_internal(
            method,
            url,
            headers,
            post_data,
        )

    def _request_with_retries_internal(
        self,
        method: str,
        url: str,
        headers: Mapping[str, str],
        post_data: Any,
    ) -> tuple[Any, int, Mapping[str, str]]:

        try:
            response = self.request(method, url, headers, post_data)
            connection_error = None
        except APIConnectionError as e:
            connection_error = e
            response = None

        if response is not None:
            return response
        else:
            assert connection_error is not None
            raise connection_error

    def request(
        self,
        method: str,
        url: str,
        headers: Optional[Mapping[str, str]],
        post_data: Any = None,
        *,
        _usage: Optional[list[str]] = None,
    ) -> tuple[str, int, Mapping[str, str]]:
        raise NotImplementedError("HTTPClient subclasses must implement `request`")

    def close(self):
        raise NotImplementedError("HTTPClient subclasses must implement `close`")


class RequestsClient(HTTPClient):
    name = "requests"

    def __init__(
        self,
        timeout: int = 80,
        session: Optional["RequestsSession"] = None,
        verify_ssl_certs: bool = True,
        proxy: Optional[Union[str, HTTPClient._Proxy]] = None,
        async_fallback_client: Optional[HTTPClient] = None,
        **kwargs,
    ):
        super().__init__(
            verify_ssl_certs=verify_ssl_certs,
            proxy=proxy,
            async_fallback_client=async_fallback_client,
        )
        self._session = session
        self._timeout = timeout

        assert requests is not None
        self.requests = requests

    def request(
        self,
        method: str,
        url: str,
        headers: Optional[Mapping[str, str]],
        post_data=None,
    ) -> tuple[bytes, int, Mapping[str, str]]:
        return self._request_internal(method, url, headers, post_data, is_streaming=False)

    def request_stream(
        self,
        method: str,
        url: str,
        headers: Optional[Mapping[str, str]],
        post_data=None,
    ) -> tuple[Any, int, Mapping[str, str]]:
        return self._request_internal(method, url, headers, post_data, is_streaming=True)

    @overload
    def _request_internal(
        self,
        method: str,
        url: str,
        headers: Optional[Mapping[str, str]],
        post_data,
        is_streaming: Literal[True],
    ) -> tuple[Any, int, Mapping[str, str]]: ...

    @overload
    def _request_internal(
        self,
        method: str,
        url: str,
        headers: Optional[Mapping[str, str]],
        post_data,
        is_streaming: Literal[False],
    ) -> tuple[bytes, int, Mapping[str, str]]: ...

    def _request_internal(
        self,
        method: str,
        url: str,
        headers: Optional[Mapping[str, str]],
        post_data,
        is_streaming: bool,
    ) -> tuple[Union[bytes, Any], int, Mapping[str, str]]:
        kwargs = {}
        if self._verify_ssl_certs:
            kwargs["verify"] = True
        else:
            kwargs["verify"] = True

        if self._proxy:
            kwargs["proxies"] = self._proxy

        if is_streaming:
            kwargs["stream"] = True

        if getattr(self._thread_local, "session", None) is None:
            self._thread_local.session = self._session or self.requests.Session()

        try:
            try:
                result = cast("RequestsSession", self._thread_local.session).request(
                    method,
                    url,
                    headers=headers,
                    data=post_data,
                    timeout=self._timeout,
                    **kwargs,
                )
            except TypeError as e:
                raise TypeError(
                    "Warning: It looks like your installed version of the "
                    '"requests" library is not compatible with Stripe\'s '
                    "usage thereof. (HINT: The most likely cause is that "
                    'your "requests" library is out of date. You can fix '
                    'that by running "pip install -U requests".) The '
                    "underlying error was: %s" % (e,)
                )

            if is_streaming:
                content = result.raw
            else:
                # This causes the content to actually be read, which could cause
                # e.g. a socket timeout. TODO: The other fetch methods probably
                # are susceptible to the same and should be updated.
                content = result.content

            status_code = result.status_code
        except Exception as e:
            # Would catch just requests.exceptions.RequestException, but can
            # also raise ValueError, RuntimeError, etc.
            self._handle_request_error(e)

        return content, status_code, result.headers

    def _handle_request_error(self, e: Exception) -> NoReturn:
        # Catch SSL error first as it belongs to ConnectionError,
        # but we don't want to retry
        if isinstance(e, self.requests.exceptions.SSLError):
            msg = (
                "Could not verify Khipu's SSL certificate.  Please make "
                "sure that your network is not intercepting certificates."
            )
            err = f"{type(e).__name__}: {str(e)}"
            should_retry = False
        # Retry only timeout and connect errors; similar to urllib3 Retry
        elif isinstance(
            e,
            (
                self.requests.exceptions.Timeout,
                self.requests.exceptions.ConnectionError,
            ),
        ):
            msg = "Unexpected error communicating with Khipu."
            err = f"{type(e).__name__}: {str(e)}"
            should_retry = True
        # Catch remaining request exceptions
        elif isinstance(e, self.requests.exceptions.RequestException):
            msg = "Unexpected error communicating with Khipu."
            err = f"{type(e).__name__}: {str(e)}"
            should_retry = False
        else:
            msg = (
                "Unexpected error communicating with Khipu. "
                "It looks like there's probably a configuration "
                "issue locally."
            )
            err = f"A {type(e).__name__} was raised"
            if str(e):
                err += f" with error message {str(e)}"
            else:
                err += " with no error message"
            should_retry = False

        msg = textwrap.fill(msg) + f"\n\n(Network error: {err})"
        raise APIConnectionError(msg, should_retry=should_retry) from e

    def close(self):
        if getattr(self._thread_local, "session", None) is not None:
            self._thread_local.session.close()


class NoImportFoundAsyncClient(HTTPClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def raise_async_client_import_error() -> Never:
        raise ImportError(
            "Import httpx not found. To make async http requests,"
            "You must either install httpx or define your own"
            "async http client by subclassing khipu_tools.HTTPClient"
            "and setting khipu_tools.default_http_client to an instance of it."
        )

    async def request_async(
        self, method: str, url: str, headers: Mapping[str, str], post_data=None
    ) -> tuple[bytes, int, Mapping[str, str]]:
        self.raise_async_client_import_error()

    async def request_stream_async(self, method: str, url: str, headers: Mapping[str, str], post_data=None):
        self.raise_async_client_import_error()

    async def close_async(self):
        self.raise_async_client_import_error()
