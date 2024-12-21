from typing import Optional

import khipu_tools
from khipu_tools._base_address import BaseAddresses


class RequestorOptions:
    api_key: Optional[str]
    base_addresses: BaseAddresses

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_addresses: BaseAddresses = {},
    ):
        self.api_key = api_key
        self.base_addresses = {}

        if base_addresses.get("api"):
            self.base_addresses["api"] = base_addresses.get("api")

    def to_dict(self):
        return {
            "api_key": self.api_key,
            "base_addresses": self.base_addresses,
        }


class _GlobalRequestorOptions(RequestorOptions):
    def __init__(self):
        pass

    @property
    def base_addresses(self):
        return {
            "api": khipu_tools.api_base,
        }

    @property
    def api_key(self):
        return khipu_tools.api_key
