from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.tunnel_category import TunnelCategory
from ..models.vehicle_category import VehicleCategory
from ..models.vehicle_engine_type import VehicleEngineType
from ..models.vehicle_type import VehicleType
from ..types import UNSET, Unset

T = TypeVar("T", bound="Vehicle")


@_attrs_define
class Vehicle:
    """Vehicle-specific parameters

    Attributes:
        shipped_hazardous_goods (str | Unset): Hazardous goods restrictions refer to the limitations and regulations
            imposed on the transportation of specific types of hazardous materials during a trip.

            A comma-separated list of hazardous goods being shipped in the vehicle. The following values are possible:

            * `explosive`: Materials that are capable of causing an explosion.
            * `gas`: Gas (definition varies from country to country). For details, check
            [here](https://en.wikipedia.org/wiki/HAZMAT_Class_2_Gases).
            * `flammable`: Materials that are easily ignited and capable of catching fire.
            * `combustible`: Materials that have the potential to burn or catch fire.
            * `organic`: Materials derived from living organisms or containing carbon compounds.
            * `poison`: Substances that can cause harm or death when ingested, inhaled, or absorbed.
            * `radioactive`: Materials that emit radiation and pose potential health risks.
            * `corrosive`: Substances that can cause damage or destruction through chemical reactions.
            * `poisonousInhalation`: Materials that are toxic when inhaled.
            * `harmfulToWater`: Materials that can cause pollution or harm to water bodies.
            * `other`: Other types of hazardous materials not covered by the above categories.

            **Note:** Supported in `truck`, `bus`, `privateBus`, `car` (Beta), `taxi` (Beta) transport modes.
             Example: explosive,gas,flammable.
        gross_weight (int | Unset): Gross vehicle weight, including trailers and shipped goods when loaded at capacity,
            specified in kilograms.

            If unspecified, it will default to currentWeight. If neither parameter has a value specified, it will default to
            0.

            **Notes:**
            * Supported in `truck`, `bus`, `privateBus`, `car` (Beta), `taxi` (Beta) transport modes.
            * Maximum weight for a car or taxi _without_ a trailer is 4250 kg.
            * Maximum weight for a car or taxi _with_ a trailer is 7550 kg.
        current_weight (int | Unset): Current vehicle weight, including trailers and shipped goods currently loaded,
            specified in kilograms.

            If unspecified, it will default to grossWeight. If neither parameter has a value specified, it will default to
            0.

            **Notes:**
            * Supported in `truck`, `bus`, `privateBus`, `car` (Beta), `taxi` (Beta) transport modes.
            * Maximum weight for a car or taxi _without_ a trailer is 5000 kg.
            * Maximum weight for a car or taxi _with_ a trailer is 8500 kg.
            * A route request with `currentWeight` above `grossWeight` may result in non-compliant or invalid routes.
        empty_weight (int | Unset): Empty weight of the vehicle combination ready to be driven, including necessary
            fluids and equipment
            determined by the local regulations, specified in kilograms.

            **Note:**
            * Supported in `truck`, `bus`, `privateBus`, `car` (Beta), `taxi` (Beta) transport modes.
            * Maximum weight for a car or taxi _without_ a trailer is 4250 kg.
            * Maximum weight for a car or taxi _with_ a trailer is 7550 kg.
        weight_per_axle (int | Unset): Heaviest vehicle weight-per-axle, specified in kilograms.

            Heaviest weight-per-axle, regardless of axle-type or axle-group. It is evaluated against
            all axle-weight restrictions, including single-axle and tandem-axle weight restrictions.
            It is useful if differences between axle types, like tandem and triple axles, are not
            relevant. This is the case in many countries, since they don't distinguish between these
            different axle groups on signs and in regulations.

            More fine-grained axle weight input is possible with `weightPerAxleGroup`.

            **Note:** `weightPerAxleGroup` and `weightPerAxle` are incompatible.

            **Note:** Supported in `truck`, `bus`, `privateBus`, `car` (Beta), `taxi` (Beta) transport modes.
        weight_per_axle_group (str | Unset): Specifies the weights of different axle groups, such as single and tandem
            axles.

            This allows specification of axle weights in a more fine-grained way than `weightPerAxle`. This
            is relevant in countries with signs and regulations that specify different limits for different
            axle groups, such as the USA and Sweden.

            All axle group weights are evaluated against their respective axle group restrictions and against
            generic axle weight restrictions. This means that the provided tandem axle group weight is
            compared with all tandem axle group weight restrictions and all generic axle weight restrictions.
            The same is true for single, triple, quad, and quint axle groups.

            Format: `AxleGroup:Weight[,AxleGroup2:Weight2]...`

            Currently, allowed axle-groups are:
              * `single`
              * `tandem`
              * `triple`
              * `quad`
              * `quint`

            Weights are specified in kilograms (kg) and represent the total weight of the axle-group.

            **Note:** `weightPerAxleGroup` and `weightPerAxle` are incompatible.

            **Limitations:** only valid when `transportMode` is one of (`truck`, `bus`, `privateBus`).
             Example: single:11000,tandem:18000.
        height (int | Unset): Vehicle height, specified in centimeters.

            **Note:** Supported in `truck`, `bus`, `privateBus`, `car` (Beta), `taxi` (Beta) transport modes.
        width (int | Unset): Vehicle width, specified in centimeters.

            **Note:** Supported in `truck`, `bus`, `privateBus`, `car` (Beta), `taxi` (Beta) transport modes.
        length (int | Unset): Vehicle length, specified in centimeters.

            **Note:** Supported in `truck`, `bus`, `privateBus`, `car` (Beta), `taxi` (Beta) transport modes.
        kpra_length (int | Unset): Kingpin to rear axle length, in centimeters.

            **NOTE:** Currently, the KPRA restrictions are only present in California and Idaho.

            **Note:** Supported in `truck`, `car` (Beta), `taxi` (Beta) transport modes.
        payload_capacity (int | Unset): Allowed payload capacity, including trailers, specified in kilograms.

            **Note:** Supported in `truck`, `car` (Beta), `taxi` (Beta) transport modes.
        tunnel_category (TunnelCategory | Unset): Specifies the tunnel category used to restrict the transport of
            specific goods.
        axle_count (int | Unset): Specifies the total number of axles the vehicle has, i.e., axles on the base vehicle
            and any attached trailers.

            **Note:** Supported in `truck`, `bus`, `privateBus`, `car` (Beta), `taxi` (Beta) transport modes.
        tires_count (int | Unset): Specifies the total number of tires the vehicle has, i.e., the tires on the base
            vehicle and any attached trailers.
        category (VehicleCategory | Unset): Specifies the category of the vehicle. The supported values are:

            * `undefined`: The vehicle category is undefined, and no special considerations are taken into
              account. Vehicle routing will proceed as normal.
            * `lightTruck`: The vehicle is a truck light enough to be classified more as a car than as a truck.
              This exempts it from many legal restrictions for normal trucks. However, restrictions related to the physical
            dimensions of the truck or its cargo still apply.

              For more details, refer to [Truck categories](https://www.here.com/docs/bundle/routing-api-developer-
            guide-v8/page/concepts/truck-routing.html#truck-categories).

              **Note:** Supported only in `truck` transport mode.
             Default: VehicleCategory.UNDEFINED.
        trailer_count (int | Unset): The number of trailers attached to the vehicle.

            Maximum value when used with `transportMode=car` or `transportMode=taxi` is 1.

            **Limitations:** Considered for route calculation when `transportMode` is one of (`truck`, `bus`, `privateBus`).
            Considered for route calculation for restrictions, but not for speed limits, when `transportMode` is `car` or
            `taxi`.
             Default: 0.
        hov_occupancy (int | Unset): **Note**: This parameter is deprecated, `vehicle[occupancy]` and `allow[hov]`
            should be used instead.
            The number of occupants in the vehicle, defined as individuals occupying a seat with a restraint device.
            This value affects the ability of the router to use HOV (High-Occupancy Vehicles) restricted lanes.

            Limitations:
              * Any value over 1 is interpreted as the ability to use any HOV lane, including those restricted to 3+
            passengers.
             Default: 1.
        license_plate (str | Unset): Specifies the information about the vehicle's license plate number.
            This information is used to evaluate whether certain vehicle restrictions in environmental zones apply.
            Currently, only the last character of the license plate can be provided.

            Format: `lastCharacter:{character}`

            Example: `lastCharacter:2`
        speed_cap (float | Unset): Specifies the maximum speed, in meters per second (m/s), that the user wishes not to
            exceed.
            This parameter affects the route's estimated time of arrival (ETA) and consumption calculation.

            Limitations:
              * valid for following transport modes: `car`, `truck`, `scooter`, `taxi`, `bus`, and `privateBus`

            Notes:
              * Car and Truck mode updates route ETA.
              * Scooter mode updates route optimization and ETA.
              * Resulting ETA can not be decreased by this parameter.
        speed_cap_per_fc (str | Unset): A comma separated list of speeds in meters per second (m/s) specifying the
            maximum speed per FC (Functional Class, as defined in the `FunctionalClass` schema) that the user wishes not to
            exceed.
            The list can have up to 5 entries, corresponding to FC 1 to FC 5. Empty entries indicate that no speed cap is
            specified for the corresponding FC.
            This parameter affects the route's estimated time of arrival (ETA) and consumption calculation.

            Limitations:
              * valid for following transport modes: `car`, `truck`

            Values limitations:
              * minimum: 1.00
              * maximum: 70.00

            Examples:
              * `vehicle[speedCapPerFc]=65,50.5,40,30,10` - specify limits for all FCs
              * `vehicle[speedCapPerFc]=65,50.5,,30,10` - specify limits for all FCs except for FC 3
              * `vehicle[speedCapPerFc]=65,50.5,40` - specify limits for FC 1, 2 and 3

            Notes:
              * Resulting ETA can not be decreased by this parameter.
              * vehicle[speedCapPerFc] and vehicle[speedCap] may be used in combination. For FCs where both values are
            specified, the minimum value is used.
        engine_size_cc (int | Unset): Specifies the engine size of the vehicle in cubic centimeters.
            Currently, the value is used only in scooter mode.
            This parameter is utilized to determine if the scooter can be classified as a moped.
            Scooters with an engine size less than 51cc are considered mopeds.
            **Alpha**: This API is in development. It may not be stable and is subject to change. It may have no impact on
            response.
        occupancy (int | Unset): The number of occupants on the vehicle, defined as individuals occupying a seat.
            This value affects the ability of the router to use HOV (High-Occupancy Vehicles) restricted lanes. If not set
            and `allow[hov]=true` is set, then occupancy requirements for all HOV conditions are considered to be met.
            This parameter also affects scooter occupancy restrictions. If not set, occupancy restrictions for scooters are
            ignored.

            The parameter is also used for calculating the toll cost, in cases where the toll-cost for the vehicle depends
            on the passenger count. If not set, occupancy of 1 is assumed for toll calculation.

            **Note:**: This parameter can't be used with 'vehicle[hovOccupancy]'.
        engine_type (VehicleEngineType | Unset): Specifies the engine type of the vehicle.

            **Limitations:**  Currently this parameter is used only for toll calculation. It may be used at any point for
            route calculation (for example, to automatically avoid environmental zones).

            **Note:**
              * If engineType is specified as `internalCombustion`, valid `fuel[type]` should also be provided to get fuel
            specific toll. If `fuel[type]` is not provided, default toll without considering `fuel[type]` will be returned.
              * If `ev` or `fuel` namespace parameters are provided with an incompatible `engineType` (e.g.
            engineType=internalCombustion is provided along with `ev` namespace parameters) then `ev` namespace will
            override `engineType` and incompatible `engineType` will be ignored for toll, consumption, and emission
            computations.
        frontal_area (float | Unset): Frontal area represents the total cross section area of the vehicle as viewed from
            the front, specified in square meters. Physical consumption model is using this value in combination with
            `airDragCoefficient` to calculate the consumption caused by air resistance.
            **Note:** This attribute, or both `width` and `height`, is required when using the physical model
            `consumptionModel=physical` for EV consumption.

            **Alpha**: This parameter is in development. It may not be stable and is subject to change.
        rolling_resistance_coefficient (float | Unset): Rolling resistance refers to the resistance experienced by your
            vehicle tire as it rolls over a surface. The main causes of this resistance are tire deformation, wing drag, and
            friction with the ground. The coefficient of rolling resistance is a numerical value indicating the severity of
            this factor.
            **Note:** This attribute is required when using the physical model `consumptionModel=physical` for EV
            consumption.

            **Alpha**: This parameter is in development. It may not be stable and is subject to change.
        air_drag_coefficient (float | Unset): The drag coefficient of an vehicle defines the way the vehicle is expected
            to pass through the surrounding air. More streamlined vehicles are more aerodynamic and therefore have smaller
            drag coefficient.
            **Note:** This attribute is required when using the physical model `consumptionModel=physical` for EV
            consumption.

            **Alpha**: This parameter is in development. It may not be stable and is subject to change.
        type_ (VehicleType | Unset): Specifies the type of the vehicle

            * `StraightTruck`: A truck on a single frame with a permanently attached cargo area. **Note:**
            default value when truck routing mode is used.
            * `Tractor`: A towing vehicle that can pull one or more semi-trailers (also known as a semi-truck).

            **Limitations:** only valid for `transportMode=truck`.
    """

    shipped_hazardous_goods: str | Unset = UNSET
    gross_weight: int | Unset = UNSET
    current_weight: int | Unset = UNSET
    empty_weight: int | Unset = UNSET
    weight_per_axle: int | Unset = UNSET
    weight_per_axle_group: str | Unset = UNSET
    height: int | Unset = UNSET
    width: int | Unset = UNSET
    length: int | Unset = UNSET
    kpra_length: int | Unset = UNSET
    payload_capacity: int | Unset = UNSET
    tunnel_category: TunnelCategory | Unset = UNSET
    axle_count: int | Unset = UNSET
    tires_count: int | Unset = UNSET
    category: VehicleCategory | Unset = VehicleCategory.UNDEFINED
    trailer_count: int | Unset = 0
    hov_occupancy: int | Unset = 1
    license_plate: str | Unset = UNSET
    speed_cap: float | Unset = UNSET
    speed_cap_per_fc: str | Unset = UNSET
    engine_size_cc: int | Unset = UNSET
    occupancy: int | Unset = UNSET
    engine_type: VehicleEngineType | Unset = UNSET
    frontal_area: float | Unset = UNSET
    rolling_resistance_coefficient: float | Unset = UNSET
    air_drag_coefficient: float | Unset = UNSET
    type_: VehicleType | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        shipped_hazardous_goods = self.shipped_hazardous_goods

        gross_weight = self.gross_weight

        current_weight = self.current_weight

        empty_weight = self.empty_weight

        weight_per_axle = self.weight_per_axle

        weight_per_axle_group = self.weight_per_axle_group

        height = self.height

        width = self.width

        length = self.length

        kpra_length = self.kpra_length

        payload_capacity = self.payload_capacity

        tunnel_category: str | Unset = UNSET
        if not isinstance(self.tunnel_category, Unset):
            tunnel_category = self.tunnel_category.value

        axle_count = self.axle_count

        tires_count = self.tires_count

        category: str | Unset = UNSET
        if not isinstance(self.category, Unset):
            category = self.category.value

        trailer_count = self.trailer_count

        hov_occupancy = self.hov_occupancy

        license_plate = self.license_plate

        speed_cap = self.speed_cap

        speed_cap_per_fc = self.speed_cap_per_fc

        engine_size_cc = self.engine_size_cc

        occupancy = self.occupancy

        engine_type: str | Unset = UNSET
        if not isinstance(self.engine_type, Unset):
            engine_type = self.engine_type.value

        frontal_area = self.frontal_area

        rolling_resistance_coefficient = self.rolling_resistance_coefficient

        air_drag_coefficient = self.air_drag_coefficient

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if shipped_hazardous_goods is not UNSET:
            field_dict["shippedHazardousGoods"] = shipped_hazardous_goods
        if gross_weight is not UNSET:
            field_dict["grossWeight"] = gross_weight
        if current_weight is not UNSET:
            field_dict["currentWeight"] = current_weight
        if empty_weight is not UNSET:
            field_dict["emptyWeight"] = empty_weight
        if weight_per_axle is not UNSET:
            field_dict["weightPerAxle"] = weight_per_axle
        if weight_per_axle_group is not UNSET:
            field_dict["weightPerAxleGroup"] = weight_per_axle_group
        if height is not UNSET:
            field_dict["height"] = height
        if width is not UNSET:
            field_dict["width"] = width
        if length is not UNSET:
            field_dict["length"] = length
        if kpra_length is not UNSET:
            field_dict["kpraLength"] = kpra_length
        if payload_capacity is not UNSET:
            field_dict["payloadCapacity"] = payload_capacity
        if tunnel_category is not UNSET:
            field_dict["tunnelCategory"] = tunnel_category
        if axle_count is not UNSET:
            field_dict["axleCount"] = axle_count
        if tires_count is not UNSET:
            field_dict["tiresCount"] = tires_count
        if category is not UNSET:
            field_dict["category"] = category
        if trailer_count is not UNSET:
            field_dict["trailerCount"] = trailer_count
        if hov_occupancy is not UNSET:
            field_dict["hovOccupancy"] = hov_occupancy
        if license_plate is not UNSET:
            field_dict["licensePlate"] = license_plate
        if speed_cap is not UNSET:
            field_dict["speedCap"] = speed_cap
        if speed_cap_per_fc is not UNSET:
            field_dict["speedCapPerFc"] = speed_cap_per_fc
        if engine_size_cc is not UNSET:
            field_dict["engineSizeCc"] = engine_size_cc
        if occupancy is not UNSET:
            field_dict["occupancy"] = occupancy
        if engine_type is not UNSET:
            field_dict["engineType"] = engine_type
        if frontal_area is not UNSET:
            field_dict["frontalArea"] = frontal_area
        if rolling_resistance_coefficient is not UNSET:
            field_dict["rollingResistanceCoefficient"] = rolling_resistance_coefficient
        if air_drag_coefficient is not UNSET:
            field_dict["airDragCoefficient"] = air_drag_coefficient
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        shipped_hazardous_goods = d.pop("shippedHazardousGoods", UNSET)

        gross_weight = d.pop("grossWeight", UNSET)

        current_weight = d.pop("currentWeight", UNSET)

        empty_weight = d.pop("emptyWeight", UNSET)

        weight_per_axle = d.pop("weightPerAxle", UNSET)

        weight_per_axle_group = d.pop("weightPerAxleGroup", UNSET)

        height = d.pop("height", UNSET)

        width = d.pop("width", UNSET)

        length = d.pop("length", UNSET)

        kpra_length = d.pop("kpraLength", UNSET)

        payload_capacity = d.pop("payloadCapacity", UNSET)

        _tunnel_category = d.pop("tunnelCategory", UNSET)
        tunnel_category: TunnelCategory | Unset
        if isinstance(_tunnel_category, Unset):
            tunnel_category = UNSET
        else:
            tunnel_category = TunnelCategory(_tunnel_category)

        axle_count = d.pop("axleCount", UNSET)

        tires_count = d.pop("tiresCount", UNSET)

        _category = d.pop("category", UNSET)
        category: VehicleCategory | Unset
        if isinstance(_category, Unset):
            category = UNSET
        else:
            category = VehicleCategory(_category)

        trailer_count = d.pop("trailerCount", UNSET)

        hov_occupancy = d.pop("hovOccupancy", UNSET)

        license_plate = d.pop("licensePlate", UNSET)

        speed_cap = d.pop("speedCap", UNSET)

        speed_cap_per_fc = d.pop("speedCapPerFc", UNSET)

        engine_size_cc = d.pop("engineSizeCc", UNSET)

        occupancy = d.pop("occupancy", UNSET)

        _engine_type = d.pop("engineType", UNSET)
        engine_type: VehicleEngineType | Unset
        if isinstance(_engine_type, Unset):
            engine_type = UNSET
        else:
            engine_type = VehicleEngineType(_engine_type)

        frontal_area = d.pop("frontalArea", UNSET)

        rolling_resistance_coefficient = d.pop("rollingResistanceCoefficient", UNSET)

        air_drag_coefficient = d.pop("airDragCoefficient", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: VehicleType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = VehicleType(_type_)

        vehicle = cls(
            shipped_hazardous_goods=shipped_hazardous_goods,
            gross_weight=gross_weight,
            current_weight=current_weight,
            empty_weight=empty_weight,
            weight_per_axle=weight_per_axle,
            weight_per_axle_group=weight_per_axle_group,
            height=height,
            width=width,
            length=length,
            kpra_length=kpra_length,
            payload_capacity=payload_capacity,
            tunnel_category=tunnel_category,
            axle_count=axle_count,
            tires_count=tires_count,
            category=category,
            trailer_count=trailer_count,
            hov_occupancy=hov_occupancy,
            license_plate=license_plate,
            speed_cap=speed_cap,
            speed_cap_per_fc=speed_cap_per_fc,
            engine_size_cc=engine_size_cc,
            occupancy=occupancy,
            engine_type=engine_type,
            frontal_area=frontal_area,
            rolling_resistance_coefficient=rolling_resistance_coefficient,
            air_drag_coefficient=air_drag_coefficient,
            type_=type_,
        )

        vehicle.additional_properties = d
        return vehicle

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
