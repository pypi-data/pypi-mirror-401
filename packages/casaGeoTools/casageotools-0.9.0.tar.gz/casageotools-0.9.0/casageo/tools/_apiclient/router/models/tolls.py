from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Tolls")


@_attrs_define
class Tolls:
    """Vehicle-independent options that may affect route toll calculation as well as options
    affecting the output of the tolls, such as summaries.

    Since this parameter controls behaviour related to tolls in the return part of the response,
    use of this parameter requires `return=tolls` to be selected.

        Attributes:
            transponders (str | Unset): Certain toll systems allow users to pay for the usage of the corresponding tollroads
                using transponders.
                As the price that the user pays with a transponder could be different from other payment methods for accessing
                the same toll roads
                this  is provided to allow the user to specify the transponders that they have.
                If a toll system requires a certain transponder to access it and the user states that they have it,
                the price for payment with transponders will be used when reporting fare prices
                and for summaries, if required by the `tolls[summaries]` parameter.

                The value of the parameter is a comma-separated list of transponder systems that the user has. Alternatively,
                the user can also specify `all` as a list element to state they have all required transponders along any
                potential route.

                **Note**: Currently, the only valid value is `all`.
            vignettes (str | Unset): This parameter allows the user to specify for which toll roads the user has valid
                vignettes.
                If a road requires a certain vignette and the user states that they have it, no notices will be
                given regarding the requirement to have it.

                The value of the parameter is a comma-separated list of vignettes that the user has. Alternatively,
                the user can also specify `all` as a list element to state they have all required vignettes along any potential
                route.

                No toll costs information will be returned for a given road requiring a vignette if the user states
                they already have it, as no further payment is necessary. If `tolls` are requested for spans, the toll
                sections for these types of toll systems are still reported, nevertheless.

                **Note**: Currently, the only valid value is `all`.
            summaries (list[str] | Unset): Items extensible enum: `total` `tollSystem` `country` `...`
                This parameter allows the user to specify criteria for tolls aggregation.
                Multiple values may be requested at once.
                Toll aggregation is performed at the section level only.

                Possible values are:
                  - `total`: the user wants a single value summarizing the tolls to be paid in the section.
                    This summary criterion requires that a `currency` has been passed as a parameter, to group
                    multi-currency roads together, even if the route would traverse roads that use only one currency;
                    see `currency` parameter.
                  - `tollSystem`: toll costs are aggregated per toll system.
                  - `country`: toll costs are aggregated per country.

                Note that any toll instance may have multiple prices, depending on factors such as time of day,
                payment methods, etc. that are not available in the request. As a result,
                the most economical value is selected for summary calculation, so summaries should be considered
                informative only.
            vehicle_category (str | Unset): Extensible enum: `minibus` `...`
                Defines special toll vehicle types. Usual types like car or truck are determined from transport mode.

                | category  | Description |
                | --------- | ------- |
                | minibus | Commercial buses with a seating capacity of 16-25 passengers (NA) or a small bus that is used to
                transport a maximum of 15 passengers. Can be used only with transport mode `car` |

                **NOTE:** It can be extended by other vehicle categories in the future.
            emission_type (str | Unset): Defines the emission types and CO2 emission classes as defined by the toll
                operator.
                The emission types defined are based on the Emission standards. Emission types are only published when the toll
                cost is defined based on emission type classes.

                ## Format

                Format: `EmissionType[CO2EmissionClass]`

                `EmissionType` is specified as `euro6`, `euro5`, etc. Allowed values are `[euro1, euro2, euro3, euro4, euro5,
                euro6, euroEev]`.

                `CO2EmissionClass` is optional and is specified as `;co2class=1`, `;co2class=2`, etc. Allowed values for
                `co2class` are `[1, 2, 3, 4, 5]`.

                ## Examples:

                Only toll emission type (euro6), without CO2 emission class: `euro6`

                Toll emission type (euro6) with CO2 emission class (class1): `euro6;co2class=1`

                **NOTES:**
                * This parameter is not compatible with EV routing. When EV routing is used (i.e., any `ev` namespace parameter
                is specified in the request or `vehicle[engineType]=electric` is specified), the appropriate emission type
                (Electric Vehicle) is used.
                * For cases other than EV routing: when not specified, `EmissionType` defaults to `euro5`. If `EmissionType` is
                provided without a `co2class`, then `co2class` defaults to `1`.
                * Providing only a `CO2EmissionClass` without an `EmissionType` is not supported, i.e. `euro6;co2class=1` is
                valid but `co2class=1` is invalid.
                * Providing an invalid combination of `EmissionType` and `CO2EmissionClass` as input may result in unexpected
                tolls.
                 Example: euro6.
    """

    transponders: str | Unset = UNSET
    vignettes: str | Unset = UNSET
    summaries: list[str] | Unset = UNSET
    vehicle_category: str | Unset = UNSET
    emission_type: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        transponders = self.transponders

        vignettes = self.vignettes

        summaries: list[str] | Unset = UNSET
        if not isinstance(self.summaries, Unset):
            summaries = self.summaries

        vehicle_category = self.vehicle_category

        emission_type = self.emission_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if transponders is not UNSET:
            field_dict["transponders"] = transponders
        if vignettes is not UNSET:
            field_dict["vignettes"] = vignettes
        if summaries is not UNSET:
            field_dict["summaries"] = summaries
        if vehicle_category is not UNSET:
            field_dict["vehicleCategory"] = vehicle_category
        if emission_type is not UNSET:
            field_dict["emissionType"] = emission_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        transponders = d.pop("transponders", UNSET)

        vignettes = d.pop("vignettes", UNSET)

        summaries = cast(list[str], d.pop("summaries", UNSET))

        vehicle_category = d.pop("vehicleCategory", UNSET)

        emission_type = d.pop("emissionType", UNSET)

        tolls = cls(
            transponders=transponders,
            vignettes=vignettes,
            summaries=summaries,
            vehicle_category=vehicle_category,
            emission_type=emission_type,
        )

        tolls.additional_properties = d
        return tolls

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
