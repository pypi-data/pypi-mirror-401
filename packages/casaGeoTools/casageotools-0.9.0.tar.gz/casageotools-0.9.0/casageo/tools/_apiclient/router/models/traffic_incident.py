from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.traffic_incident_criticality import TrafficIncidentCriticality
from ..types import UNSET, Unset

T = TypeVar("T", bound="TrafficIncident")


@_attrs_define
class TrafficIncident:
    """An incident describes a temporary event on the road network.
    It typically refers to a real world incident (accident, road construction, weather condition, etc.)
    on a street or street segment

        Attributes:
            description (str | Unset): A human readable description of the incident Example: closed due to roadworks.
            type_ (str | Unset): Extensible enum: `accident` `congestion` `construction` `disabledVehicle` `massTransit`
                `plannedEvent` `roadHazard` `roadClosure` `weather` `laneRestriction` `other` `...`
                An open list of possible incident causes / types.
                Note: Since new types are expected to appear, it is important to check for unknown types when parsing this
                value.
            criticality (TrafficIncidentCriticality | Unset): Describes the impact an incident has on the route.
                * critical - The part of the route the incident affects is not usable.
                * major - Major impact on duration, e.g. stop and go
                * minor - Minor impact on duration, e.g. traffic jam
                * low - Very little impact on duration, e.g. slightly increased traffic
            valid_from (datetime.datetime | Unset): **RFC 3339**, section 5.6 as defined by either `date-time` or `date-
                only` 'T' `partial-time` (ie no time-offset).
            valid_until (datetime.datetime | Unset): **RFC 3339**, section 5.6 as defined by either `date-time` or `date-
                only` 'T' `partial-time` (ie no time-offset).
            id (str | Unset): Traffic Incident unique identifier,

                Example of an incident identifier in standard representation:
                here:traffic:incident:1000155780078589348

                Id usage:
                Incident details can be queried from the traffic service. See
                [this tutorial](https://www.here.com/docs/bundle/traffic-api-developer-guide-v7/page/topics/use-cases/incidents-
                by-id.html).

                **Notice**:
                In most cases, the ID comes from a third party incident supplier.
                This means that once an incident has expired, the ID might be reused
    """

    description: str | Unset = UNSET
    type_: str | Unset = UNSET
    criticality: TrafficIncidentCriticality | Unset = UNSET
    valid_from: datetime.datetime | Unset = UNSET
    valid_until: datetime.datetime | Unset = UNSET
    id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        type_ = self.type_

        criticality: str | Unset = UNSET
        if not isinstance(self.criticality, Unset):
            criticality = self.criticality.value

        valid_from: str | Unset = UNSET
        if not isinstance(self.valid_from, Unset):
            valid_from = self.valid_from.isoformat()

        valid_until: str | Unset = UNSET
        if not isinstance(self.valid_until, Unset):
            valid_until = self.valid_until.isoformat()

        id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if type_ is not UNSET:
            field_dict["type"] = type_
        if criticality is not UNSET:
            field_dict["criticality"] = criticality
        if valid_from is not UNSET:
            field_dict["validFrom"] = valid_from
        if valid_until is not UNSET:
            field_dict["validUntil"] = valid_until
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description = d.pop("description", UNSET)

        type_ = d.pop("type", UNSET)

        _criticality = d.pop("criticality", UNSET)
        criticality: TrafficIncidentCriticality | Unset
        if isinstance(_criticality, Unset):
            criticality = UNSET
        else:
            criticality = TrafficIncidentCriticality(_criticality)

        _valid_from = d.pop("validFrom", UNSET)
        valid_from: datetime.datetime | Unset
        if isinstance(_valid_from, Unset):
            valid_from = UNSET
        else:
            valid_from = isoparse(_valid_from)

        _valid_until = d.pop("validUntil", UNSET)
        valid_until: datetime.datetime | Unset
        if isinstance(_valid_until, Unset):
            valid_until = UNSET
        else:
            valid_until = isoparse(_valid_until)

        id = d.pop("id", UNSET)

        traffic_incident = cls(
            description=description,
            type_=type_,
            criticality=criticality,
            valid_from=valid_from,
            valid_until=valid_until,
            id=id,
        )

        traffic_incident.additional_properties = d
        return traffic_incident

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
