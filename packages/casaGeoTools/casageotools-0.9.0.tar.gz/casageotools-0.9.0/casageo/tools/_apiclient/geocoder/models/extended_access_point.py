from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.extended_access_point_type import ExtendedAccessPointType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExtendedAccessPoint")


@_attrs_define
class ExtendedAccessPoint:
    """
    Attributes:
        lat (float): Latitude of the access position. For example: `"52.19404"`
        lng (float): Longitude of the access position. For example: `"8.80135"`
        primary (bool | Unset): Only applies to response items of type `"place"`. Set to true for the primary access
            position when the place
            result has more than one `access` position.
            Only the first element in the access array can have a primary field set to `true`.
        type_ (ExtendedAccessPointType | Unset): Only applies to response items of type `"place"`

            Description of supported values:

            - `delivery`: A designated access position for receiving goods and services, typically used by delivery
            personnel.
            - `emergency`: A position specifically designated for emergency access or services,
              such as ambulance or fire vehicle entry points.
            - `entrance`: A designated access position for larger or complex places, such as shopping malls or sports
            centers,
              where multiple entrances are located around the perimeter. Each entrance provides a specific
              point of entry for visitors.
            - `loading`: An access position to a designated area for the loading and unloading of goods, typically used by
            delivery and service vehicles.
            - `other`: An access type that does not fit into predefined categories, used for unique or less common
            situations.
            - `parking`: An access position to a designated private area for vehicle parking, associated with the place.
            - `taxi`: A position specifically designated for taxi/ride-share pick-up and drop-off services.
        label (str | Unset): Only applies to response items of type `"place"`. The value is a short textual description
            of the access point. Example: "North Entrance"
    """

    lat: float
    lng: float
    primary: bool | Unset = UNSET
    type_: ExtendedAccessPointType | Unset = UNSET
    label: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        lat = self.lat

        lng = self.lng

        primary = self.primary

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        label = self.label

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "lat": lat,
            "lng": lng,
        })
        if primary is not UNSET:
            field_dict["primary"] = primary
        if type_ is not UNSET:
            field_dict["type"] = type_
        if label is not UNSET:
            field_dict["label"] = label

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        lat = d.pop("lat")

        lng = d.pop("lng")

        primary = d.pop("primary", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: ExtendedAccessPointType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = ExtendedAccessPointType(_type_)

        label = d.pop("label", UNSET)

        extended_access_point = cls(
            lat=lat,
            lng=lng,
            primary=primary,
            type_=type_,
            label=label,
        )

        extended_access_point.additional_properties = d
        return extended_access_point

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
