from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.violated_zone_reference_type import ViolatedZoneReferenceType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.license_plate_restriction import LicensePlateRestriction
    from ..models.vehicle_restriction_max_weight import VehicleRestrictionMaxWeight


T = TypeVar("T", bound="ViolatedZoneReference")


@_attrs_define
class ViolatedZoneReference:
    r"""Provides details about the zone associated with `violatedZoneRestriction` and
    the violated restriction conditions that were evaluated against parameter values
    set in the routing request (such as vehicle properties).

    The restriction is violated only if all of the conditions present are met.

        Attributes:
            type_ (ViolatedZoneReferenceType): Detail type. Each type of detail might contain extra attributes.

                **NOTE:** The list of possible detail types may be extended in the future.
                The client application is expected to handle such a case gracefully.
            title (str | Unset): Detail title
            cause (str | Unset): Cause of the notice
            routing_zone_ref (str | Unset): A reference to a routing zone in HMC.

                The standard representation of a routing zone reference has the following structure:
                `{catalogHrn}:{catalogVersion}:({layerId})?:{tileId}:{zoneId}`

                The individual parts are:
                * `catalogHrn`: The HERE Resource Name that identifies the source catalog of the routing zone, example:
                `hrn:here:data::olp-here:rib-2`
                * `catalogVersion`: The catalog version
                * `layerId` (optional): The layer inside the catalog where the routing zone is located, example: `environmental-
                zones`
                * `tileId`: The HERE tile key of the partition/tile where the routing zone is located in the given version of
                the catalog
                * `zoneId`: The identifier of the referenced routing zone within the catalog, example: `here:cm:envzone:3455277`

                Example of a reference to an environmental zone in standard form:
                `hrn:here:data::olp-here:rib-2:1557:environmental-zones:all:here:cm:envzone:3455277`

                In order to reduce response size, routing zone references can also be provided in a compact representation.
                In compact form, parts of a reference are replaced by placeholders, which can be resolved using the
                `refReplacements` dictionary in the parent section.
                The placeholder format is ```\$\d+``` and needs to be surrounded by colons or string start/end. It can be
                captured with the following regular expression: ```(^|:)\$\d+(:|$)``` .

                Example of the aforementioned environmental zone reference in compact form: `$0:$1:3455277`
                With the corresponding `refReplacements`:
                ```
                "refReplacements": {
                  "0": "hrn:here:data::olp-here:rib-2:1557",
                  "1": "environmental-zones:all:here:cm:envzone"
                }
                ```
            time_dependent (bool | Unset): Indicates if the violation is time-dependent
            restricted_times (str | Unset): Specifies date and time period during which the restriction applies. Value is a
                string in the Time
                Domain format. Time Domain is part of the GDF (Geographic Data Files) specification, which is an ISO standard.
                Current standard is GDF 5.1 which is [ISO 20524-1:2020](https://www.iso.org/standard/68244.html).

                For a detailed description of the Time Domain specification and usage in routing services, please refer to
                the documentation available in the [Time Domain](https://www.here.com/docs/bundle/routing-api-developer-
                guide-v8/page/concepts/time-domain.html) page of the Developer Guide.
                 Example: -(d1){w1}(d3){d1}.
            license_plate_restriction (LicensePlateRestriction | Unset): Contains details of the violated license plate
                restriction.
            max_weight (VehicleRestrictionMaxWeight | Unset): Contains the maximum permitted weight, specified in kilograms,
                along with the specific type of the maximum permitted weight restriction.
    """

    type_: ViolatedZoneReferenceType
    title: str | Unset = UNSET
    cause: str | Unset = UNSET
    routing_zone_ref: str | Unset = UNSET
    time_dependent: bool | Unset = UNSET
    restricted_times: str | Unset = UNSET
    license_plate_restriction: LicensePlateRestriction | Unset = UNSET
    max_weight: VehicleRestrictionMaxWeight | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        title = self.title

        cause = self.cause

        routing_zone_ref = self.routing_zone_ref

        time_dependent = self.time_dependent

        restricted_times = self.restricted_times

        license_plate_restriction: dict[str, Any] | Unset = UNSET
        if not isinstance(self.license_plate_restriction, Unset):
            license_plate_restriction = self.license_plate_restriction.to_dict()

        max_weight: dict[str, Any] | Unset = UNSET
        if not isinstance(self.max_weight, Unset):
            max_weight = self.max_weight.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
        })
        if title is not UNSET:
            field_dict["title"] = title
        if cause is not UNSET:
            field_dict["cause"] = cause
        if routing_zone_ref is not UNSET:
            field_dict["routingZoneRef"] = routing_zone_ref
        if time_dependent is not UNSET:
            field_dict["timeDependent"] = time_dependent
        if restricted_times is not UNSET:
            field_dict["restrictedTimes"] = restricted_times
        if license_plate_restriction is not UNSET:
            field_dict["licensePlateRestriction"] = license_plate_restriction
        if max_weight is not UNSET:
            field_dict["maxWeight"] = max_weight

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.license_plate_restriction import LicensePlateRestriction
        from ..models.vehicle_restriction_max_weight import VehicleRestrictionMaxWeight

        d = dict(src_dict)
        type_ = ViolatedZoneReferenceType(d.pop("type"))

        title = d.pop("title", UNSET)

        cause = d.pop("cause", UNSET)

        routing_zone_ref = d.pop("routingZoneRef", UNSET)

        time_dependent = d.pop("timeDependent", UNSET)

        restricted_times = d.pop("restrictedTimes", UNSET)

        _license_plate_restriction = d.pop("licensePlateRestriction", UNSET)
        license_plate_restriction: LicensePlateRestriction | Unset
        if isinstance(_license_plate_restriction, Unset):
            license_plate_restriction = UNSET
        else:
            license_plate_restriction = LicensePlateRestriction.from_dict(
                _license_plate_restriction
            )

        _max_weight = d.pop("maxWeight", UNSET)
        max_weight: VehicleRestrictionMaxWeight | Unset
        if isinstance(_max_weight, Unset):
            max_weight = UNSET
        else:
            max_weight = VehicleRestrictionMaxWeight.from_dict(_max_weight)

        violated_zone_reference = cls(
            type_=type_,
            title=title,
            cause=cause,
            routing_zone_ref=routing_zone_ref,
            time_dependent=time_dependent,
            restricted_times=restricted_times,
            license_plate_restriction=license_plate_restriction,
            max_weight=max_weight,
        )

        violated_zone_reference.additional_properties = d
        return violated_zone_reference

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
