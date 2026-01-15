from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.functional_class_value import FunctionalClassValue

T = TypeVar("T", bound="FunctionalClass")


@_attrs_define
class FunctionalClass:
    """
    Attributes:
        value (FunctionalClassValue):

            Description of supported values:

            - `1`: allowing for high volume, maximum speed traffic movement
            - `2`: allowing for high volume, high speed traffic movement
            - `3`: providing a high volume of traffic movement
            - `4`: providing for a high volume of traffic movement at moderate speeds between neighbourhoods
            - `5`: roads whose volume and traffic movement are below the level of any functional class
    """

    value: FunctionalClassValue
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = self.value.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "value": value,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        value = FunctionalClassValue(d.pop("value"))

        functional_class = cls(
            value=value,
        )

        functional_class.additional_properties = d
        return functional_class

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
