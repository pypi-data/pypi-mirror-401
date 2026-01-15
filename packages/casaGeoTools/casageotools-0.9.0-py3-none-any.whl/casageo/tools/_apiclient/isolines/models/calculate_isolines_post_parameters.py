from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.avoid_post import AvoidPost
    from ..models.exclude_post import ExcludePost
    from ..models.max_speed_on_segment_post_inner import MaxSpeedOnSegmentPostInner


T = TypeVar("T", bound="CalculateIsolinesPostParameters")


@_attrs_define
class CalculateIsolinesPostParameters:
    """Parameters of the POST body for isoline calculation

    Attributes:
        avoid (AvoidPost | Unset): Avoid routes that violate certain features of road network or that go through
            user-specified geographical bounding boxes.

            For the general description of the functionality please refer to the `avoid` parameter of the
            query string.

            Passing parameters in the POST body is suggested when the length of the parameters exceeds the
            limitation of the GET request.
        exclude (ExcludePost | Unset): User-specified properties that need to be strictly excluded during route
            calculation.

            For the general description of the functionality please refer to the `exclude` parameter of the
            query string.

            Passing parameters in the POST body is suggested when the length of the parameters exceeds the
            limitation of the GET request.
        max_speed_on_segment (list[MaxSpeedOnSegmentPostInner] | Unset): Segments with restrictions on maximum
            `baseSpeed`.

            For the general description of the functionality please refer to the `maxSpeedOnSegment` parameter of the
            query string.

            Passing parameters in the POST body is suggested when the length of the parameters exceeds the
            limitation of the GET request.

            Example of a parameter value excluding two segments:
            ```
            [
              {
                "segment": "here:cm:segment:207551710#+",
                "speed": 10
              },
              {
                "segment": "here:cm:segment:76771992",
                "speed": 1
              }
            ]
            ```

            **Notes**:
            - Maximum number of penalized segments in one request cannot be greater than 1000.
              "penalized segments" refer to segments that have a restrictions on maximum baseSpeed with `maxSpeedOnSegment`
              or avoided with `avoid[segments]`.
            - In case the same segment is penalized multiple times through values provided in the query string and/or the
            POST body,
              then the most restrictive value will be applied.
    """

    avoid: AvoidPost | Unset = UNSET
    exclude: ExcludePost | Unset = UNSET
    max_speed_on_segment: list[MaxSpeedOnSegmentPostInner] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        avoid: dict[str, Any] | Unset = UNSET
        if not isinstance(self.avoid, Unset):
            avoid = self.avoid.to_dict()

        exclude: dict[str, Any] | Unset = UNSET
        if not isinstance(self.exclude, Unset):
            exclude = self.exclude.to_dict()

        max_speed_on_segment: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.max_speed_on_segment, Unset):
            max_speed_on_segment = []
            for (
                componentsschemas_max_speed_on_segment_post_item_data
            ) in self.max_speed_on_segment:
                componentsschemas_max_speed_on_segment_post_item = (
                    componentsschemas_max_speed_on_segment_post_item_data.to_dict()
                )
                max_speed_on_segment.append(
                    componentsschemas_max_speed_on_segment_post_item
                )

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if avoid is not UNSET:
            field_dict["avoid"] = avoid
        if exclude is not UNSET:
            field_dict["exclude"] = exclude
        if max_speed_on_segment is not UNSET:
            field_dict["maxSpeedOnSegment"] = max_speed_on_segment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.avoid_post import AvoidPost
        from ..models.exclude_post import ExcludePost
        from ..models.max_speed_on_segment_post_inner import MaxSpeedOnSegmentPostInner

        d = dict(src_dict)
        _avoid = d.pop("avoid", UNSET)
        avoid: AvoidPost | Unset
        if isinstance(_avoid, Unset):
            avoid = UNSET
        else:
            avoid = AvoidPost.from_dict(_avoid)

        _exclude = d.pop("exclude", UNSET)
        exclude: ExcludePost | Unset
        if isinstance(_exclude, Unset):
            exclude = UNSET
        else:
            exclude = ExcludePost.from_dict(_exclude)

        _max_speed_on_segment = d.pop("maxSpeedOnSegment", UNSET)
        max_speed_on_segment: list[MaxSpeedOnSegmentPostInner] | Unset = UNSET
        if _max_speed_on_segment is not UNSET:
            max_speed_on_segment = []
            for (
                componentsschemas_max_speed_on_segment_post_item_data
            ) in _max_speed_on_segment:
                componentsschemas_max_speed_on_segment_post_item = (
                    MaxSpeedOnSegmentPostInner.from_dict(
                        componentsschemas_max_speed_on_segment_post_item_data
                    )
                )

                max_speed_on_segment.append(
                    componentsschemas_max_speed_on_segment_post_item
                )

        calculate_isolines_post_parameters = cls(
            avoid=avoid,
            exclude=exclude,
            max_speed_on_segment=max_speed_on_segment,
        )

        calculate_isolines_post_parameters.additional_properties = d
        return calculate_isolines_post_parameters

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
