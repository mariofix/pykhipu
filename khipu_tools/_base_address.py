from typing import Literal, TypedDict, Optional
from typing_extensions import NotRequired

BaseAddress = Literal["api"]


class BaseAddresses(TypedDict):
    api: NotRequired[Optional[str]]
