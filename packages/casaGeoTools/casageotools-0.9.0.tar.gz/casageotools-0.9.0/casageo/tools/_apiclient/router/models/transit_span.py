from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.localized_string import LocalizedString


T = TypeVar("T", bound="TransitSpan")


@_attrs_define
class TransitSpan:
    r"""Contains information attached to a contiguous part of a `Section`. The information may be
    attached along different dimensions of a section which are geometry (spatial), distance or
    time.

    A section, if it uses spans, has an optional attribute `spans` which is an array of
    extended `Span` types.

    The attributes of a span which should be returned in the response are
    configured by a request parameter.

    Use this type as a base for any span extension for sections that provide spans.

        Attributes:
            offset (int | Unset): Offset of a coordinate in the section's polyline.
            length (int | Unset): Distance in meters. Example: 189.
            duration (int | Unset): Duration in seconds. Example: 198.
            country_code (str | Unset): ISO-3166-1 alpha-3 code Example: FRA.
            state_code (str | Unset): The second part of an ISO-3166-2 code (e.g., `TX` from `USA-TX`) consists of up to
                three alphanumeric characters.
                It is used to identify the principal subdivisions (e.g., provinces or states) of a country in conjunction with a
                CountryCode

                Note: State codes may not be available in some countries.
            names (list[LocalizedString] | Unset): Designated name for the span (e.g. a street name or a transport name)
            segment_id (str | Unset): **NOTE:** Attribute segmentId is deprecated. Use segmentRef instead.

                The directed topology segment id including prefix (e.g '+here:cm:segment:').

                The id consists of two parts.
                * The direction ('+' or '-')
                * followed by the topology segment id (a unique identifier within the HERE platform catalogs).

                The direction specifies whether the route is using the segment in its canonical direction ('+' aka traveling
                along the geometry's direction), or against it ('-' aka traveling against the geometry's direction).

                This attribute will not appear for HERE Public Transit v8 and HERE Intermodal Routing v8 requests
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
            notices (list[int] | Unset): A list of indexes into the notices array of the parent section.
                References all notices that apply to the span.
    """

    offset: int | Unset = UNSET
    length: int | Unset = UNSET
    duration: int | Unset = UNSET
    country_code: str | Unset = UNSET
    state_code: str | Unset = UNSET
    names: list[LocalizedString] | Unset = UNSET
    segment_id: str | Unset = UNSET
    segment_ref: str | Unset = UNSET
    notices: list[int] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offset = self.offset

        length = self.length

        duration = self.duration

        country_code = self.country_code

        state_code = self.state_code

        names: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.names, Unset):
            names = []
            for names_item_data in self.names:
                names_item = names_item_data.to_dict()
                names.append(names_item)

        segment_id = self.segment_id

        segment_ref = self.segment_ref

        notices: list[int] | Unset = UNSET
        if not isinstance(self.notices, Unset):
            notices = self.notices

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if offset is not UNSET:
            field_dict["offset"] = offset
        if length is not UNSET:
            field_dict["length"] = length
        if duration is not UNSET:
            field_dict["duration"] = duration
        if country_code is not UNSET:
            field_dict["countryCode"] = country_code
        if state_code is not UNSET:
            field_dict["stateCode"] = state_code
        if names is not UNSET:
            field_dict["names"] = names
        if segment_id is not UNSET:
            field_dict["segmentId"] = segment_id
        if segment_ref is not UNSET:
            field_dict["segmentRef"] = segment_ref
        if notices is not UNSET:
            field_dict["notices"] = notices

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.localized_string import LocalizedString

        d = dict(src_dict)
        offset = d.pop("offset", UNSET)

        length = d.pop("length", UNSET)

        duration = d.pop("duration", UNSET)

        country_code = d.pop("countryCode", UNSET)

        state_code = d.pop("stateCode", UNSET)

        _names = d.pop("names", UNSET)
        names: list[LocalizedString] | Unset = UNSET
        if _names is not UNSET:
            names = []
            for names_item_data in _names:
                names_item = LocalizedString.from_dict(names_item_data)

                names.append(names_item)

        segment_id = d.pop("segmentId", UNSET)

        segment_ref = d.pop("segmentRef", UNSET)

        notices = cast(list[int], d.pop("notices", UNSET))

        transit_span = cls(
            offset=offset,
            length=length,
            duration=duration,
            country_code=country_code,
            state_code=state_code,
            names=names,
            segment_id=segment_id,
            segment_ref=segment_ref,
            notices=notices,
        )

        transit_span.additional_properties = d
        return transit_span

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
