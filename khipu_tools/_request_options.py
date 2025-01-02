from collections.abc import Mapping
from typing import Any, Optional, TypedDict

from typing_extensions import NotRequired

from khipu_tools._requestor_options import RequestorOptions


class RequestOptions(TypedDict):
    api_key: NotRequired["str|None"]
    content_type: NotRequired["str|None"]
    headers: NotRequired["Mapping[str, str]|None"]


def merge_options(
    requestor: RequestorOptions,
    request: Optional[RequestOptions],
) -> RequestOptions:
    if request is None:
        return {
            "api_key": requestor.api_key,
            "content_type": None,
            "headers": None,
        }

    return {
        "api_key": request.get("api_key") or requestor.api_key,
        "content_type": request.get("content_type"),
        "headers": request.get("headers"),
    }


def extract_options_from_dict(
    d: Optional[Mapping[str, Any]],
) -> tuple[RequestOptions, dict[str, Any]]:
    if not d:
        return {}, {}
    options: RequestOptions = {}
    d_copy = dict(d)
    for key in [
        "api_key",
        "content_type",
        "headers",
    ]:
        if key in d_copy:
            options[key] = d_copy.pop(key)

    return options, d_copy
