"""
Type protocols for CRUD operations.

This module defines Protocol classes that provide overload signatures
for common CRUD operations (GET, POST, PUT, DELETE). These protocols
ensure consistent type hints across all generated endpoint classes while
reducing code duplication.

These protocols are purely for type checking and IDE autocomplete - they
have no runtime behavior.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Protocol, TypeVar, overload

if TYPE_CHECKING:
    from hfortix_fortios.models import FortiObject


# Type variable for the identifier/mkey type (usually str or int)
MKeyT = TypeVar("MKeyT", bound=str | int)


class GetProtocol(Protocol):
    """
    Protocol defining type-safe overloads for GET operations.

    This protocol defines all possible return types based on:
    - Whether an identifier (mkey) is provided
    - The value of raw_json parameter
    - The value of response_mode parameter
    """

    # Overload for response_mode="object" with mkey provided (single object)
    @overload
    def get(
        self,
        name: str,
        filter: list[str] | None = None,
        count: int | None = None,
        start: int | None = None,
        payload_dict: dict[str, Any] | None = None,
        vdom: str | bool | None = None,
        raw_json: Literal[False] = False,
        response_mode: Literal["object"] = ...,
        **kwargs: Any,
    ) -> FortiObject: ...

    # Overload for response_mode="object" without mkey (list of objects)
    @overload
    def get(
        self,
        name: None = None,
        filter: list[str] | None = None,
        count: int | None = None,
        start: int | None = None,
        payload_dict: dict[str, Any] | None = None,
        vdom: str | bool | None = None,
        raw_json: Literal[False] = False,
        response_mode: Literal["object"] = ...,
        **kwargs: Any,
    ) -> list[FortiObject]: ...

    # Overload for response_mode="dict" with mkey provided (single dict)
    @overload
    def get(
        self,
        name: str,
        filter: list[str] | None = None,
        count: int | None = None,
        start: int | None = None,
        payload_dict: dict[str, Any] | None = None,
        vdom: str | bool | None = None,
        raw_json: Literal[False] = False,
        response_mode: Literal["dict"] = ...,
        **kwargs: Any,
    ) -> dict[str, Any]: ...

    # Overload for response_mode="dict" without mkey (list of dicts)
    @overload
    def get(
        self,
        name: None = None,
        filter: list[str] | None = None,
        count: int | None = None,
        start: int | None = None,
        payload_dict: dict[str, Any] | None = None,
        vdom: str | bool | None = None,
        raw_json: Literal[False] = False,
        response_mode: Literal["dict"] = ...,
        **kwargs: Any,
    ) -> dict[str, Any]: ...

    # Overload for default behavior WITH name (returns dict - client default is dict mode)
    @overload
    def get(
        self,
        name: str,
        filter: list[str] | None = None,
        count: int | None = None,
        start: int | None = None,
        payload_dict: dict[str, Any] | None = None,
        vdom: str | bool | None = None,
        raw_json: Literal[False] = False,
        response_mode: None = None,
        **kwargs: Any,
    ) -> dict[str, Any]: ...

    # Overload for default behavior WITHOUT name (returns dict - client default is dict mode)
    @overload
    def get(
        self,
        name: None = None,
        filter: list[str] | None = None,
        count: int | None = None,
        start: int | None = None,
        payload_dict: dict[str, Any] | None = None,
        vdom: str | bool | None = None,
        raw_json: Literal[False] = False,
        response_mode: None = None,
        **kwargs: Any,
    ) -> dict[str, Any]: ...

    # Overload for raw_json=True
    @overload
    def get(
        self,
        name: str | None = None,
        filter: list[str] | None = None,
        count: int | None = None,
        start: int | None = None,
        payload_dict: dict[str, Any] | None = None,
        vdom: str | bool | None = None,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> dict[str, Any]: ...


class PostProtocol(Protocol):
    """
    Protocol defining type-safe overloads for POST (create) operations.
    """

    # Overload for default behavior (no response_mode, no raw_json)
    @overload
    def post(
        self,
        payload_dict: dict[str, Any] | None = None,
        vdom: str | bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | FortiObject: ...

    # Overload for raw_json=True
    @overload
    def post(
        self,
        payload_dict: dict[str, Any] | None = None,
        vdom: str | bool | None = None,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> dict[str, Any]: ...

    # Overload for response_mode="dict"
    @overload
    def post(
        self,
        payload_dict: dict[str, Any] | None = None,
        vdom: str | bool | None = None,
        raw_json: Literal[False] = False,
        response_mode: Literal["dict"] = ...,
        **kwargs: Any,
    ) -> dict[str, Any]: ...

    # Overload for response_mode="object" - MOST SPECIFIC LAST
    @overload
    def post(
        self,
        payload_dict: dict[str, Any] | None = None,
        vdom: str | bool | None = None,
        raw_json: Literal[False] = False,
        response_mode: Literal["object"] = ...,
        **kwargs: Any,
    ) -> FortiObject: ...


class PutProtocol(Protocol):
    """
    Protocol defining type-safe overloads for PUT (update) operations.
    """

    # Overload for default behavior (no response_mode, no raw_json)
    @overload
    def put(
        self,
        payload_dict: dict[str, Any] | None = None,
        vdom: str | bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | FortiObject: ...

    # Overload for raw_json=True
    @overload
    def put(
        self,
        payload_dict: dict[str, Any] | None = None,
        vdom: str | bool | None = None,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> dict[str, Any]: ...

    # Overload for response_mode="dict"
    @overload
    def put(
        self,
        payload_dict: dict[str, Any] | None = None,
        vdom: str | bool | None = None,
        raw_json: Literal[False] = False,
        response_mode: Literal["dict"] = ...,
        **kwargs: Any,
    ) -> dict[str, Any]: ...

    # Overload for response_mode="object" - MOST SPECIFIC LAST
    @overload
    def put(
        self,
        payload_dict: dict[str, Any] | None = None,
        vdom: str | bool | None = None,
        raw_json: Literal[False] = False,
        response_mode: Literal["object"] = ...,
        **kwargs: Any,
    ) -> FortiObject: ...


class DeleteProtocol(Protocol):
    """
    Protocol defining type-safe overloads for DELETE operations.
    """

    # Overload for default behavior (no response_mode, no raw_json)
    @overload
    def delete(
        self,
        name: str | None = None,
        vdom: str | bool | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | FortiObject: ...

    # Overload for raw_json=True
    @overload
    def delete(
        self,
        name: str | None = None,
        vdom: str | bool | None = None,
        raw_json: Literal[True] = ...,
        **kwargs: Any,
    ) -> dict[str, Any]: ...

    # Overload for response_mode="dict" (explicitly set)
    @overload
    def delete(
        self,
        name: str | None = None,
        vdom: str | bool | None = None,
        raw_json: Literal[False] = False,
        response_mode: Literal["dict"] = ...,
        **kwargs: Any,
    ) -> dict[str, Any]: ...

    # Overload for response_mode="object" (explicitly set) - MOST SPECIFIC LAST
    @overload
    def delete(
        self,
        name: str | None = None,
        vdom: str | bool | None = None,
        raw_json: Literal[False] = False,
        response_mode: Literal["object"] = ...,
        **kwargs: Any,
    ) -> FortiObject: ...


class CRUDEndpoint(
    GetProtocol, PostProtocol, PutProtocol, DeleteProtocol, Protocol
):
    """
    Combined protocol for full CRUD endpoints.

    Endpoint classes can inherit from this to get all CRUD overloads
    without repeating them in each generated file.
    """

    pass
