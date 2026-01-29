"""Parameter types and utilities for NetSuite REST API requests."""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from dataclasses import dataclass, field, fields

__all__ = [
    "ParamsLike",
    "ParamsDict", 
    "BaseParams",
    "ParamSet",
    "GetParams",
    "UpdateParams", 
    "CreateParams",
]

ParamsDict = Dict[str, Any]


@dataclass(frozen=True)
class BaseParams:
    """
    Base class for structured NetSuite query params.
    Subclasses define fields with metadata={"key": "..."} for the querystring key.
    """

    def to_dict(self) -> ParamsDict:
        out: ParamsDict = {}
        for f in fields(self):
            key = f.metadata.get("key")
            if not key:
                key = f.name

            value = getattr(self, f.name)

            # IMPORTANT: do not skip False / 0 / "" accidentally
            if value is None:
                continue

            # common NetSuite style: list => comma-separated string
            if isinstance(value, (list, tuple)):
                value = ",".join(str(v) for v in value)

            # If NetSuite expects lowercase booleans in query params
            if isinstance(value, bool):
                value = "true" if value else "false"

            out[key] = value
        return out


ParamsLike = Union[BaseParams, Mapping[str, Any]]


@dataclass(frozen=True)
class ParamSet:
    """
    A composable container for params.

    Merge order is left-to-right: later entries override earlier ones.
    """
    parts: Tuple[ParamsLike, ...] = ()

    def merge(self, other: Optional[ParamsLike]) -> "ParamSet":
        if other is None:
            return self
        return ParamSet(self.parts + (other,))

    def to_dict(self) -> ParamsDict:
        merged: ParamsDict = {}
        for part in self.parts:
            if isinstance(part, BaseParams):
                merged.update(part.to_dict())
            else:
                merged.update(dict(part))
        return merged


@dataclass(frozen=True)
class GetParams(BaseParams):
    """Parameters for GET requests to retrieve NetSuite records.
    
    Args:
        fields: The names of the fields and sublists on the record. Only the selected 
            fields and sublists will be returned in the response. Can be a string 
            (comma-separated) or list of field names.
        expand: Set to True to automatically expand all sublists, sublist lines, 
            and subrecords on this record.
        simple_enum_format: Set to True to return enumeration values in a format 
            that only shows the internal ID value.
    """
    fields: Union[List[str], str] = field(default=None, metadata={"key": "fields"})
    expand: bool = field(default=False, metadata={"key": "expandSubResources"})
    simple_enum_format: bool = field(default=False, metadata={"key": "simpleEnumFormat"})


@dataclass(frozen=True)
class UpdateParams(BaseParams):
    """Parameters for PATCH requests to update NetSuite records.
    
    Args:
        replace: The names of sublists on this record. All sublist lines will be 
            replaced with lines specified in the request. The names are delimited by comma.
        replace_selected_fields: If set to True, all fields that should be deleted 
            in the update request, including body fields, must be included in the 
            'replace' query parameter.
    """
    replace: Union[List[str], str] = field(default=None, metadata={"key": "replace"})
    replace_selected_fields: bool = field(default=False, metadata={"key": "replaceSelectedFields"})


@dataclass(frozen=True)
class CreateParams(BaseParams):
    """Parameters for POST requests to create NetSuite records.
    
    Args:
        replace: The names of sublists on this record. All sublist lines will be 
            replaced with lines specified in the request. The names are delimited by comma.
    """
    replace: Union[List[str], str] = field(default=None, metadata={"key": "replace"})