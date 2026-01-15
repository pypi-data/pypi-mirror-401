from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.access import Access
    from ..models.functional_class import FunctionalClass
    from ..models.physical import Physical
    from ..models.speed_limit import SpeedLimit


T = TypeVar("T", bound="NavigationAttributes")


@_attrs_define
class NavigationAttributes:
    """
    Attributes:
        speed_limits (list[SpeedLimit] | Unset): Speed limit for the navigable road following the direction of traffic
            on the street. If traffic is allowed in both directions
            two value sets will be returned. If the request contained a bearing parameter, then the first entry will match
            the returned
            direction.
        functional_class (list[FunctionalClass] | Unset): The value represents one of the five levels:
        access (list[Access] | Unset): The following boolean values are available for access attributes:
        physical (list[Physical] | Unset): The following boolean values are available for physical attributes:
    """

    speed_limits: list[SpeedLimit] | Unset = UNSET
    functional_class: list[FunctionalClass] | Unset = UNSET
    access: list[Access] | Unset = UNSET
    physical: list[Physical] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        speed_limits: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.speed_limits, Unset):
            speed_limits = []
            for speed_limits_item_data in self.speed_limits:
                speed_limits_item = speed_limits_item_data.to_dict()
                speed_limits.append(speed_limits_item)

        functional_class: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.functional_class, Unset):
            functional_class = []
            for functional_class_item_data in self.functional_class:
                functional_class_item = functional_class_item_data.to_dict()
                functional_class.append(functional_class_item)

        access: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.access, Unset):
            access = []
            for access_item_data in self.access:
                access_item = access_item_data.to_dict()
                access.append(access_item)

        physical: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.physical, Unset):
            physical = []
            for physical_item_data in self.physical:
                physical_item = physical_item_data.to_dict()
                physical.append(physical_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if speed_limits is not UNSET:
            field_dict["speedLimits"] = speed_limits
        if functional_class is not UNSET:
            field_dict["functionalClass"] = functional_class
        if access is not UNSET:
            field_dict["access"] = access
        if physical is not UNSET:
            field_dict["physical"] = physical

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.access import Access
        from ..models.functional_class import FunctionalClass
        from ..models.physical import Physical
        from ..models.speed_limit import SpeedLimit

        d = dict(src_dict)
        _speed_limits = d.pop("speedLimits", UNSET)
        speed_limits: list[SpeedLimit] | Unset = UNSET
        if _speed_limits is not UNSET:
            speed_limits = []
            for speed_limits_item_data in _speed_limits:
                speed_limits_item = SpeedLimit.from_dict(speed_limits_item_data)

                speed_limits.append(speed_limits_item)

        _functional_class = d.pop("functionalClass", UNSET)
        functional_class: list[FunctionalClass] | Unset = UNSET
        if _functional_class is not UNSET:
            functional_class = []
            for functional_class_item_data in _functional_class:
                functional_class_item = FunctionalClass.from_dict(
                    functional_class_item_data
                )

                functional_class.append(functional_class_item)

        _access = d.pop("access", UNSET)
        access: list[Access] | Unset = UNSET
        if _access is not UNSET:
            access = []
            for access_item_data in _access:
                access_item = Access.from_dict(access_item_data)

                access.append(access_item)

        _physical = d.pop("physical", UNSET)
        physical: list[Physical] | Unset = UNSET
        if _physical is not UNSET:
            physical = []
            for physical_item_data in _physical:
                physical_item = Physical.from_dict(physical_item_data)

                physical.append(physical_item)

        navigation_attributes = cls(
            speed_limits=speed_limits,
            functional_class=functional_class,
            access=access,
            physical=physical,
        )

        navigation_attributes.additional_properties = d
        return navigation_attributes

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
