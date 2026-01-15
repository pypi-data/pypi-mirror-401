from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.tripadvisor_media_supplier import TripadvisorMediaSupplier


T = TypeVar("T", bound="Rating")


@_attrs_define
class Rating:
    """
    Attributes:
        count (int): The current count of user reviews in the supplier database.
        average (float): The current average of user ratings in the supplier database.
        supplier (TripadvisorMediaSupplier):
        href (str | Unset): An optional deep link to a 3rd party source providing the ratings information.
    """

    count: int
    average: float
    supplier: TripadvisorMediaSupplier
    href: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        average = self.average

        supplier = self.supplier.to_dict()

        href = self.href

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "count": count,
            "average": average,
            "supplier": supplier,
        })
        if href is not UNSET:
            field_dict["href"] = href

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tripadvisor_media_supplier import TripadvisorMediaSupplier

        d = dict(src_dict)
        count = d.pop("count")

        average = d.pop("average")

        supplier = TripadvisorMediaSupplier.from_dict(d.pop("supplier"))

        href = d.pop("href", UNSET)

        rating = cls(
            count=count,
            average=average,
            supplier=supplier,
            href=href,
        )

        rating.additional_properties = d
        return rating

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
