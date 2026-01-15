from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.hazardous_goods_restriction_any import HazardousGoodsRestrictionAny
from ..models.truck_type import TruckType
from ..models.tunnel_category import TunnelCategory
from ..models.vehicle_restriction_type import VehicleRestrictionType
from ..models.vehicle_type import VehicleType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.axle_group_weight import AxleGroupWeight
    from ..models.trailer_count_range import TrailerCountRange
    from ..models.truck_axle_count_range import TruckAxleCountRange
    from ..models.vehicle_restriction_max_weight import VehicleRestrictionMaxWeight


T = TypeVar("T", bound="VehicleRestriction")


@_attrs_define
class VehicleRestriction:
    """Provides details about the violated restriction and the violated restriction
    conditions that were evaluated against parameter values set in the routing
    request (such as vehicle properties).

    The restriction is violated only if all of the conditions present are met.

        Example:
            {'$ref': '#/components/examples/restrictionExample'}

        Attributes:
            type_ (VehicleRestrictionType): Detail type. Each type of detail might contain extra attributes.

                **NOTE:** The list of possible detail types may be extended in the future.
                The client application is expected to handle such a case gracefully.
            title (str | Unset): Detail title
            cause (str | Unset): Cause of the notice
            forbidden_hazardous_goods (HazardousGoodsRestrictionAny | list[str] | Unset):
            max_weight (VehicleRestrictionMaxWeight | Unset): Contains the maximum permitted weight, specified in kilograms,
                along with the specific type of the maximum permitted weight restriction.
            max_gross_weight (int | Unset): Contains the maximum permitted weight, specified in kilograms.
                This condition is met when the vehicle's weight exceeds the specified value.

                **NOTE:** This attribute is deprecated, use `maxWeight` instead. It is redundant and is present because of
                backward compatibility reasons.
            max_weight_per_axle (int | Unset): Contains the maximum permitted weight per axle, specified in kilograms.

                This condition is met when the vehicle's `weightPerAxle` exceeds the specified value.
            max_axle_group_weight (AxleGroupWeight | Unset): Contains the maximum allowed weight for an axle-group.
            max_height (int | Unset): Contains the maximum permitted height, specified in centimeters.

                This condition is met when the vehicle's `height` exceeds the specified value.
            max_width (int | Unset): Contains the maximum permitted width, specified in centimeters.

                This condition is met when the vehicle's `width` exceeds the specified value.
            max_length (int | Unset): Contains the maximum permitted length, specified in centimeters.

                This condition is met when the vehicle's `length` exceeds the specified value.
            max_tires_count (int | Unset): Contains the maximum number of permitted tires.

                This condition is met when the vehicle's `tiresCount` exceeds the specified value.
            axle_count (TruckAxleCountRange | Unset): Constrains the restriction to trucks with the number of axles within
                the specified range.
            tunnel_category (TunnelCategory | Unset): Specifies the tunnel category used to restrict the transport of
                specific goods.
            time_dependent (bool | Unset): Indicates that the restriction depends on time.
            truck_type (TruckType | Unset): Specifies the type of the truck

                * `Straight`: A truck on a single frame with a permanently attached cargo area.
                * `Tractor`: A towing vehicle that can pull one or more semi-trailers (also known as a semi-truck).
            vehicle_type (VehicleType | Unset): Specifies the type of the vehicle

                * `StraightTruck`: A truck on a single frame with a permanently attached cargo area. **Note:**
                default value when truck routing mode is used.
                * `Tractor`: A towing vehicle that can pull one or more semi-trailers (also known as a semi-truck).

                **Limitations:** only valid for `transportMode=truck`.
            trailer_count (TrailerCountRange | Unset): Constrains the restriction to vehicles with the number of trailers
                within the specified range.
            max_engine_size_cc (int | Unset): Contains the maximum permitted size of the engine, specified in cubic
                centimeters.

                This condition is met when the vehicle's `engineSizeCC` exceeds the specified value.
            min_engine_size_cc (int | Unset): Contains the minimum permitted size of the engine, specified in cubic
                centimeters.

                This condition is met when the vehicle's `engineSizeCC' is less than the specified value.
            max_occupancy (int | Unset): Contains the maximum permitted occupancy.

                This condition is met when the vehicle's `occupancy` exceeds the specified value.
            min_occupancy (int | Unset): Contains the minimum permitted occupancy.

                This condition is met when the vehicle's `occupancy` is less than the specified value.
            restricted_times (str | Unset): Specifies date and time period during which the restriction applies. Value is a
                string in the Time
                Domain format. Time Domain is part of the GDF (Geographic Data Files) specification, which is an ISO standard.
                Current standard is GDF 5.1 which is [ISO 20524-1:2020](https://www.iso.org/standard/68244.html).

                For a detailed description of the Time Domain specification and usage in routing services, please refer to
                the documentation available in the [Time Domain](https://www.here.com/docs/bundle/routing-api-developer-
                guide-v8/page/concepts/time-domain.html) page of the Developer Guide.
                 Example: -(d1){w1}(d3){d1}.
            max_kpra_length (int | Unset): Contains max permitted kingpin to rear axle length, in centimeters.

                This condition is met when the vehicle's `kpraLength` exceeds this value.
            max_payload_capacity (int | Unset): Contains the maximum allowed payload capacity, specified in kilograms.

                This condition is met when the vehicle's `payloadCapacity` exceeds the specified value.
            unconditional (bool | Unset): Restriction applies unconditionally. Default: False.
    """

    type_: VehicleRestrictionType
    title: str | Unset = UNSET
    cause: str | Unset = UNSET
    forbidden_hazardous_goods: HazardousGoodsRestrictionAny | list[str] | Unset = UNSET
    max_weight: VehicleRestrictionMaxWeight | Unset = UNSET
    max_gross_weight: int | Unset = UNSET
    max_weight_per_axle: int | Unset = UNSET
    max_axle_group_weight: AxleGroupWeight | Unset = UNSET
    max_height: int | Unset = UNSET
    max_width: int | Unset = UNSET
    max_length: int | Unset = UNSET
    max_tires_count: int | Unset = UNSET
    axle_count: TruckAxleCountRange | Unset = UNSET
    tunnel_category: TunnelCategory | Unset = UNSET
    time_dependent: bool | Unset = UNSET
    truck_type: TruckType | Unset = UNSET
    vehicle_type: VehicleType | Unset = UNSET
    trailer_count: TrailerCountRange | Unset = UNSET
    max_engine_size_cc: int | Unset = UNSET
    min_engine_size_cc: int | Unset = UNSET
    max_occupancy: int | Unset = UNSET
    min_occupancy: int | Unset = UNSET
    restricted_times: str | Unset = UNSET
    max_kpra_length: int | Unset = UNSET
    max_payload_capacity: int | Unset = UNSET
    unconditional: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        title = self.title

        cause = self.cause

        forbidden_hazardous_goods: list[str] | str | Unset
        if isinstance(self.forbidden_hazardous_goods, Unset):
            forbidden_hazardous_goods = UNSET
        elif isinstance(self.forbidden_hazardous_goods, HazardousGoodsRestrictionAny):
            forbidden_hazardous_goods = self.forbidden_hazardous_goods.value
        else:
            forbidden_hazardous_goods = self.forbidden_hazardous_goods

        max_weight: dict[str, Any] | Unset = UNSET
        if not isinstance(self.max_weight, Unset):
            max_weight = self.max_weight.to_dict()

        max_gross_weight = self.max_gross_weight

        max_weight_per_axle = self.max_weight_per_axle

        max_axle_group_weight: dict[str, Any] | Unset = UNSET
        if not isinstance(self.max_axle_group_weight, Unset):
            max_axle_group_weight = self.max_axle_group_weight.to_dict()

        max_height = self.max_height

        max_width = self.max_width

        max_length = self.max_length

        max_tires_count = self.max_tires_count

        axle_count: dict[str, Any] | Unset = UNSET
        if not isinstance(self.axle_count, Unset):
            axle_count = self.axle_count.to_dict()

        tunnel_category: str | Unset = UNSET
        if not isinstance(self.tunnel_category, Unset):
            tunnel_category = self.tunnel_category.value

        time_dependent = self.time_dependent

        truck_type: str | Unset = UNSET
        if not isinstance(self.truck_type, Unset):
            truck_type = self.truck_type.value

        vehicle_type: str | Unset = UNSET
        if not isinstance(self.vehicle_type, Unset):
            vehicle_type = self.vehicle_type.value

        trailer_count: dict[str, Any] | Unset = UNSET
        if not isinstance(self.trailer_count, Unset):
            trailer_count = self.trailer_count.to_dict()

        max_engine_size_cc = self.max_engine_size_cc

        min_engine_size_cc = self.min_engine_size_cc

        max_occupancy = self.max_occupancy

        min_occupancy = self.min_occupancy

        restricted_times = self.restricted_times

        max_kpra_length = self.max_kpra_length

        max_payload_capacity = self.max_payload_capacity

        unconditional = self.unconditional

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
        })
        if title is not UNSET:
            field_dict["title"] = title
        if cause is not UNSET:
            field_dict["cause"] = cause
        if forbidden_hazardous_goods is not UNSET:
            field_dict["forbiddenHazardousGoods"] = forbidden_hazardous_goods
        if max_weight is not UNSET:
            field_dict["maxWeight"] = max_weight
        if max_gross_weight is not UNSET:
            field_dict["maxGrossWeight"] = max_gross_weight
        if max_weight_per_axle is not UNSET:
            field_dict["maxWeightPerAxle"] = max_weight_per_axle
        if max_axle_group_weight is not UNSET:
            field_dict["maxAxleGroupWeight"] = max_axle_group_weight
        if max_height is not UNSET:
            field_dict["maxHeight"] = max_height
        if max_width is not UNSET:
            field_dict["maxWidth"] = max_width
        if max_length is not UNSET:
            field_dict["maxLength"] = max_length
        if max_tires_count is not UNSET:
            field_dict["maxTiresCount"] = max_tires_count
        if axle_count is not UNSET:
            field_dict["axleCount"] = axle_count
        if tunnel_category is not UNSET:
            field_dict["tunnelCategory"] = tunnel_category
        if time_dependent is not UNSET:
            field_dict["timeDependent"] = time_dependent
        if truck_type is not UNSET:
            field_dict["truckType"] = truck_type
        if vehicle_type is not UNSET:
            field_dict["vehicleType"] = vehicle_type
        if trailer_count is not UNSET:
            field_dict["trailerCount"] = trailer_count
        if max_engine_size_cc is not UNSET:
            field_dict["maxEngineSizeCC"] = max_engine_size_cc
        if min_engine_size_cc is not UNSET:
            field_dict["minEngineSizeCC"] = min_engine_size_cc
        if max_occupancy is not UNSET:
            field_dict["maxOccupancy"] = max_occupancy
        if min_occupancy is not UNSET:
            field_dict["minOccupancy"] = min_occupancy
        if restricted_times is not UNSET:
            field_dict["restrictedTimes"] = restricted_times
        if max_kpra_length is not UNSET:
            field_dict["maxKpraLength"] = max_kpra_length
        if max_payload_capacity is not UNSET:
            field_dict["maxPayloadCapacity"] = max_payload_capacity
        if unconditional is not UNSET:
            field_dict["unconditional"] = unconditional

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.axle_group_weight import AxleGroupWeight
        from ..models.trailer_count_range import TrailerCountRange
        from ..models.truck_axle_count_range import TruckAxleCountRange
        from ..models.vehicle_restriction_max_weight import VehicleRestrictionMaxWeight

        d = dict(src_dict)
        type_ = VehicleRestrictionType(d.pop("type"))

        title = d.pop("title", UNSET)

        cause = d.pop("cause", UNSET)

        def _parse_forbidden_hazardous_goods(
            data: object,
        ) -> HazardousGoodsRestrictionAny | list[str] | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                componentsschemas_forbidden_hazardous_goods_type_0 = (
                    HazardousGoodsRestrictionAny(data)
                )

                return componentsschemas_forbidden_hazardous_goods_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, list):
                raise TypeError()
            componentsschemas_forbidden_hazardous_goods_type_1 = cast(list[str], data)

            return componentsschemas_forbidden_hazardous_goods_type_1

        forbidden_hazardous_goods = _parse_forbidden_hazardous_goods(
            d.pop("forbiddenHazardousGoods", UNSET)
        )

        _max_weight = d.pop("maxWeight", UNSET)
        max_weight: VehicleRestrictionMaxWeight | Unset
        if isinstance(_max_weight, Unset):
            max_weight = UNSET
        else:
            max_weight = VehicleRestrictionMaxWeight.from_dict(_max_weight)

        max_gross_weight = d.pop("maxGrossWeight", UNSET)

        max_weight_per_axle = d.pop("maxWeightPerAxle", UNSET)

        _max_axle_group_weight = d.pop("maxAxleGroupWeight", UNSET)
        max_axle_group_weight: AxleGroupWeight | Unset
        if isinstance(_max_axle_group_weight, Unset):
            max_axle_group_weight = UNSET
        else:
            max_axle_group_weight = AxleGroupWeight.from_dict(_max_axle_group_weight)

        max_height = d.pop("maxHeight", UNSET)

        max_width = d.pop("maxWidth", UNSET)

        max_length = d.pop("maxLength", UNSET)

        max_tires_count = d.pop("maxTiresCount", UNSET)

        _axle_count = d.pop("axleCount", UNSET)
        axle_count: TruckAxleCountRange | Unset
        if isinstance(_axle_count, Unset):
            axle_count = UNSET
        else:
            axle_count = TruckAxleCountRange.from_dict(_axle_count)

        _tunnel_category = d.pop("tunnelCategory", UNSET)
        tunnel_category: TunnelCategory | Unset
        if isinstance(_tunnel_category, Unset):
            tunnel_category = UNSET
        else:
            tunnel_category = TunnelCategory(_tunnel_category)

        time_dependent = d.pop("timeDependent", UNSET)

        _truck_type = d.pop("truckType", UNSET)
        truck_type: TruckType | Unset
        if isinstance(_truck_type, Unset):
            truck_type = UNSET
        else:
            truck_type = TruckType(_truck_type)

        _vehicle_type = d.pop("vehicleType", UNSET)
        vehicle_type: VehicleType | Unset
        if isinstance(_vehicle_type, Unset):
            vehicle_type = UNSET
        else:
            vehicle_type = VehicleType(_vehicle_type)

        _trailer_count = d.pop("trailerCount", UNSET)
        trailer_count: TrailerCountRange | Unset
        if isinstance(_trailer_count, Unset):
            trailer_count = UNSET
        else:
            trailer_count = TrailerCountRange.from_dict(_trailer_count)

        max_engine_size_cc = d.pop("maxEngineSizeCC", UNSET)

        min_engine_size_cc = d.pop("minEngineSizeCC", UNSET)

        max_occupancy = d.pop("maxOccupancy", UNSET)

        min_occupancy = d.pop("minOccupancy", UNSET)

        restricted_times = d.pop("restrictedTimes", UNSET)

        max_kpra_length = d.pop("maxKpraLength", UNSET)

        max_payload_capacity = d.pop("maxPayloadCapacity", UNSET)

        unconditional = d.pop("unconditional", UNSET)

        vehicle_restriction = cls(
            type_=type_,
            title=title,
            cause=cause,
            forbidden_hazardous_goods=forbidden_hazardous_goods,
            max_weight=max_weight,
            max_gross_weight=max_gross_weight,
            max_weight_per_axle=max_weight_per_axle,
            max_axle_group_weight=max_axle_group_weight,
            max_height=max_height,
            max_width=max_width,
            max_length=max_length,
            max_tires_count=max_tires_count,
            axle_count=axle_count,
            tunnel_category=tunnel_category,
            time_dependent=time_dependent,
            truck_type=truck_type,
            vehicle_type=vehicle_type,
            trailer_count=trailer_count,
            max_engine_size_cc=max_engine_size_cc,
            min_engine_size_cc=min_engine_size_cc,
            max_occupancy=max_occupancy,
            min_occupancy=min_occupancy,
            restricted_times=restricted_times,
            max_kpra_length=max_kpra_length,
            max_payload_capacity=max_payload_capacity,
            unconditional=unconditional,
        )

        vehicle_restriction.additional_properties = d
        return vehicle_restriction

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
