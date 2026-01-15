from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RoutingErrorResponse")


@_attrs_define
class RoutingErrorResponse:
    """Response in case of error

    Attributes:
        title (str): Human-readable error description Example: Input data failed validation.
        status (int): HTTP status code Example: 400.
        code (str): Machine readable service error code.

            All error codes of this service start with "`E605`". The last three digits describe a specific error. Provide
            this error code when contacting support.

            **NOTE:** Please note that the list of possible error codes could be extended in the future. The client
            application is expected to handle such a case gracefully.

            | Code      | Reason  |
            | --------- | ------- |
            | `E60500X` | Malformed query. Typically due to invalid values such as `transportMode=spaceShuttle` or missing
            required fields. Check the error message for details. |
            | `E605010` | Invalid combination of vehicle options and transport mode. |
            | `E605011` | Invalid combination of avoid feature `difficultTurns` or `uTurns` and transport mode. Check
            `avoid` for details. |
            | `E605012` | Invalid combination of transport mode and routing mode. Check `routingMode` for a list of
            supported combinations. |
            | `E605013` | Invalid return options. Check `return` for valid combinations of values. |
            | `E605014` | Invalid language code. Check `lang` for details on how valid language codes look. |
            | `E605015` | Too many alternatives. Check `alternatives` for the maximum number of alternatives allowed. |
            | `E605016` | Invalid country code. Check `countries` under `Exclude`. |
            | `E605017` | `spans` contains a value whose dependency has not been requested |
            | `E605018` | Invalid combination of departure and arrival time |
            | `E605019` | `truck[weightPerAxle]` and `truck[weightPerAxleGroup]` are incompatible |
            | `E605020` | Invalid combination of `radius` and `snapRadius`  |
            | `E605021` | Invalid Combination of `vehicle[occupancy]`/`allow[hot]`/`allow[hov]` and `vehicle[hovOccupancy]`
            |
            | `E605022` | `radius` * `radiusPenalty` / 100 must not exceed 7200  |
            | `E605023` | Invalid combination of `radiusPenalty` and `snapRadius` |
            | `E605024` | `vehicle[currentWeight]` or `vehicle[grossWeight]` exceeds limit for given `transportMode`. |
            | `E605025` | Invalid state code. Check `states` under `Exclude` |
            | `E605026` | Invalid country code. Check `states` under `Exclude` |
            | `E605027` | Ev parameters cannot be used with the specified transportMode. |
            | `E605028` | Fuel parameters cannot be used with the specified transportMode. |
            | `E605029` | State code not available in map data. Check `states` under `Exclude` |
            | `E605030` | Invalid EV options. Check `ev` for details. |
            | `E605032` | Invalid transport mode for speed cap, check `vehicle[speedCap]` for details. |
            | `E605033` | Invalid combination of scooter and transport mode. Check `scooter` for valid scooter transport
            modes. |
            | `E605034` | Invalid Speed Cap, check `vehicle[speedCap]` or `vehicle[speedCapPerFc]` for details. |
            | `E605035` | MLDuration is not supported with `vehicle[speedCap]` and `vehicle[speedCapPerFc]` parameter. |
            | `E605036` | Consumption parameters are not supported for combination of EV and Fuel-based vehicle. Check `ev`
            or `fuel` for details. |
            | `E605037` | Invalid Fuel options. Check `fuel` for details. |
            | `E605039` | Invalid combination of driver schedule and transport mode. |
            | `E605040` | Invalid combination of `ev[makeReachable]` and `transportMode`. Check `ev` for details. |
            | `E605041` | Invalid combination of `ev[makeReachable]` and `routingMode`. Check `ev` for details. |
            | `E605043` | Invalid combination of `ev[makeReachable]` and `avoid` options. Check `ev` for details. |
            | `E605047` | Invalid combination of `ev[makeReachable]` and `arrivalTime`. Check `ev` for details. |
            | `E605048` | Invalid combination of avoid feature `difficultTurns` and truck category `lightTruck`. |
            | `E605052` | Invalid number of trace points. Check `MatchTrace` for the minimum and maximum number of trace
            points allowed. |
            | `E605053` | Invalid Match trace via. Check `via` in `MatchTrace` for valid indexes. |
            | `E605054` | Too many avoid areas. Check `areas` for the maximum number of avoid areas allowed. |
            | `E605055` | Invalid trailer axle count. |
            | `E605056` | Too many avoid polygons. Check `areas[polygon]` for the maximum number of polygons allowed. |
            | `E605057` | Too many vertices in the polygon. Check `areas[polygon]` for the maximum number of vertices
            allowed. |
            | `E605058` | Not enough vertices in the polygon. Check `areas[polygon]` for the minimum number of vertices
            allowed. |
            | `E605059` | Polygon is self-intersecting. Check `areas[polygon]`. |
            | `E605060` | Invalid trace point. Check `lat` value must be between -90 and 90 and `lng` value must be between
            -180 and 180. |
            | `E605064` | Invalid transport mode for speed cap per Functional Class, check `vehicle[speedCapPerFc]` for
            details. |
            | `E605075` | Invalid customizationIndex. |
            | `E605076` | Too many charging stations to exclude. Check `ev[excludeChargingStations]` for maximum number of
            charging stations allowed. |
            | `E605077` | `rerouting[lastTraveledSectionIndex]` is out of range. |
            | `E605101` | Credentials not allowed for calculating routes in Japan. |
            | `E605201` | RouteHandle not valid (anymore). (Re-)calculate route to retrieve new handle. |
            | `E605204` | Invalid combination of EV and driver schedule. |
            | `E605301` | Pedestrian options are only supported for transport mode `pedestrian`. |
            | `E605302` | Routing zones is not supported for transport mode `pedestrian`. |
            | `E605303` | Avoiding routing zones is not supported for transport mode `pedestrian`. |
            | `E605304` | Avoiding truck road types is not supported for transport mode `pedestrian`. |
            | `E605400` | Customization not supported. |
            | `E6055XX` | Internal server error. |
             Example: E605001.
        cause (str): Human-readable explanation for the error Example: The input data in question does not comply with
            validation rules.
        action (str): Human-readable description of the action that can be taken to correct the error Example: Request a
            valid id.
        correlation_id (str): Auto-generated id that univocally identifies the request Example:
            4199533b-6290-41db-8d79-edf4f4019a74.
    """

    title: str
    status: int
    code: str
    cause: str
    action: str
    correlation_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        status = self.status

        code = self.code

        cause = self.cause

        action = self.action

        correlation_id = self.correlation_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "title": title,
            "status": status,
            "code": code,
            "cause": cause,
            "action": action,
            "correlationId": correlation_id,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        title = d.pop("title")

        status = d.pop("status")

        code = d.pop("code")

        cause = d.pop("cause")

        action = d.pop("action")

        correlation_id = d.pop("correlationId")

        routing_error_response = cls(
            title=title,
            status=status,
            code=code,
            cause=cause,
            action=action,
            correlation_id=correlation_id,
        )

        routing_error_response.additional_properties = d
        return routing_error_response

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
