from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BaseEVPhysicalModel")


@_attrs_define
class BaseEVPhysicalModel:
    """Specifies parameters required for calculation of energy consumption for electric vehicles using physical model.

    Attributes:
        drive_efficiency (float): The proportion of the energy drawn from the battery that is used to move the vehicle.
            (This is to factor in energy losses through heat in the motors, for example.)
            **Note:** This attribute is required when using the physical model `consumptionModel=physical` for EV
            consumption.

            **Alpha**: This parameter is in development. It may not be stable and is subject to change.
        recuperation_efficiency (float): The proportion of the energy gained when braking or going downhill that can be
            recuperated and restored as battery charge.
            **Note:** This attribute is required when using the physical model `consumptionModel=physical` for EV
            consumption.

            **Alpha**: This parameter is in development. It may not be stable and is subject to change.
        auxiliary_power_consumption (float | Unset): Power (in W) consumed by the vehicle's auxiliary systems (for
            example, air conditioning, lights).

            **Alpha**: This parameter is in development. It may not be stable and is subject to change.
        air_density (float | Unset): The density of air (in kg/m³) used for calculating aerodynamic drag.

            **Alpha**: This parameter is in development. It may not be stable and is subject to change.
             Default: 1.225.
        auxiliary_power_curve (str | Unset): Function curve specifying power consumed by the vehicle's auxiliary systems
            as a function of time.
            Use this instead of the single-valued `auxiliaryPowerConsumption` when auxiliary power consumption is not
            constant.

            The format of the string is a pipe separated list of number pairs, as follows:

            ```
            <TIME_0>,<POWER_0>|<TIME_1>,<POWER_1>|...|<TIME_N>,<POWER_N>
            ```

            where time values are strictly increasing non-negative integer values in seconds, representing elapsed driving
            time since the start of the route, and power values are non-negative floating point values in watts.
            The function is piecewise constant, e.g., for any elapsed time in the range `[TIME_0, TIME_1]` the value of the
            function is `POWER_0`.
            For time greater than `TIME_N`, the value of the function is `POWER_N`. TIME_0 must be explicitly set to zero.
            The time in the last pair, `TIME_N`, can be at most 1800 (30 minutes).

            Waypoint waiting times, setup times or anything other than driving time does not
            cause power consumption but function curve keeps advancing.

            The list can have a maximum of six `TIME`,`POWER` pairs.

            **Note**: When using this feature `departureTime` needs to be set and cannot be set to `any`.

            **Alpha**: This parameter is in development. It may not be stable and is subject to change.
    """

    drive_efficiency: float
    recuperation_efficiency: float
    auxiliary_power_consumption: float | Unset = UNSET
    air_density: float | Unset = 1.225
    auxiliary_power_curve: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        drive_efficiency = self.drive_efficiency

        recuperation_efficiency = self.recuperation_efficiency

        auxiliary_power_consumption = self.auxiliary_power_consumption

        air_density = self.air_density

        auxiliary_power_curve = self.auxiliary_power_curve

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "driveEfficiency": drive_efficiency,
            "recuperationEfficiency": recuperation_efficiency,
        })
        if auxiliary_power_consumption is not UNSET:
            field_dict["auxiliaryPowerConsumption"] = auxiliary_power_consumption
        if air_density is not UNSET:
            field_dict["airDensity"] = air_density
        if auxiliary_power_curve is not UNSET:
            field_dict["auxiliaryPowerCurve"] = auxiliary_power_curve

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        drive_efficiency = d.pop("driveEfficiency")

        recuperation_efficiency = d.pop("recuperationEfficiency")

        auxiliary_power_consumption = d.pop("auxiliaryPowerConsumption", UNSET)

        air_density = d.pop("airDensity", UNSET)

        auxiliary_power_curve = d.pop("auxiliaryPowerCurve", UNSET)

        base_ev_physical_model = cls(
            drive_efficiency=drive_efficiency,
            recuperation_efficiency=recuperation_efficiency,
            auxiliary_power_consumption=auxiliary_power_consumption,
            air_density=air_density,
            auxiliary_power_curve=auxiliary_power_curve,
        )

        base_ev_physical_model.additional_properties = d
        return base_ev_physical_model

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
