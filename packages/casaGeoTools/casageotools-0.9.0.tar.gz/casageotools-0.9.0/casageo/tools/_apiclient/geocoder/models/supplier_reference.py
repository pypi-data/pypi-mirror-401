from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.reference_supplier import ReferenceSupplier


T = TypeVar("T", bound="SupplierReference")


@_attrs_define
class SupplierReference:
    """
    Attributes:
        supplier (ReferenceSupplier):
        id (str): Identifier of the place as provided by the supplier.
    """

    supplier: ReferenceSupplier
    id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        supplier = self.supplier.to_dict()

        id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "supplier": supplier,
            "id": id,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.reference_supplier import ReferenceSupplier

        d = dict(src_dict)
        supplier = ReferenceSupplier.from_dict(d.pop("supplier"))

        id = d.pop("id")

        supplier_reference = cls(
            supplier=supplier,
            id=id,
        )

        supplier_reference.additional_properties = d
        return supplier_reference

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
