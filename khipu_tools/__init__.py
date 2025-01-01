from khipu_tools._predict import Predict as Predict
from khipu_tools._payments import Payments as Payments
from khipu_tools._banks import Banks as Banks
from khipu_tools._http_client import (
    new_default_http_client as new_default_http_client,
)
from khipu_tools._api_resource import APIResource as APIResource
from khipu_tools._khipu_client import KhipuClient as KhipuClient
from typing import Optional

from typing import Literal

from khipu_tools._api_requestor import _APIRequestor
from khipu_tools._api_version import _ApiVersion
from khipu_tools._app_info import AppInfo as AppInfo
from khipu_tools._version import VERSION as VERSION

# Constants
DEFAULT_API_BASE: str = "https://payment-api.khipu.com"

api_key: Optional[str] = None
api_base: str = DEFAULT_API_BASE
api_version: str = _ApiVersion.CURRENT
default_http_client: Optional["HTTPClient"] = None
app_info: Optional[AppInfo] = None


def ensure_default_http_client():
    _init_default_http_client()


def _init_default_http_client():
    global default_http_client

    default_http_client = new_default_http_client()


log: Optional[Literal["debug", "info"]] = None


def set_app_info(
    name: str,
    url: Optional[str] = None,
    version: Optional[str] = None,
):
    global app_info
    app_info = {
        "name": name,
        "url": url,
        "version": version,
    }


# Infrastructure types
