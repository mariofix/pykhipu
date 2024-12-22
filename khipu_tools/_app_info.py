from typing import Optional

from typing import TypedDict


class AppInfo(TypedDict):
    name: str
    url: Optional[str]
    version: Optional[str]
