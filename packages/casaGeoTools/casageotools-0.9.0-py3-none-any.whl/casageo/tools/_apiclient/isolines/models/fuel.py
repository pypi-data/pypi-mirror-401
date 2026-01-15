from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Fuel")


@_attrs_define
class Fuel:
    """Fuel parameters to be used for calculating consumption and consumption-based isolines for fuel-based vehicles
    using empirical consumption model.

    Attributes:
    * `type`
    * `freeFlowSpeedTable`
    * `trafficSpeedTable`
    * `additionalConsumption`
    * `ascent`

        Attributes:
            type_ (str): Extensible enum: `diesel` `petrol` `lpg` `cng` `lng` `ethanol` `propane` `hydrogen` `...`
                Vehicle fuel type. It is mandatory for calculation of consumption and CO2 emission.
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
            additional_consumption (float | Unset): Rate of fuel (in ml/s for diesel, petrol & LPG, gm/s for CNG) consumed
                by the vehicle for any other reason
                additional to fuel consumption for speed.
            ascent (float | Unset): Rate of fuel consumed per meter rise in elevation (in ml/m for diesel, petrol & LPG,
                gm/m for CNG).
    """

    type_: str
    free_flow_speed_table: str
    traffic_speed_table: str | Unset = UNSET
    additional_consumption: float | Unset = UNSET
    ascent: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        free_flow_speed_table = self.free_flow_speed_table

        traffic_speed_table = self.traffic_speed_table

        additional_consumption = self.additional_consumption

        ascent = self.ascent

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "freeFlowSpeedTable": free_flow_speed_table,
        })
        if traffic_speed_table is not UNSET:
            field_dict["trafficSpeedTable"] = traffic_speed_table
        if additional_consumption is not UNSET:
            field_dict["additionalConsumption"] = additional_consumption
        if ascent is not UNSET:
            field_dict["ascent"] = ascent

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        free_flow_speed_table = d.pop("freeFlowSpeedTable")

        traffic_speed_table = d.pop("trafficSpeedTable", UNSET)

        additional_consumption = d.pop("additionalConsumption", UNSET)

        ascent = d.pop("ascent", UNSET)

        fuel = cls(
            type_=type_,
            free_flow_speed_table=free_flow_speed_table,
            traffic_speed_table=traffic_speed_table,
            additional_consumption=additional_consumption,
            ascent=ascent,
        )

        fuel.additional_properties = d
        return fuel

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
