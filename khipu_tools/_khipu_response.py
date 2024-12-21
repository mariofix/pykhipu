import json
from collections import OrderedDict
from collections.abc import Mapping


class KhipuResponseBase:
    code: int
    headers: Mapping[str, str]

    def __init__(self, code: int, headers: Mapping[str, str]):
        self.code = code
        self.headers = headers


class KhipuResponse(KhipuResponseBase):
    body: str
    data: object

    def __init__(self, body: str, code: int, headers: Mapping[str, str]):
        KhipuResponseBase.__init__(self, code, headers)
        self.body = body
        self.data = json.loads(body, object_pairs_hook=OrderedDict)
