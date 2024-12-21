from typing import Any, Optional

from khipu_tools._api_mode import ApiMode
from khipu_tools._khipu_object import KhipuObject
from khipu_tools._util import merge_dicts


class ErrorObject(KhipuObject):
    charge: Optional[str]
    code: Optional[str]
    decline_code: Optional[str]
    doc_url: Optional[str]
    message: Optional[str]
    param: Optional[str]
    payment_intent: Optional[Any]
    payment_method: Optional[Any]
    setup_intent: Optional[Any]
    source: Optional[Any]
    type: str

    def refresh_from(
        self,
        values,
        api_key=None,
        partial=False,
        last_response=None,
        *,
        api_mode: ApiMode = "V3",
    ):
        return self._refresh_from(
            values=values,
            partial=partial,
            last_response=last_response,
            requestor=self._requestor._replace_options(
                {
                    "api_key": api_key,
                }
            ),
            api_mode=api_mode,
        )

    def _refresh_from(
        self,
        *,
        values,
        partial=False,
        last_response=None,
        requestor,
        api_mode: ApiMode,
    ) -> None:
        values = merge_dicts(
            {
                "code": None,
                "doc_url": None,
                "message": None,
                "param": None,
                "source": None,
                "type": None,
            },
            values,
        )
        return super()._refresh_from(
            values=values,
            partial=partial,
            last_response=last_response,
            requestor=requestor,
            api_mode=api_mode,
        )
