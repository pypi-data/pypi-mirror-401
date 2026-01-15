from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="TransitIncident")


@_attrs_define
class TransitIncident:
    """An incident describes disruptions on the transit network.
    Disruptions scale from delays to service cancellations.

        Example:
            {'summary': 'The subway is closed each night between 1 AM and 5 AM.', 'description': 'The subway is closed each
                night between 1 AM and 5 AM while we clean our trains and stations. We are running extra bus service
                overnight.', 'type': 'maintenance', 'effect': 'modifiedService'}

        Attributes:
            type_ (str): Extensible enum: `technicalProblem` `strike` `demonstration` `accident` `holiday` `weather`
                `maintenance` `construction` `policeActivity` `medicalEmergency` `other` `...`
                An open list of possible incident causes / types.
                Note: Since new types are expected to appear, it is important to check for unknown types when parsing this
                value.
            effect (str): Extensible enum: `cancelledService` `reducedService` `additionalService` `modifiedService`
                `delays` `detour` `stopMoved` `other` `...`
                An open list of possible incident effects.
                Note: Since new types are expected to appear, it is important to check for unknown types when parsing this
                value.
            summary (str | Unset): A human readable summary of the incident Example: The subway is closed each night between
                1 AM and 5 AM..
            description (str | Unset): A human readable description of the incident Example: The subway is closed each night
                between 1 AM and 5 AM while we clean our trains and stations. We are running extra bus service overnight..
            valid_from (datetime.datetime | Unset): **RFC 3339**, section 5.6 as defined by either `date-time` or `date-
                only` 'T' `partial-time` (ie no time-offset).
            valid_until (datetime.datetime | Unset): **RFC 3339**, section 5.6 as defined by either `date-time` or `date-
                only` 'T' `partial-time` (ie no time-offset).
            url (str | Unset): An URL address that links to a particular resource. Example:
                https://url.address.com/resource.
    """

    type_: str
    effect: str
    summary: str | Unset = UNSET
    description: str | Unset = UNSET
    valid_from: datetime.datetime | Unset = UNSET
    valid_until: datetime.datetime | Unset = UNSET
    url: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        effect = self.effect

        summary = self.summary

        description = self.description

        valid_from: str | Unset = UNSET
        if not isinstance(self.valid_from, Unset):
            valid_from = self.valid_from.isoformat()

        valid_until: str | Unset = UNSET
        if not isinstance(self.valid_until, Unset):
            valid_until = self.valid_until.isoformat()

        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "effect": effect,
        })
        if summary is not UNSET:
            field_dict["summary"] = summary
        if description is not UNSET:
            field_dict["description"] = description
        if valid_from is not UNSET:
            field_dict["validFrom"] = valid_from
        if valid_until is not UNSET:
            field_dict["validUntil"] = valid_until
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        effect = d.pop("effect")

        summary = d.pop("summary", UNSET)

        description = d.pop("description", UNSET)

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

        url = d.pop("url", UNSET)

        transit_incident = cls(
            type_=type_,
            effect=effect,
            summary=summary,
            description=description,
            valid_from=valid_from,
            valid_until=valid_until,
            url=url,
        )

        transit_incident.additional_properties = d
        return transit_incident

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
