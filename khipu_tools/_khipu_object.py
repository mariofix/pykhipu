import datetime
import json
from collections.abc import Mapping
from copy import deepcopy
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Optional,
    Union,
    cast,
    overload,
)

from typing import Literal
from typing_extensions import Self

# Used to break circular imports
import khipu_tools
from khipu_tools import _util
from khipu_tools._api_mode import ApiMode
from khipu_tools._base_address import BaseAddress
from khipu_tools._encode import _encode_datetime
from khipu_tools._khipu_response import KhipuResponse
from khipu_tools._request_options import extract_options_from_dict

if TYPE_CHECKING:
    from khipu_tools import _APIRequestor  # type: ignore


@overload
def _compute_diff(current: dict[str, Any], previous: Optional[dict[str, Any]]) -> dict[str, Any]: ...


@overload
def _compute_diff(current: object, previous: Optional[dict[str, Any]]) -> object: ...


def _compute_diff(current: object, previous: Optional[dict[str, Any]]) -> object:
    if isinstance(current, dict):
        current = cast(dict[str, Any], current)
        previous = previous or {}
        diff = current.copy()
        for key in set(previous.keys()) - set(diff.keys()):
            diff[key] = ""
        return diff
    return current if current is not None else ""


def _serialize_list(array: Optional[list[Any]], previous: list[Any]) -> dict[str, Any]:
    array = array or []
    previous = previous or []
    params: dict[str, Any] = {}

    for i, v in enumerate(array):
        previous_item = previous[i] if len(previous) > i else None
        if hasattr(v, "serialize"):
            params[str(i)] = v.serialize(previous_item)
        else:
            params[str(i)] = _compute_diff(v, previous_item)

    return params


