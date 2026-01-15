from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BaseEVEmpiricalModel")


@_attrs_define
class BaseEVEmpiricalModel:
    """Specifies parameters required for calculation of energy consumption for electric vehicles using Empirical model.

    Attributes:
        free_flow_speed_table (str): Function curve specifying consumption rate at a given speed.

            The format of the string is a comma-separated list of numbers, as follows:

            ```
            <SPEED_0>,<CONSUMPTION_0>,<SPEED_1>,<CONSUMPTION_1>,...,<SPEED_N>,<CONSUMPTION_N>
            ```

            where speed values are strictly increasing, non-negative integers in units of (km/h), and
            consumption values are non-negative floating point values.

            * Unit for EV:
            | Vehicle Type | Unit |
            |--------------|------|
            | Electric | Wh/m i.e., Watt-hours per meter|

            * Units for Fuel-based vehicles:
            | Vehicle Type | Unit |
            |--------------|------|
            | Diesel, Petrol & LPG | ml/m i.e., milliliters per meter|
            | CNG | gm/m i.e., grams per meter|

            The function is linearly interpolated between data points. For speeds less than `SPEED_0`
            the value of the function is `CONSUMPTION_0`, and for speeds greater than `SPEED_N` the
            value of the function is `CONSUMPTION_N`.
             Example:
            0,0.2394,14,0.2394,36,0.2586,52,0.196,68,0.2074,83,0.238,95,0.2597,105,0.2597,115,0.2964,125,0.3367,135,0.3508.
        traffic_speed_table (str | Unset): Function curve specifying consumption rate at a given speed.

            The format of the string is a comma-separated list of numbers, as follows:

            ```
            <SPEED_0>,<CONSUMPTION_0>,<SPEED_1>,<CONSUMPTION_1>,...,<SPEED_N>,<CONSUMPTION_N>
            ```

            where speed values are strictly increasing, non-negative integers in units of (km/h), and
            consumption values are non-negative floating point values.

            * Unit for EV:
            | Vehicle Type | Unit |
            |--------------|------|
            | Electric | Wh/m i.e., Watt-hours per meter|

            * Units for Fuel-based vehicles:
            | Vehicle Type | Unit |
            |--------------|------|
            | Diesel, Petrol & LPG | ml/m i.e., milliliters per meter|
            | CNG | gm/m i.e., grams per meter|

            The function is linearly interpolated between data points. For speeds less than `SPEED_0`
            the value of the function is `CONSUMPTION_0`, and for speeds greater than `SPEED_N` the
            value of the function is `CONSUMPTION_N`.
             Example:
            0,0.2394,14,0.2394,36,0.2586,52,0.196,68,0.2074,83,0.238,95,0.2597,105,0.2597,115,0.2964,125,0.3367,135,0.3508.
        ascent (float | Unset): Rate of energy consumed per meter rise in elevation (in Wh/m, i.e., Watt-hours per
            meter).
        descent (float | Unset): Rate of energy recovered per meter fall in elevation (in Wh/m, i.e., Watt-hours per
            meter).
        auxiliary_consumption (float | Unset): Rate of energy (in Wh/s) consumed by the vehicle's auxiliary systems (for
            example, air conditioning, lights).
            The value represents the number of Watt-hours consumed per second of travel.
    """

    free_flow_speed_table: str
    traffic_speed_table: str | Unset = UNSET
    ascent: float | Unset = UNSET
    descent: float | Unset = UNSET
    auxiliary_consumption: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        free_flow_speed_table = self.free_flow_speed_table

        traffic_speed_table = self.traffic_speed_table

        ascent = self.ascent

        descent = self.descent

        auxiliary_consumption = self.auxiliary_consumption

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "freeFlowSpeedTable": free_flow_speed_table,
        })
        if traffic_speed_table is not UNSET:
            field_dict["trafficSpeedTable"] = traffic_speed_table
        if ascent is not UNSET:
            field_dict["ascent"] = ascent
        if descent is not UNSET:
            field_dict["descent"] = descent
        if auxiliary_consumption is not UNSET:
            field_dict["auxiliaryConsumption"] = auxiliary_consumption

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        free_flow_speed_table = d.pop("freeFlowSpeedTable")

        traffic_speed_table = d.pop("trafficSpeedTable", UNSET)

        ascent = d.pop("ascent", UNSET)

        descent = d.pop("descent", UNSET)

        auxiliary_consumption = d.pop("auxiliaryConsumption", UNSET)

        base_ev_empirical_model = cls(
            free_flow_speed_table=free_flow_speed_table,
            traffic_speed_table=traffic_speed_table,
            ascent=ascent,
            descent=descent,
            auxiliary_consumption=auxiliary_consumption,
        )

        base_ev_empirical_model.additional_properties = d
        return base_ev_empirical_model

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
