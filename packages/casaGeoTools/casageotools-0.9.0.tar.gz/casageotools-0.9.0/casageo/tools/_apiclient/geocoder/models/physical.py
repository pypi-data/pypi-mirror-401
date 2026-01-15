from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Physical")


@_attrs_define
class Physical:
    """
    Attributes:
        boat_ferry (bool | Unset): The segment represents a generalised route of a boat ferry for passengers or vehicles
            over water,
            including routes to pedestrian only islands, tourist areas, commuter ferry routes open to only pedestrians, etc.

            - `true`: The road is a boat ferry.
            - `false`: The road isn't a boat ferry.
        bridge (bool | Unset): Identifies a structure that allows a road, railway, or walkway to pass over another road,
            railway, waterway, or valley serving map display and route guidance functionalities.

            - `true`: The road is a bridge.
            - `false`: The road isn't a bridge.
        delivery_road (bool | Unset): Indication of a delivery road.

            - `true`: The physical characteristic of the road is that it functions as a delivery road.
            - `false`: The physical characteristic of the road is that it doesn't function as a delivery road.
        movable_bridge (bool | Unset): Movable Bridge indicates a bridge that moves to allow passage (usually) for boats
            or barges.

            - `true`: The road is a movable bridge.
            - `false`: The road isn't a movable bridge.
        multiply_digitized (bool | Unset): Multiply Digitised identifies separately digitised roads, i.e., roads that
            are digitised with one line per
            direction of traffic instead of one line per road.

            - `true`: The physical characteristic of the road is that it functions as multiplyDigitized.
            - `false`: The physical characteristic of the road is that it doesn't function as multiplyDigitized.
        paved (bool | Unset): Indicates whether the navigable segment is paved.

            - `true`: The physical characteristic of the road is paved.
            - `false`: The physical characteristic of the road isn't paved.
        private (bool | Unset): Private identifies roads that are not maintained by an organisation responsible for
            maintenance of
            public roads.

            - `true`: The road is private..
            - `false`: The road isn't private.
        rail_ferry (bool | Unset): The segment represents a generalised route of a ferry for passengers or vehicles via
            rail.

            - `true`: The road is a rail flerry.
            - `false`: The road isn't a rail flerry.
        tunnel (bool | Unset): Identifies an enclosed (on all sides) passageway through or under an obstruction.

            - `true`: The road is a tunnel.
            - `false`: The road isn't a tunnel.
    """

    boat_ferry: bool | Unset = UNSET
    bridge: bool | Unset = UNSET
    delivery_road: bool | Unset = UNSET
    movable_bridge: bool | Unset = UNSET
    multiply_digitized: bool | Unset = UNSET
    paved: bool | Unset = UNSET
    private: bool | Unset = UNSET
    rail_ferry: bool | Unset = UNSET
    tunnel: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        boat_ferry = self.boat_ferry

        bridge = self.bridge

        delivery_road = self.delivery_road

        movable_bridge = self.movable_bridge

        multiply_digitized = self.multiply_digitized

        paved = self.paved

        private = self.private

        rail_ferry = self.rail_ferry

        tunnel = self.tunnel

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if boat_ferry is not UNSET:
            field_dict["boatFerry"] = boat_ferry
        if bridge is not UNSET:
            field_dict["bridge"] = bridge
        if delivery_road is not UNSET:
            field_dict["deliveryRoad"] = delivery_road
        if movable_bridge is not UNSET:
            field_dict["movableBridge"] = movable_bridge
        if multiply_digitized is not UNSET:
            field_dict["multiplyDigitized"] = multiply_digitized
        if paved is not UNSET:
            field_dict["paved"] = paved
        if private is not UNSET:
            field_dict["private"] = private
        if rail_ferry is not UNSET:
            field_dict["railFerry"] = rail_ferry
        if tunnel is not UNSET:
            field_dict["tunnel"] = tunnel

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        boat_ferry = d.pop("boatFerry", UNSET)

        bridge = d.pop("bridge", UNSET)

        delivery_road = d.pop("deliveryRoad", UNSET)

        movable_bridge = d.pop("movableBridge", UNSET)

        multiply_digitized = d.pop("multiplyDigitized", UNSET)

        paved = d.pop("paved", UNSET)

        private = d.pop("private", UNSET)

        rail_ferry = d.pop("railFerry", UNSET)

        tunnel = d.pop("tunnel", UNSET)

        physical = cls(
            boat_ferry=boat_ferry,
            bridge=bridge,
            delivery_road=delivery_road,
            movable_bridge=movable_bridge,
            multiply_digitized=multiply_digitized,
            paved=paved,
            private=private,
            rail_ferry=rail_ferry,
            tunnel=tunnel,
        )

        physical.additional_properties = d
        return physical

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
