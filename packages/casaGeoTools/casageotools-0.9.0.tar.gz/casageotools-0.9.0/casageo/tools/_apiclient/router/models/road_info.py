from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.road_info_type import RoadInfoType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.localized_route_number import LocalizedRouteNumber
    from ..models.localized_string import LocalizedString


T = TypeVar("T", bound="RoadInfo")


@_attrs_define
class RoadInfo:
    """Road information attached to an offset action

    Example:
        {'fennstrasse': {'type': 'street', 'name': [{'value': 'Fennstraße', 'language': 'de'}], 'number': [{'value':
            'B96', 'language': 'de'}], 'toward': [{'value': 'Reinickendorf', 'language': 'de'}]}}

    Attributes:
        type_ (RoadInfoType | Unset): Type of the road (rural, urban, highway)
        name (list[LocalizedString] | Unset): Name of the road

            If the road has multiple names, each name will be a separate entry in the array.
            The road names can be in multiple languages. If a preferred language was provided,
            and names in that language are available, they will be prioritized in the array.
            Otherwise the default name of the street is prioritized.
        number (list[LocalizedRouteNumber] | Unset): Route name or number (e.g. 'M25')
        toward (list[LocalizedString] | Unset): Names of destinations on sign which can be reached when going in that
            direction
    """

    type_: RoadInfoType | Unset = UNSET
    name: list[LocalizedString] | Unset = UNSET
    number: list[LocalizedRouteNumber] | Unset = UNSET
    toward: list[LocalizedString] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        name: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.name, Unset):
            name = []
            for name_item_data in self.name:
                name_item = name_item_data.to_dict()
                name.append(name_item)

        number: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.number, Unset):
            number = []
            for number_item_data in self.number:
                number_item = number_item_data.to_dict()
                number.append(number_item)

        toward: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.toward, Unset):
            toward = []
            for toward_item_data in self.toward:
                toward_item = toward_item_data.to_dict()
                toward.append(toward_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if name is not UNSET:
            field_dict["name"] = name
        if number is not UNSET:
            field_dict["number"] = number
        if toward is not UNSET:
            field_dict["toward"] = toward

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.localized_route_number import LocalizedRouteNumber
        from ..models.localized_string import LocalizedString

        d = dict(src_dict)
        _type_ = d.pop("type", UNSET)
        type_: RoadInfoType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = RoadInfoType(_type_)

        _name = d.pop("name", UNSET)
        name: list[LocalizedString] | Unset = UNSET
        if _name is not UNSET:
            name = []
            for name_item_data in _name:
                name_item = LocalizedString.from_dict(name_item_data)

                name.append(name_item)

        _number = d.pop("number", UNSET)
        number: list[LocalizedRouteNumber] | Unset = UNSET
        if _number is not UNSET:
            number = []
            for number_item_data in _number:
                number_item = LocalizedRouteNumber.from_dict(number_item_data)

                number.append(number_item)

        _toward = d.pop("toward", UNSET)
        toward: list[LocalizedString] | Unset = UNSET
        if _toward is not UNSET:
            toward = []
            for toward_item_data in _toward:
                toward_item = LocalizedString.from_dict(toward_item_data)

                toward.append(toward_item)

        road_info = cls(
            type_=type_,
            name=name,
            number=number,
            toward=toward,
        )

        road_info.additional_properties = d
        return road_info

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
