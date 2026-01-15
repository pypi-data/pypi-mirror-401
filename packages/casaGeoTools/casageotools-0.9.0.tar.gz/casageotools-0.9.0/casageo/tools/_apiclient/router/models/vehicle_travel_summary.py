from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.toll_summary import TollSummary


T = TypeVar("T", bound="VehicleTravelSummary")


@_attrs_define
class VehicleTravelSummary:
    """Total value of key attributes for a route section.

    Attributes:
        duration (int): Duration in seconds. Example: 198.
        length (int): Distance in meters. Example: 189.
        base_duration (int | Unset): Duration in seconds. Example: 198.
        consumption (float | Unset): Energy or fuel consumption.
            For EV energy consumption is in kilowatt hours (kWh). For fuel-based vehicles fuel consumption is in Liters (L)
            for diesel, petrol and LPG vehicles, and Kilograms (kg) for CNG vehicles.
        typical_duration (int | Unset): Duration in seconds. Example: 198.
        ml_duration (int | Unset): Duration in seconds. Example: 198.
        tolls (TollSummary | Unset): The summary of the tolls grouped by criteria (total, per system, per country).
        co_2_emission (float | Unset): Estimation of the carbon dioxide emission for the given route section. Unit is
            kilograms with precision to three decimal places.

            Definitions:

            * Total Emission (Well-to-Wheel) = Production Emission (Well-to-Tank) + Operational Emission (Tank-to-Wheel)
            * CO2 Equivalent Emission (CO2e for CH4, N2O, etc.) = Gas Emission * Global Warming Potential (GWP)

            **Notes:**

            * This value represents the operational (tank-to-wheel) carbon dioxide emission.
            * This value represents only the carbon dioxide emission and does not represent the carbon dioxide equivalent
            emission for other gases or particulates.
    """

    duration: int
    length: int
    base_duration: int | Unset = UNSET
    consumption: float | Unset = UNSET
    typical_duration: int | Unset = UNSET
    ml_duration: int | Unset = UNSET
    tolls: TollSummary | Unset = UNSET
    co_2_emission: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        duration = self.duration

        length = self.length

        base_duration = self.base_duration

        consumption = self.consumption

        typical_duration = self.typical_duration

        ml_duration = self.ml_duration

        tolls: dict[str, Any] | Unset = UNSET
        if not isinstance(self.tolls, Unset):
            tolls = self.tolls.to_dict()

        co_2_emission = self.co_2_emission

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "duration": duration,
            "length": length,
        })
        if base_duration is not UNSET:
            field_dict["baseDuration"] = base_duration
        if consumption is not UNSET:
            field_dict["consumption"] = consumption
        if typical_duration is not UNSET:
            field_dict["typicalDuration"] = typical_duration
        if ml_duration is not UNSET:
            field_dict["mlDuration"] = ml_duration
        if tolls is not UNSET:
            field_dict["tolls"] = tolls
        if co_2_emission is not UNSET:
            field_dict["co2Emission"] = co_2_emission

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.toll_summary import TollSummary

        d = dict(src_dict)
        duration = d.pop("duration")

        length = d.pop("length")

        base_duration = d.pop("baseDuration", UNSET)

        consumption = d.pop("consumption", UNSET)

        typical_duration = d.pop("typicalDuration", UNSET)

        ml_duration = d.pop("mlDuration", UNSET)

        _tolls = d.pop("tolls", UNSET)
        tolls: TollSummary | Unset
        if isinstance(_tolls, Unset):
            tolls = UNSET
        else:
            tolls = TollSummary.from_dict(_tolls)

        co_2_emission = d.pop("co2Emission", UNSET)

        vehicle_travel_summary = cls(
            duration=duration,
            length=length,
            base_duration=base_duration,
            consumption=consumption,
            typical_duration=typical_duration,
            ml_duration=ml_duration,
            tolls=tolls,
            co_2_emission=co_2_emission,
        )

        vehicle_travel_summary.additional_properties = d
        return vehicle_travel_summary

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
