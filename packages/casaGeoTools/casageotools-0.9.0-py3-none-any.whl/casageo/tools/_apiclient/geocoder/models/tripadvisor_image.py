from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.tripadvisor_image_variants import TripadvisorImageVariants
    from ..models.tripadvisor_media_supplier import TripadvisorMediaSupplier


T = TypeVar("T", bound="TripadvisorImage")


@_attrs_define
class TripadvisorImage:
    """
    Attributes:
        href (str): The URL points to the default image provided by Tripadvisor (TM). These default images are typically
            sized for the *medium* format used by Tripadvisor.
            In rare cases, the image may be larger than expected. To ensure consistent rendering across all scenarios, we
            recommend enforcing maximum dimensions when displaying the image.
        supplier (TripadvisorMediaSupplier):
        variants (TripadvisorImageVariants | Unset):
    """

    href: str
    supplier: TripadvisorMediaSupplier
    variants: TripadvisorImageVariants | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        href = self.href

        supplier = self.supplier.to_dict()

        variants: dict[str, Any] | Unset = UNSET
        if not isinstance(self.variants, Unset):
            variants = self.variants.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "href": href,
            "supplier": supplier,
        })
        if variants is not UNSET:
            field_dict["variants"] = variants

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tripadvisor_image_variants import TripadvisorImageVariants
        from ..models.tripadvisor_media_supplier import TripadvisorMediaSupplier

        d = dict(src_dict)
        href = d.pop("href")

        supplier = TripadvisorMediaSupplier.from_dict(d.pop("supplier"))

        _variants = d.pop("variants", UNSET)
        variants: TripadvisorImageVariants | Unset
        if isinstance(_variants, Unset):
            variants = UNSET
        else:
            variants = TripadvisorImageVariants.from_dict(_variants)

        tripadvisor_image = cls(
            href=href,
            supplier=supplier,
            variants=variants,
        )

        tripadvisor_image.additional_properties = d
        return tripadvisor_image

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
