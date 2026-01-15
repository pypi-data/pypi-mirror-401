from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EVPhysicalModel")


@_attrs_define
class EVPhysicalModel:
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
        initial_charge (float | Unset): Charge level of the vehicle's battery at the start of the route (in kWh).
            Value must be less than or equal to the value of `maxCharge`.
        max_charge (float | Unset): Total capacity of the vehicle's battery (in kWh).
        charging_curve (str | Unset): Function curve describing the maximum battery charging rate (in kW) at a given
            charge level (in kWh).

            The format of the string is a comma-separated list of numbers, as follows:

            ```
            <CHARGE_0>,<RATE_0>,<CHARGE_1>,<RATE_1>,...,<RATE_N>,<CHARGE_N>
            ```

            where charge values are strictly increasing, non-negative floating-point values in units
            of (kWh), and rate values are positive floating point values in units of (kW).

            Charge values must cover the entire range of `[0, maxChargeAfterChargingStation`]. The
            charging curve is piecewise constant, e.g., for any charge in the range `[CHARGE_0,
            CHARGE_1)`, the value of the function is `RATE_0`.

            Maximum value of rate must not be greater than 2000 kW. The values of charge in the curve are only validated up
            to the value of `maxChargeAfterChargingStation` since values outside this range are not used.
            Minimum value of rate must not be less than 7kW. The values of charge in the curve are only validated up to the
            value of `maxChargeAfterChargingStation` since values outside this range are not used.

            The algorithm calculates a route as the best possible combination of driving and charging
            parts and uses the charging curve to evaluate the most efficent range of
            charging. For example, if the rate of charging is high at lower levels of battery, but slows down significantly
            after charging a little, stopping
            often and charging less, but quicker, at each station might be better for the overall route.
            Because batteries lose charging speed with use, providing a charging curve for the
            exact battery would give more accurate charging time estimate than providing a
            generic curve for all batteries of one type.
             Example: 0,207,28.761,207,29.011,173,43.493,173,43.743,145,51.209,145,51.459,113,56.120,113,56.370,87,80.0,10.
        max_charging_voltage (float | Unset): Maximum charging voltage supported by the vehicle's battery (in Volt).
        max_charging_current (float | Unset): Maximum charging current supported by the vehicle's battery (in Ampere).
        max_charge_after_charging_station (float | Unset): Maximum charge to which the battery should be charged at a
            charging station (in kWh).
            Value must be less than or equal to the value of `maxCharge`.

            The algorithm calculates a route as the best possible combination of driving and charging
            parts so charging at a charging station does not happen strictly to the value of
            this parameter. Instead, the algorithm attempts to leave every station with
            different charge levels, and only the best possible combination of charging stations
            and target charge will form the final route.

            For example, if there is a fast but not reachable charging station on the route,
            the algorithm prefers first to charge at a slower station, but only to a level that enables it
            to reach the fast station. This way it calculates the best possible combination of driving
            and charging parts.
        min_charge_at_charging_station (float | Unset): Minimum charge when arriving at a charging station (in kWh).
            Value must be less than the value of `maxChargeAfterChargingStation`.

            The algorithm calculates a route as the best possible combination of driving and charging
            parts so visiting a charging station is planned not when the remaining charge is close
            to the value of this parameter but when it is part of the best possible charging
            plan for the given route.

            For example, it might prefer charging a still half-full battery at the fast charging station because
            there are only slower stations later on the route and the remaining charge is not
            enough to reach the destination without charging at all.
        min_charge_at_first_charging_station (float | Unset): Minimum charge when arriving at first charging station (in
            kWh).
            Value must be less than the value of `maxChargeAfterChargingStation`.

            This overrides `minChargeAtChargingStation` for the first charging station. If not specified,
            `minChargeAtChargingStation`
            will be used for all charging stations, including the first one.

            This is usually used when the current charge is too low to reach a charging station within
            `minChargeAtChargingStation` limits.
        min_charge_at_destination (float | Unset): Minimum charge at the final route destination (in kWh).
            Value must be less than the value of `maxChargeAfterChargingStation`.

            The algorithm calculates a route as the best possible combination of driving and charging
            parts while making sure that the actual value of the charge at the destination would be close to the
            value of this parameter. I.e., the resulting value is expected to be bigger
            than this parameter's value by no more than 10% of the battery capacity.
        charging_setup_duration (int | Unset): Time spent (in seconds) after arriving at a charging station but before
            actually charging
            (for example, time spent for payment processing).
        max_charging_duration (int | Unset): Maximum time spent (in seconds) at a charging station unless otherwise
            specified in a user-introduced charging waypoint. Charging waypoint may
            specify max or min duration, both of which can be higher. (see documentation for the `via` parameter)
        connector_types (str | Unset): Comma-separated list of connector types that are compatible with the vehicle. If
            `makeReachable` is set to `true`,
            then only stations with any of these connector types will be evaluated as a potential charging stop.
            For stations with multiple compatible connectors, the charging time is based on the connector type with the
            highest power rating among them.

            Currently supported connector types are:
              * `iec62196Type1Combo`:  Type 1 Combo connector, commonly called "CCS1"
              * `iec62196Type2Combo`:  Type 2 Combo connector, commonly called "CCS2"
              * `chademo`: CHAdeMO connector
              * `tesla`: Deprecated alias for `saeJ3400`. Use `saeJ3400` instead. Cannot be used in combination with
            `saeJ3400`
              * `saeJ3400`: North American Charging Standard (NACS) connector.
              * `gbtDc`: Guobiao GB/T 20234.3 DC connector
             Example: iec62196Type1Combo,chademo.
        max_power_at_low_voltage (float | Unset): The maximum power (in kW) at which a vehicle can charge given these
            conditions:
            * The charging station connector's maximum supply voltage < 800 V.
            * The vehicle's `maxChargingVoltage` >= 800 V.

            The `consumablePower` at a station is then taken to be the lower of `maxPowerAtLowVoltage` and the charging
            station's available power.
             Default: 45.0.
    """

    drive_efficiency: float
    recuperation_efficiency: float
    auxiliary_power_consumption: float | Unset = UNSET
    air_density: float | Unset = 1.225
    auxiliary_power_curve: str | Unset = UNSET
    initial_charge: float | Unset = UNSET
    max_charge: float | Unset = UNSET
    charging_curve: str | Unset = UNSET
    max_charging_voltage: float | Unset = UNSET
    max_charging_current: float | Unset = UNSET
    max_charge_after_charging_station: float | Unset = UNSET
    min_charge_at_charging_station: float | Unset = UNSET
    min_charge_at_first_charging_station: float | Unset = UNSET
    min_charge_at_destination: float | Unset = UNSET
    charging_setup_duration: int | Unset = UNSET
    max_charging_duration: int | Unset = UNSET
    connector_types: str | Unset = UNSET
    max_power_at_low_voltage: float | Unset = 45.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        drive_efficiency = self.drive_efficiency

        recuperation_efficiency = self.recuperation_efficiency

        auxiliary_power_consumption = self.auxiliary_power_consumption

        air_density = self.air_density

        auxiliary_power_curve = self.auxiliary_power_curve

        initial_charge = self.initial_charge

        max_charge = self.max_charge

        charging_curve = self.charging_curve

        max_charging_voltage = self.max_charging_voltage

        max_charging_current = self.max_charging_current

        max_charge_after_charging_station = self.max_charge_after_charging_station

        min_charge_at_charging_station = self.min_charge_at_charging_station

        min_charge_at_first_charging_station = self.min_charge_at_first_charging_station

        min_charge_at_destination = self.min_charge_at_destination

        charging_setup_duration = self.charging_setup_duration

        max_charging_duration = self.max_charging_duration

        connector_types = self.connector_types

        max_power_at_low_voltage = self.max_power_at_low_voltage

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
        if initial_charge is not UNSET:
            field_dict["initialCharge"] = initial_charge
        if max_charge is not UNSET:
            field_dict["maxCharge"] = max_charge
        if charging_curve is not UNSET:
            field_dict["chargingCurve"] = charging_curve
        if max_charging_voltage is not UNSET:
            field_dict["maxChargingVoltage"] = max_charging_voltage
        if max_charging_current is not UNSET:
            field_dict["maxChargingCurrent"] = max_charging_current
        if max_charge_after_charging_station is not UNSET:
            field_dict["maxChargeAfterChargingStation"] = (
                max_charge_after_charging_station
            )
        if min_charge_at_charging_station is not UNSET:
            field_dict["minChargeAtChargingStation"] = min_charge_at_charging_station
        if min_charge_at_first_charging_station is not UNSET:
            field_dict["minChargeAtFirstChargingStation"] = (
                min_charge_at_first_charging_station
            )
        if min_charge_at_destination is not UNSET:
            field_dict["minChargeAtDestination"] = min_charge_at_destination
        if charging_setup_duration is not UNSET:
            field_dict["chargingSetupDuration"] = charging_setup_duration
        if max_charging_duration is not UNSET:
            field_dict["maxChargingDuration"] = max_charging_duration
        if connector_types is not UNSET:
            field_dict["connectorTypes"] = connector_types
        if max_power_at_low_voltage is not UNSET:
            field_dict["maxPowerAtLowVoltage"] = max_power_at_low_voltage

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        drive_efficiency = d.pop("driveEfficiency")

        recuperation_efficiency = d.pop("recuperationEfficiency")

        auxiliary_power_consumption = d.pop("auxiliaryPowerConsumption", UNSET)

        air_density = d.pop("airDensity", UNSET)

        auxiliary_power_curve = d.pop("auxiliaryPowerCurve", UNSET)

        initial_charge = d.pop("initialCharge", UNSET)

        max_charge = d.pop("maxCharge", UNSET)

        charging_curve = d.pop("chargingCurve", UNSET)

        max_charging_voltage = d.pop("maxChargingVoltage", UNSET)

        max_charging_current = d.pop("maxChargingCurrent", UNSET)

        max_charge_after_charging_station = d.pop(
            "maxChargeAfterChargingStation", UNSET
        )

        min_charge_at_charging_station = d.pop("minChargeAtChargingStation", UNSET)

        min_charge_at_first_charging_station = d.pop(
            "minChargeAtFirstChargingStation", UNSET
        )

        min_charge_at_destination = d.pop("minChargeAtDestination", UNSET)

        charging_setup_duration = d.pop("chargingSetupDuration", UNSET)

        max_charging_duration = d.pop("maxChargingDuration", UNSET)

        connector_types = d.pop("connectorTypes", UNSET)

        max_power_at_low_voltage = d.pop("maxPowerAtLowVoltage", UNSET)

        ev_physical_model = cls(
            drive_efficiency=drive_efficiency,
            recuperation_efficiency=recuperation_efficiency,
            auxiliary_power_consumption=auxiliary_power_consumption,
            air_density=air_density,
            auxiliary_power_curve=auxiliary_power_curve,
            initial_charge=initial_charge,
            max_charge=max_charge,
            charging_curve=charging_curve,
            max_charging_voltage=max_charging_voltage,
            max_charging_current=max_charging_current,
            max_charge_after_charging_station=max_charge_after_charging_station,
            min_charge_at_charging_station=min_charge_at_charging_station,
            min_charge_at_first_charging_station=min_charge_at_first_charging_station,
            min_charge_at_destination=min_charge_at_destination,
            charging_setup_duration=charging_setup_duration,
            max_charging_duration=max_charging_duration,
            connector_types=connector_types,
            max_power_at_low_voltage=max_power_at_low_voltage,
        )

        ev_physical_model.additional_properties = d
        return ev_physical_model

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
