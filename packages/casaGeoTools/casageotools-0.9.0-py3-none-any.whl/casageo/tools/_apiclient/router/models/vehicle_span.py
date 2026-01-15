from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.max_speed_type_1 import MaxSpeedType1
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dynamic_speed_info import DynamicSpeedInfo
    from ..models.localized_route_number import LocalizedRouteNumber
    from ..models.localized_string import LocalizedString


T = TypeVar("T", bound="VehicleSpan")


@_attrs_define
class VehicleSpan:
    r"""Span attached to a `Section` that describes the vehicle content.

    Attributes:
        offset (int | Unset): Offset of a coordinate in the section's polyline.
        length (int | Unset): Distance in meters. Example: 189.
        duration (int | Unset): Duration in seconds. Example: 198.
        street_attributes (list[str] | Unset): `StreetAttributes` is applied to a span of a route section and describes
            attribute flags of a street. The following flags can be assigned:
            * `rightDrivingSide`: Vehicles must drive on the right-hand side of the road in this part of the route.
            * `dirtRoad`: This part of the route has an unpaved surface, such as a gravel or dirt road.
            * `tunnel`: This part of the route passes through a tunnel.
            * `bridge`: This part of the route crosses a bridge.
            * `ramp`: This part of the route is a ramp, typically connecting to or from highways.
            * `motorway`: This part of the route is a controlled access road, typically a highway with motorway signage.
            * `roundabout`: This part of the route includes a roundabout.
            * `underConstruction`: This part of the route is currently under construction.
            * `dividedRoad`: This part of the route uses a road with a physical or legal divider in the middle, separating
            opposing traffic flows.
            * `privateRoad`: This part of the route uses a privately owned road.
            * `controlledAccessHighway`: This part of the route is either a controlled access road, limited access road, or
            both.
            * `builtUpArea`: This part of the route most likely passes through a built-up area.

            It is possible that new street-attributes may be supported in the future. When encountering unknown street-
            attributes, e.g., in the software parser, it is recommended to ignore them.
        walk_attributes (list[str] | Unset): The following attribute flags are used to describe accessibility and walk-
            related features along a route:

            * `stairs`: This part of the route includes a staircase that needs to be climbed or descended.
            * `park`: This part of the route is located within a park or park-like area.
            * `indoor`: This part of the route is inside a venue or building.
            * `open`: This part of the route is open and accessible for walking.
            * `noThrough`: This part of the route can only be traversed if the origin, destination, or any via waypoint is
            located there. In other words, it is not a through-route.
            * `tollRoad`: Access to this part of the route is restricted and requires the payment of a fee or toll.

            It is possible that new street-attributes may be supported in the future. When encountering unknown street-
            attributes, e.g., in the software parser, it is recommended to ignore them.
        car_attributes (list[str] | Unset): Car-specific `AccessAttributes`.

            `AccessAttributes` is applied to a span of a route section and describe access flags specific to cars. The
            following flags can be assigned:
            * `open`: This part of the route is open and accessible to cars.
            * `noThrough`: This part of the route can only be traversed by cars if the origin, destination, or any via
            waypoint is located there. It is not a through-route for cars.
            * `tollRoad`: This part of the route is a toll road, which means access is restricted for cars and requires the
            payment of a fee or toll.

            It is possible that new street-attributes may be supported in the future. When encountering unknown street-
            attributes, e.g., in the software parser, it is recommended to ignore them.
        truck_attributes (list[str] | Unset): Truck-specific `AccessAttributes`.

            `AccessAttributes` is applied to a span of a route section and describe access flags specific to trucks. These
            flags indicate the accessibility and restrictions for trucks along the route. The following flags can be
            assigned:
            * `open`: This part of the route is open and accessible to trucks.
            * `noThrough`: That this part of the route can only be traversed by trucks if the origin, destination, or any
            via waypoint is located there. It is not a through-route for trucks.
            * `tollRoad`: This part of the route is a toll road, which means access is restricted for trucks and requires
            the payment of a fee or toll.

            It is possible that new street-attributes may be supported in the future. When encountering unknown street-
            attributes, e.g., in the software parser, it is recommended to ignore them.
        scooter_attributes (list[str] | Unset): Scooter-specific `AccessAttributes`.

            `AccessAttributes` is applied to a span of a route section and describe access flags specific to scooters. These
            flags indicate the accessibility of streets for scooters along the route. The following flag can be assigned:
            * `open`: Indicates that this part of the route is open and accessible to scooters.

            It is possible that new street-attributes may be supported in the future. When encountering unknown street-
            attributes, e.g., in the software parser, it is recommended to ignore them.
        toll_systems (list[int] | Unset): The toll systems applicable to specific spans are described using an array of
            reference indexes. These indexes correspond to the `tollSystems` array in the enclosing section. Please note
            that toll information is not static and can vary based on factors such as transport-mode, time-of-day, etc.
            Therefore, the tolls applicable to a span may change in similar requests.
        names (list[LocalizedString] | Unset): Designated name for the span, e.g., a street name or a transport name.
        route_numbers (list[LocalizedRouteNumber] | Unset): Designated route name or number of the span, e.g., 'M25')
        country_code (str | Unset): ISO-3166-1 alpha-3 code Example: FRA.
        state_code (str | Unset): The second part of an ISO-3166-2 code (e.g., `TX` from `USA-TX`) consists of up to
            three alphanumeric characters.
            It is used to identify the principal subdivisions (e.g., provinces or states) of a country in conjunction with a
            CountryCode

            Note: State codes may not be available in some countries.
        functional_class (int | Unset): Functional class defines a hierarchical network used to determine a logical and
            efficient route. The following classifications are used:

            * `1`: Roads that allow for high volume, maximum speed traffic movement between and through major metropolitan
            areas.
            * `2`: Roads that are used to channel traffic to functional class 1 roads for travel between and through cities
            in the shortest amount of time.
            * `3`: Roads that intersect functional class 2 roads and provide a high volume of traffic movement at a lower
            level of mobility than functional class 2 roads.
            * `4`: Roads that provide for a high volume of traffic movement at moderate speeds between neighborhoods.
            * `5`: Roads with volume and traffic movement below the level of any other functional class.
        speed_limit (float | Unset): Speed in meters per second
        max_speed (float | MaxSpeedType1 | Unset): Speed in meters per second, or "unlimited" indicating that the speed
            is unlimited, e.g., on a German autobahn
        dynamic_speed_info (DynamicSpeedInfo | Unset): Describes dynamic speed information, such as traffic speed,
            estimated speed without traffic, and turn time.
        segment_id (str | Unset):
            **NOTE:** The attribute `segmentId` is deprecated and should be replaced with `segmentRef`.

            The directed topology segment id, including prefix, e.g., '+here:cm:segment:'. The id consists of two parts
            * The direction, represented by either '+' or '-'.
            * The topology segment id (a unique identifier within the HERE platform catalogs).

            The direction specifies whether the route is using the segment in its canonical direction ('+' also known as
            traveling along the geometry's direction), or against it ('-' also known as traveling against the geometry's
            direction).
        segment_ref (str | Unset): A reference to the HMC topology segment used in this span.

            The standard representation of a segment reference has the following structure:
            {catalogHrn}:{catalogVersion}:({layerId})?:{tileId}:{segmentId}(#{direction}({startOffset}..{endOffset})?)?

            The individual parts are:
            * catalogHrn: The HERE Resource Name that identifies the source catalog of the segment, example:
            hrn:here:data::olp-here:rib-2
            * catalogVersion: The catalog version
            * layerId (optional): The layer inside the catalog where the segment can be found, example: topology-geometry
            * tileId: The HERE tile key of the partition/tile where the segment is located in the given version of the
            catalog. This can be on a lower level than the actual segment is stored at (for example, the provided tile ID
            can be on level 14, despite topology-geometry partitions being tiled at level 12). The level of a HERE tile key
            is indicated by the position of the highest set bit in binary representation. Since the HERE tile key represents
            a morton code of the x and y portion of the Tile ID, the level 12 tile ID can be retrieved from the level 14
            tile ID by removing the 4 least significant bits (or 2 bits per level) or 1 hexadecimal digit. For example, the
            level 14 tile 377894441 is included in the level 12 tile 23618402 (377894441<sub>10</sub> =
            16863629<sub>16</sub> &rightarrow; 1686362<sub>16</sub> = 23618402<sub>10</sub>)
            * segmentId: The identifier of the referenced topology segment inside the catalog, example:
            here:cm:segment:84905195
            * direction (optional): Either '*' for undirected or bidirectional, '+' for positive direction, '-' for negative
            direction, or '?' for unknown direction (not used by the routing service)
            * startOffset/endOffset (optional): The start- and end offset are non-negative numbers between 0 and 1,
            representing the start and end of the referenced range using a proportion of the length of the segment. 0
            represents the start and 1 the end of the segment, relative to the indicated direction (or positive direction in
            case of undirected segments). Example: 0.7..1

            Example of a segment reference in standard representation:
            hrn:here:data::olp-here:rib-2:1363::377894441:here:cm:segment:84905195#+0.7..1

            The segment references can also be provided in a compact representation, to reduce the response size. In the
            compact representation, some parts are replaced by placeholders, which can be resolved using the refReplacements
            dictionary in the parent section.
            The placeholder format is ```\$\d+``` and needs to be surrounded by colons or string start/end. It can be
            captured with the following regular expression: ```(^|:)\$\d+(:|$)/``` .

            Example of the segment reference previously mentioned in compact representation:
            $0:377894441:$1:84905195#+0.7..1
            With the corresponding refReplacements:
            "refReplacements": {
              "0": "hrn:here:data::olp-here:rib-2:1363:",
              "1": "here:cm:segment"
            }
        consumption (float | Unset): Energy or fuel consumption.
            For EV energy consumption is in kilowatt hours (kWh). For fuel-based vehicles fuel consumption is in Liters (L)
            for diesel, petrol and LPG vehicles, and Kilograms (kg) for CNG vehicles.
        base_duration (int | Unset): Duration in seconds. Example: 198.
        typical_duration (int | Unset): Duration in seconds. Example: 198.
        incidents (list[int] | Unset): A list of indexes into the incident array of the parent section.
            References all incidents that apply to the span.
            This requires `incidents` to be specified as part of the `return` parameter.
        intersection_incidents (list[int] | Unset): A list of indexes in the incident array of the parent section.
            References all incidents that block movement through the intersection at the end of this span.
            This requires `incidents` to be specified in `return` and `spans` parameters.
        routing_zones (list[int] | Unset): A list of indexes into the routing zone array of the parent section.
            References all applicable routing zones to the span.
        truck_road_types (list[int] | Unset): A list of indexes into the truck road types array of the parent section.
            References all applicable truck road types to the span.
        gate (str | Unset): Extensible enum: `keyAccess` `permissionRequired` `emergency` `...`
            Type of gate crossing.
        railway_crossing (str | Unset): Extensible enum: `protected` `unprotected` `unknown` `...`
            Type of railway crossing.
        notices (list[int] | Unset): A list of indexes into the notices array of the parent section.
            References all notices that apply to the span.

            Depending on the notice type the notice might apply to the whole span, or only at the end of the span. Notices
            that only apply at the end of the span are:

            | Code      | Description  |
            | --------- | ------- |
            | violatedTurnRestriction | A restricted turn is performed at the end of the span |
            | violatedAvoidDifficultTurns | A difficult turn is performed at the end of the span |
            | violatedAvoidUTurns | A U-turn is performed at the end of the span |
            | violatedEmergencyGate | An emergency gate is crossed at the end of the span |
        no_through_restrictions (list[int] | Unset): A list of indexes into the `noThroughRestrictions` array of the
            parent section.
            References all `noThroughRestrictions` that apply to the span.
    """

    offset: int | Unset = UNSET
    length: int | Unset = UNSET
    duration: int | Unset = UNSET
    street_attributes: list[str] | Unset = UNSET
    walk_attributes: list[str] | Unset = UNSET
    car_attributes: list[str] | Unset = UNSET
    truck_attributes: list[str] | Unset = UNSET
    scooter_attributes: list[str] | Unset = UNSET
    toll_systems: list[int] | Unset = UNSET
    names: list[LocalizedString] | Unset = UNSET
    route_numbers: list[LocalizedRouteNumber] | Unset = UNSET
    country_code: str | Unset = UNSET
    state_code: str | Unset = UNSET
    functional_class: int | Unset = UNSET
    speed_limit: float | Unset = UNSET
    max_speed: float | MaxSpeedType1 | Unset = UNSET
    dynamic_speed_info: DynamicSpeedInfo | Unset = UNSET
    segment_id: str | Unset = UNSET
    segment_ref: str | Unset = UNSET
    consumption: float | Unset = UNSET
    base_duration: int | Unset = UNSET
    typical_duration: int | Unset = UNSET
    incidents: list[int] | Unset = UNSET
    intersection_incidents: list[int] | Unset = UNSET
    routing_zones: list[int] | Unset = UNSET
    truck_road_types: list[int] | Unset = UNSET
    gate: str | Unset = UNSET
    railway_crossing: str | Unset = UNSET
    notices: list[int] | Unset = UNSET
    no_through_restrictions: list[int] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offset = self.offset

        length = self.length

        duration = self.duration

        street_attributes: list[str] | Unset = UNSET
        if not isinstance(self.street_attributes, Unset):
            street_attributes = self.street_attributes

        walk_attributes: list[str] | Unset = UNSET
        if not isinstance(self.walk_attributes, Unset):
            walk_attributes = self.walk_attributes

        car_attributes: list[str] | Unset = UNSET
        if not isinstance(self.car_attributes, Unset):
            car_attributes = self.car_attributes

        truck_attributes: list[str] | Unset = UNSET
        if not isinstance(self.truck_attributes, Unset):
            truck_attributes = self.truck_attributes

        scooter_attributes: list[str] | Unset = UNSET
        if not isinstance(self.scooter_attributes, Unset):
            scooter_attributes = self.scooter_attributes

        toll_systems: list[int] | Unset = UNSET
        if not isinstance(self.toll_systems, Unset):
            toll_systems = self.toll_systems

        names: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.names, Unset):
            names = []
            for names_item_data in self.names:
                names_item = names_item_data.to_dict()
                names.append(names_item)

        route_numbers: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.route_numbers, Unset):
            route_numbers = []
            for route_numbers_item_data in self.route_numbers:
                route_numbers_item = route_numbers_item_data.to_dict()
                route_numbers.append(route_numbers_item)

        country_code = self.country_code

        state_code = self.state_code

        functional_class = self.functional_class

        speed_limit = self.speed_limit

        max_speed: float | str | Unset
        if isinstance(self.max_speed, Unset):
            max_speed = UNSET
        elif isinstance(self.max_speed, MaxSpeedType1):
            max_speed = self.max_speed.value
        else:
            max_speed = self.max_speed

        dynamic_speed_info: dict[str, Any] | Unset = UNSET
        if not isinstance(self.dynamic_speed_info, Unset):
            dynamic_speed_info = self.dynamic_speed_info.to_dict()

        segment_id = self.segment_id

        segment_ref = self.segment_ref

        consumption = self.consumption

        base_duration = self.base_duration

        typical_duration = self.typical_duration

        incidents: list[int] | Unset = UNSET
        if not isinstance(self.incidents, Unset):
            incidents = self.incidents

        intersection_incidents: list[int] | Unset = UNSET
        if not isinstance(self.intersection_incidents, Unset):
            intersection_incidents = self.intersection_incidents

        routing_zones: list[int] | Unset = UNSET
        if not isinstance(self.routing_zones, Unset):
            routing_zones = self.routing_zones

        truck_road_types: list[int] | Unset = UNSET
        if not isinstance(self.truck_road_types, Unset):
            truck_road_types = self.truck_road_types

        gate = self.gate

        railway_crossing = self.railway_crossing

        notices: list[int] | Unset = UNSET
        if not isinstance(self.notices, Unset):
            notices = self.notices

        no_through_restrictions: list[int] | Unset = UNSET
        if not isinstance(self.no_through_restrictions, Unset):
            no_through_restrictions = self.no_through_restrictions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if offset is not UNSET:
            field_dict["offset"] = offset
        if length is not UNSET:
            field_dict["length"] = length
        if duration is not UNSET:
            field_dict["duration"] = duration
        if street_attributes is not UNSET:
            field_dict["streetAttributes"] = street_attributes
        if walk_attributes is not UNSET:
            field_dict["walkAttributes"] = walk_attributes
        if car_attributes is not UNSET:
            field_dict["carAttributes"] = car_attributes
        if truck_attributes is not UNSET:
            field_dict["truckAttributes"] = truck_attributes
        if scooter_attributes is not UNSET:
            field_dict["scooterAttributes"] = scooter_attributes
        if toll_systems is not UNSET:
            field_dict["tollSystems"] = toll_systems
        if names is not UNSET:
            field_dict["names"] = names
        if route_numbers is not UNSET:
            field_dict["routeNumbers"] = route_numbers
        if country_code is not UNSET:
            field_dict["countryCode"] = country_code
        if state_code is not UNSET:
            field_dict["stateCode"] = state_code
        if functional_class is not UNSET:
            field_dict["functionalClass"] = functional_class
        if speed_limit is not UNSET:
            field_dict["speedLimit"] = speed_limit
        if max_speed is not UNSET:
            field_dict["maxSpeed"] = max_speed
        if dynamic_speed_info is not UNSET:
            field_dict["dynamicSpeedInfo"] = dynamic_speed_info
        if segment_id is not UNSET:
            field_dict["segmentId"] = segment_id
        if segment_ref is not UNSET:
            field_dict["segmentRef"] = segment_ref
        if consumption is not UNSET:
            field_dict["consumption"] = consumption
        if base_duration is not UNSET:
            field_dict["baseDuration"] = base_duration
        if typical_duration is not UNSET:
            field_dict["typicalDuration"] = typical_duration
        if incidents is not UNSET:
            field_dict["incidents"] = incidents
        if intersection_incidents is not UNSET:
            field_dict["intersectionIncidents"] = intersection_incidents
        if routing_zones is not UNSET:
            field_dict["routingZones"] = routing_zones
        if truck_road_types is not UNSET:
            field_dict["truckRoadTypes"] = truck_road_types
        if gate is not UNSET:
            field_dict["gate"] = gate
        if railway_crossing is not UNSET:
            field_dict["railwayCrossing"] = railway_crossing
        if notices is not UNSET:
            field_dict["notices"] = notices
        if no_through_restrictions is not UNSET:
            field_dict["noThroughRestrictions"] = no_through_restrictions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dynamic_speed_info import DynamicSpeedInfo
        from ..models.localized_route_number import LocalizedRouteNumber
        from ..models.localized_string import LocalizedString

        d = dict(src_dict)
        offset = d.pop("offset", UNSET)

        length = d.pop("length", UNSET)

        duration = d.pop("duration", UNSET)

        street_attributes = cast(list[str], d.pop("streetAttributes", UNSET))

        walk_attributes = cast(list[str], d.pop("walkAttributes", UNSET))

        car_attributes = cast(list[str], d.pop("carAttributes", UNSET))

        truck_attributes = cast(list[str], d.pop("truckAttributes", UNSET))

        scooter_attributes = cast(list[str], d.pop("scooterAttributes", UNSET))

        toll_systems = cast(list[int], d.pop("tollSystems", UNSET))

        _names = d.pop("names", UNSET)
        names: list[LocalizedString] | Unset = UNSET
        if _names is not UNSET:
            names = []
            for names_item_data in _names:
                names_item = LocalizedString.from_dict(names_item_data)

                names.append(names_item)

        _route_numbers = d.pop("routeNumbers", UNSET)
        route_numbers: list[LocalizedRouteNumber] | Unset = UNSET
        if _route_numbers is not UNSET:
            route_numbers = []
            for route_numbers_item_data in _route_numbers:
                route_numbers_item = LocalizedRouteNumber.from_dict(
                    route_numbers_item_data
                )

                route_numbers.append(route_numbers_item)

        country_code = d.pop("countryCode", UNSET)

        state_code = d.pop("stateCode", UNSET)

        functional_class = d.pop("functionalClass", UNSET)

        speed_limit = d.pop("speedLimit", UNSET)

        def _parse_max_speed(data: object) -> float | MaxSpeedType1 | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                componentsschemas_max_speed_type_1 = MaxSpeedType1(data)

                return componentsschemas_max_speed_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(float | MaxSpeedType1 | Unset, data)

        max_speed = _parse_max_speed(d.pop("maxSpeed", UNSET))

        _dynamic_speed_info = d.pop("dynamicSpeedInfo", UNSET)
        dynamic_speed_info: DynamicSpeedInfo | Unset
        if isinstance(_dynamic_speed_info, Unset):
            dynamic_speed_info = UNSET
        else:
            dynamic_speed_info = DynamicSpeedInfo.from_dict(_dynamic_speed_info)

        segment_id = d.pop("segmentId", UNSET)

        segment_ref = d.pop("segmentRef", UNSET)

        consumption = d.pop("consumption", UNSET)

        base_duration = d.pop("baseDuration", UNSET)

        typical_duration = d.pop("typicalDuration", UNSET)

        incidents = cast(list[int], d.pop("incidents", UNSET))

        intersection_incidents = cast(list[int], d.pop("intersectionIncidents", UNSET))

        routing_zones = cast(list[int], d.pop("routingZones", UNSET))

        truck_road_types = cast(list[int], d.pop("truckRoadTypes", UNSET))

        gate = d.pop("gate", UNSET)

        railway_crossing = d.pop("railwayCrossing", UNSET)

        notices = cast(list[int], d.pop("notices", UNSET))

        no_through_restrictions = cast(list[int], d.pop("noThroughRestrictions", UNSET))

        vehicle_span = cls(
            offset=offset,
            length=length,
            duration=duration,
            street_attributes=street_attributes,
            walk_attributes=walk_attributes,
            car_attributes=car_attributes,
            truck_attributes=truck_attributes,
            scooter_attributes=scooter_attributes,
            toll_systems=toll_systems,
            names=names,
            route_numbers=route_numbers,
            country_code=country_code,
            state_code=state_code,
            functional_class=functional_class,
            speed_limit=speed_limit,
            max_speed=max_speed,
            dynamic_speed_info=dynamic_speed_info,
            segment_id=segment_id,
            segment_ref=segment_ref,
            consumption=consumption,
            base_duration=base_duration,
            typical_duration=typical_duration,
            incidents=incidents,
            intersection_incidents=intersection_incidents,
            routing_zones=routing_zones,
            truck_road_types=truck_road_types,
            gate=gate,
            railway_crossing=railway_crossing,
            notices=notices,
            no_through_restrictions=no_through_restrictions,
        )

        vehicle_span.additional_properties = d
        return vehicle_span

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
