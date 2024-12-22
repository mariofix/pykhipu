from typing import Optional

from typing import Literal, NotRequired, TypedDict

BaseAddress = Literal["api"]


class BaseAddresses(TypedDict):
    api: NotRequired[Optional[str]]