class KhipuObject(dict[str, Any]):
    class _ReprJSONEncoder(json.JSONEncoder):
        def default(self, o: Any) -> Any:
            if isinstance(o, datetime.datetime):
                return _encode_datetime(o)
            return super().default(o)

    _retrieve_params: Mapping[str, Any]
    _previous: Optional[Mapping[str, Any]]

    def __init__(
        self,
        id: Optional[str] = None,
        api_key: Optional[str] = None,
        last_response: Optional[KhipuResponse] = None,
        *,
        _requestor: Optional["_APIRequestor"] = None,
        **params: Any,
    ):
        super().__init__()

        self._unsaved_values: set[str] = set()
        self._transient_values: set[str] = set()
        self._last_response = last_response

        self._retrieve_params = params
        self._previous = None

        self._requestor = (
            khipu_tools._APIRequestor._global_with_options(
                api_key=api_key,
            )
            if _requestor is None
            else _requestor
        )

        if id:
            self["id"] = id

    @property
    def api_key(self):
        return self._requestor.api_key

    @property
    def last_response(self) -> Optional[KhipuResponse]:
        return self._last_response

    # KhipuObject inherits from `dict` which has an update method, and this doesn't quite match
    # the full signature of the update method in MutableMapping. But we ignore.
    def update(self, update_dict: Mapping[str, Any]) -> None:  # pyright: ignore
        for k in update_dict:
            self._unsaved_values.add(k)

        return super().update(update_dict)

    if not TYPE_CHECKING:

        def __setattr__(self, k, v):
            if k in {"api_key"}:
                self._requestor = self._requestor._replace_options({k: v})
                return None

            if k[0] == "_" or k in self.__dict__:
                return super().__setattr__(k, v)

            self[k] = v
            return None

        def __getattr__(self, k):
            if k[0] == "_":
                raise AttributeError(k)

            try:
                if k in self._field_remappings:
                    k = self._field_remappings[k]
                return self[k]
            except KeyError as err:
                raise AttributeError(*err.args) from err

        def __delattr__(self, k):
            if k[0] == "_" or k in self.__dict__:
                return super().__delattr__(k)
            else:
                del self[k]

    def __setitem__(self, k: str, v: Any) -> None:
        if v == "":
            raise ValueError(
                "You cannot set %s to an empty string on this object. "
                "The empty string is treated specially in our requests. "
                "If you'd like to delete the property using the save() method on this object, you may set %s.%s=None. "
                "Alternatively, you can pass %s='' to delete the property when using a resource method such as modify()."
                % (k, str(self), k, k)
            )

        # Allows for unpickling in Python 3.x
        if not hasattr(self, "_unsaved_values"):
            self._unsaved_values = set()

        self._unsaved_values.add(k)

        super().__setitem__(k, v)

    def __getitem__(self, k: str) -> Any:
        try:
            return super().__getitem__(k)
        except KeyError as err:
            if k in self._transient_values:
                raise KeyError(
                    "%r.  HINT: The %r attribute was set in the past."
                    "It was then wiped when refreshing the object with "
                    "the result returned by Stripe's API, probably as a "
                    "result of a save().  The attributes currently "
                    "available on this object are: %s" % (k, k, ", ".join(list(self.keys())))
                )
            else:
                raise err

    def __delitem__(self, k: str) -> None:
        super().__delitem__(k)

        # Allows for unpickling in Python 3.x
        if hasattr(self, "_unsaved_values") and k in self._unsaved_values:
            self._unsaved_values.remove(k)

    # Custom unpickling method that uses `update` to update the dictionary
    # without calling __setitem__, which would fail if any value is an empty
    # string
    def __setstate__(self, state: dict[str, Any]) -> None:
        self.update(state)

    # Custom pickling method to ensure the instance is pickled as a custom
    # class and not as a dict, otherwise __setstate__ would not be called when
    # unpickling.
    def __reduce__(self) -> tuple[Any, ...]:
        reduce_value = (
            type(self),  # callable
            (  # args
                self.get("id", None),
                self.api_key,
            ),
            dict(self),  # state
        )
        return reduce_value

    @classmethod
    def construct_from(
        cls,
        values: dict[str, Any],
        key: Optional[str],
        last_response: Optional[KhipuResponse] = None,
        *,
        api_mode: ApiMode = "V3",
    ) -> Self:
        return cls._construct_from(
            values=values,
            requestor=khipu_tools._APIRequestor._global_with_options(  # pyright: ignore[reportPrivateUsage]
                api_key=key,
            ),
            api_mode=api_mode,
            last_response=last_response,
        )

    @classmethod
    def _construct_from(
        cls,
        *,
        values: dict[str, Any],
        last_response: Optional[KhipuResponse] = None,
        requestor: "_APIRequestor",
        api_mode: ApiMode,
    ) -> Self:
        instance = cls(
            values.get("id"),
            last_response=last_response,
            _requestor=requestor,
        )
        instance._refresh_from(
            values=values,
            last_response=last_response,
            requestor=requestor,
            api_mode=api_mode,
        )
        return instance

    def refresh_from(
        self,
        values: dict[str, Any],
        api_key: Optional[str] = None,
        partial: Optional[bool] = False,
        last_response: Optional[KhipuResponse] = None,
        *,
        api_mode: ApiMode = "V3",
    ) -> None:
        self._refresh_from(
            values=values,
            partial=partial,
            last_response=last_response,
            requestor=self._requestor._replace_options(  # pyright: ignore[reportPrivateUsage]
                {
                    "api_key": api_key,
                }
            ),
            api_mode=api_mode,
        )

    def _refresh_from(
        self,
        *,
        values: dict[str, Any],
        partial: Optional[bool] = False,
        last_response: Optional[KhipuResponse] = None,
        requestor: Optional["_APIRequestor"] = None,
        api_mode: ApiMode,
    ) -> None:
        self._requestor = requestor or self._requestor
        self._last_response = last_response or getattr(values, "_last_response", None)

        # Wipe old state before setting new.  This is useful for e.g.
        # updating a customer, where there is no persistent card
        # parameter.  Mark those values which don't persist as transient
        if partial:
            self._unsaved_values = self._unsaved_values - set(values)
        else:
            removed = set(self.keys()) - set(values)
            self._transient_values = self._transient_values | removed
            self._unsaved_values = set()
            self.clear()

        self._transient_values = self._transient_values - set(values)

        for k, v in values.items():
            inner_class = self._get_inner_class_type(k)
            is_dict = self._get_inner_class_is_beneath_dict(k)
            if is_dict:
                obj = {
                    k: (
                        None
                        if v is None
                        else cast(
                            KhipuObject,
                            _util._convert_to_khipu_object(  # pyright: ignore[reportPrivateUsage]
                                resp=v,
                                params=None,
                                klass_=inner_class,
                                requestor=self._requestor,
                                api_mode=api_mode,
                            ),
                        )
                    )
                    for k, v in v.items()
                }
            else:
                obj = cast(
                    Union[KhipuObject, list[KhipuObject]],
                    _util._convert_to_khipu_object(  # pyright: ignore[reportPrivateUsage]
                        resp=v,
                        params=None,
                        klass_=inner_class,
                        requestor=self._requestor,
                        api_mode=api_mode,
                    ),
                )
            super().__setitem__(k, obj)

        self._previous = values

    @_util.deprecated("This will be removed in a future version of khipu_tools.")
    def request(
        self,
        method: Literal["get", "post", "delete"],
        url: str,
        params: Optional[dict[str, Any]] = None,
        *,
        base_address: BaseAddress = "api",
    ) -> "KhipuObject":
        return KhipuObject._request(
            self,
            method,
            url,
            params=params,
            base_address=base_address,
        )

    def _request(
        self,
        method: Literal["get", "post", "delete"],
        url: str,
        params: Optional[Mapping[str, Any]] = None,
        usage: Optional[list[str]] = None,
        *,
        base_address: BaseAddress,
    ) -> "KhipuObject":
        if params is None:
            params = self._retrieve_params

        request_options, request_params = extract_options_from_dict(params)

        return self._requestor.request(
            method,
            url,
            params=request_params,
            options=request_options,
            base_address=base_address,
        )

    def __repr__(self) -> str:
        ident_parts = [type(self).__name__]

        obj_str = self.get("object")
        if isinstance(obj_str, str):
            ident_parts.append(obj_str)

        if isinstance(self.get("id"), str):
            ident_parts.append("id={}".format(self.get("id")))

        unicode_repr = "<{} at {}> JSON: {}".format(
            " ".join(ident_parts),
            hex(id(self)),
            str(self),
        )
        return unicode_repr

    def __str__(self) -> str:
        return json.dumps(
            self._to_dict_recursive(),
            sort_keys=True,
            indent=2,
            cls=self._ReprJSONEncoder,
        )

    def _to_dict_recursive(self) -> dict[str, Any]:
        def maybe_to_dict_recursive(
            value: Optional[Union[KhipuObject, dict[str, Any]]],
        ) -> Optional[dict[str, Any]]:
            if value is None:
                return None
            elif isinstance(value, KhipuObject):
                return value._to_dict_recursive()
            else:
                return value

        return {
            key: (
                list(map(maybe_to_dict_recursive, cast(list[Any], value)))
                if isinstance(value, list)
                else maybe_to_dict_recursive(value)
            )
            for key, value in dict(self).items()
        }

    def serialize(self, previous: Optional[Mapping[str, Any]]) -> dict[str, Any]:
        params: dict[str, Any] = {}
        unsaved_keys = self._unsaved_values or set()
        previous = previous or self._previous or {}

        for k, v in self.items():
            if k == "id" or k.startswith("_"):
                continue
            elif isinstance(v, khipu_tools.APIResource):
                continue
            elif hasattr(v, "serialize"):
                child = v.serialize(previous.get(k, None))
                if child != {}:
                    params[k] = child
            elif k in unsaved_keys:
                params[k] = _compute_diff(v, previous.get(k, None))
            elif k == "additional_owners" and v is not None:
                params[k] = _serialize_list(v, previous.get(k, None))

        return params

    # This class overrides __setitem__ to throw exceptions on inputs that it
    # doesn't like. This can cause problems when we try to copy an object
    # wholesale because some data that's returned from the API may not be valid
    # if it was set to be set manually. Here we override the class' copy
    # arguments so that we can bypass these possible exceptions on __setitem__.
    def __copy__(self) -> "KhipuObject":
        copied = KhipuObject(
            self.get("id"),
            self.api_key,
        )

        copied._retrieve_params = self._retrieve_params

        for k, v in self.items():
            # Call parent's __setitem__ to avoid checks that we've added in the
            # overridden version that can throw exceptions.
            super(KhipuObject, copied).__setitem__(k, v)

        return copied

    # This class overrides __setitem__ to throw exceptions on inputs that it
    # doesn't like. This can cause problems when we try to copy an object
    # wholesale because some data that's returned from the API may not be valid
    # if it was set to be set manually. Here we override the class' copy
    # arguments so that we can bypass these possible exceptions on __setitem__.
    def __deepcopy__(self, memo: dict[int, Any]) -> "KhipuObject":
        copied = self.__copy__()
        memo[id(self)] = copied

        for k, v in self.items():
            # Call parent's __setitem__ to avoid checks that we've added in the
            # overridden version that can throw exceptions.
            super(KhipuObject, copied).__setitem__(k, deepcopy(v, memo))

        return copied

    _field_remappings: ClassVar[dict[str, str]] = {}

    _inner_class_types: ClassVar[dict[str, type["KhipuObject"]]] = {}
    _inner_class_dicts: ClassVar[list[str]] = []

    def _get_inner_class_type(self, field_name: str) -> Optional[type["KhipuObject"]]:
        return self._inner_class_types.get(field_name)

    def _get_inner_class_is_beneath_dict(self, field_name: str):
        return field_name in self._inner_class_dicts
