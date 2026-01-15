from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.location import Location


T = TypeVar("T", bound="TollCollectionLocation")


@_attrs_define
class TollCollectionLocation:
    """Refers to the physical location where the toll is collected. This can include various structures such as toll
    booths, transponder readers, or number-plate cameras.
    It's important to note that certain toll collection methods, such as vignettes, do not have specific toll collection
    locations associated with them, and therefore this element
    will not be present at all.

    The value of this property is a `Location` that specifies the coordinates of the payment location.

        Attributes:
            location (Location): Location on the Earth Example: {'lat': 52.531677, 'lng': 13.381777}.
            name (str | Unset): A descriptive name of the location.
    """

    location: Location
    name: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        location = self.location.to_dict()

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "location": location,
        })
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.location import Location

        d = dict(src_dict)
        location = Location.from_dict(d.pop("location"))

        name = d.pop("name", UNSET)

        toll_collection_location = cls(
            location=location,
            name=name,
        )

        toll_collection_location.additional_properties = d
        return toll_collection_location

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
