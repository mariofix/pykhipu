from typing import Optional

from typing_extensions import Literal, NotRequired, TypedDict

BaseAddress = Literal["api"]


class BaseAddresses(TypedDict):
    api: NotRequired[Optional[str]]
