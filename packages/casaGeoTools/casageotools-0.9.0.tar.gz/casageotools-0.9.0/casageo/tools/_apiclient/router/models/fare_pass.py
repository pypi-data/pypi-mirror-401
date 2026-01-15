from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fare_pass_validity_period import FarePassValidityPeriod


T = TypeVar("T", bound="FarePass")


@_attrs_define
class FarePass:
    """Specifies whether this `Fare` is a multi-travel pass, and its characteristics

    Attributes:
        return_journey (bool | Unset): This pass includes the fare for the return journey.
        validity_period (FarePassValidityPeriod | Unset): Specifies a temporal validity period for a pass
        travels (int | Unset): This pass allows for the specified number of travels.
        transfers (int | Unset): Indicates if transfers are permitted with this pass, and if so, how many.
        senior_pass (bool | Unset): This pass is valid only if presented by a senior person.
    """

    return_journey: bool | Unset = UNSET
    validity_period: FarePassValidityPeriod | Unset = UNSET
    travels: int | Unset = UNSET
    transfers: int | Unset = UNSET
    senior_pass: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return_journey = self.return_journey

        validity_period: dict[str, Any] | Unset = UNSET
        if not isinstance(self.validity_period, Unset):
            validity_period = self.validity_period.to_dict()

        travels = self.travels

        transfers = self.transfers

        senior_pass = self.senior_pass

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if return_journey is not UNSET:
            field_dict["returnJourney"] = return_journey
        if validity_period is not UNSET:
            field_dict["validityPeriod"] = validity_period
        if travels is not UNSET:
            field_dict["travels"] = travels
        if transfers is not UNSET:
            field_dict["transfers"] = transfers
        if senior_pass is not UNSET:
            field_dict["seniorPass"] = senior_pass

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.fare_pass_validity_period import FarePassValidityPeriod

        d = dict(src_dict)
        return_journey = d.pop("returnJourney", UNSET)

        _validity_period = d.pop("validityPeriod", UNSET)
        validity_period: FarePassValidityPeriod | Unset
        if isinstance(_validity_period, Unset):
            validity_period = UNSET
        else:
            validity_period = FarePassValidityPeriod.from_dict(_validity_period)

        travels = d.pop("travels", UNSET)

        transfers = d.pop("transfers", UNSET)

        senior_pass = d.pop("seniorPass", UNSET)

        fare_pass = cls(
            return_journey=return_journey,
            validity_period=validity_period,
            travels=travels,
            transfers=transfers,
            senior_pass=senior_pass,
        )

        fare_pass.additional_properties = d
        return fare_pass

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
