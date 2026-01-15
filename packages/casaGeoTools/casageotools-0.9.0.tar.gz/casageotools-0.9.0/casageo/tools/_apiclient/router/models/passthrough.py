from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.place import Place


T = TypeVar("T", bound="Passthrough")


@_attrs_define
class Passthrough:
    """Describes a location and time the section is passing through.

    Attributes:
        place (Place): A place represents a generic location relevant for the route. Example: {'type': 'place',
            'location': {'lat': 50.339167, 'lng': 18.93}}.
        offset (float | Unset): Passthrough offsets are the coordinate index in the polyline.
    """

    place: Place
    offset: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        place = self.place.to_dict()

        offset = self.offset

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "place": place,
        })
        if offset is not UNSET:
            field_dict["offset"] = offset

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.place import Place

        d = dict(src_dict)
        place = Place.from_dict(d.pop("place"))

        offset = d.pop("offset", UNSET)

        passthrough = cls(
            place=place,
            offset=offset,
        )

        passthrough.additional_properties = d
        return passthrough

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
