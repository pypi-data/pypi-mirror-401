from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.tripadvisor_media_supplier import TripadvisorMediaSupplier


T = TypeVar("T", bound="Editorial")


@_attrs_define
class Editorial:
    """
    Attributes:
        description (str): The editorial content.
        language (str): A language code indicating what language the editorial is in, if known.
        supplier (TripadvisorMediaSupplier):
        href (str | Unset): An optional deep link to a 3rd party source providing the editorials.
    """

    description: str
    language: str
    supplier: TripadvisorMediaSupplier
    href: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        language = self.language

        supplier = self.supplier.to_dict()

        href = self.href

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "description": description,
            "language": language,
            "supplier": supplier,
        })
        if href is not UNSET:
            field_dict["href"] = href

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tripadvisor_media_supplier import TripadvisorMediaSupplier

        d = dict(src_dict)
        description = d.pop("description")

        language = d.pop("language")

        supplier = TripadvisorMediaSupplier.from_dict(d.pop("supplier"))

        href = d.pop("href", UNSET)

        editorial = cls(
            description=description,
            language=language,
            supplier=supplier,
            href=href,
        )

        editorial.additional_properties = d
        return editorial

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
