from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.signpost_label_route_number import SignpostLabelRouteNumber
    from ..models.signpost_label_text import SignpostLabelText


T = TypeVar("T", bound="SignpostInfo")


@_attrs_define
class SignpostInfo:
    """Signpost information attached to an offset action.

    Example:
        {'$ref': '#/components/examples/routeResponseManeuverSignpostInfoExample'}

    Attributes:
        labels (list[SignpostLabelRouteNumber | SignpostLabelText]): Part of a signpost representing particular
            direction or destination.
    """

    labels: list[SignpostLabelRouteNumber | SignpostLabelText]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.signpost_label_text import SignpostLabelText

        labels = []
        for labels_item_data in self.labels:
            labels_item: dict[str, Any]
            if isinstance(labels_item_data, SignpostLabelText):
                labels_item = labels_item_data.to_dict()
            else:
                labels_item = labels_item_data.to_dict()

            labels.append(labels_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "labels": labels,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.signpost_label_route_number import SignpostLabelRouteNumber
        from ..models.signpost_label_text import SignpostLabelText

        d = dict(src_dict)
        labels = []
        _labels = d.pop("labels")
        for labels_item_data in _labels:

            def _parse_labels_item(
                data: object,
            ) -> SignpostLabelRouteNumber | SignpostLabelText:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_signpost_label_type_0 = (
                        SignpostLabelText.from_dict(data)
                    )

                    return componentsschemas_signpost_label_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_signpost_label_type_1 = (
                    SignpostLabelRouteNumber.from_dict(data)
                )

                return componentsschemas_signpost_label_type_1

            labels_item = _parse_labels_item(labels_item_data)

            labels.append(labels_item)

        signpost_info = cls(
            labels=labels,
        )

        signpost_info.additional_properties = d
        return signpost_info

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
