from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.open_search_multi_reverse_geocode_error_result import (
        OpenSearchMultiReverseGeocodeErrorResult,
    )
    from ..models.open_search_multi_reverse_geocode_response_item import (
        OpenSearchMultiReverseGeocodeResponseItem,
    )


T = TypeVar("T", bound="OpenSearchMultiReverseGeocodeResponse")


@_attrs_define
class OpenSearchMultiReverseGeocodeResponse:
    """
    Attributes:
        results (list[OpenSearchMultiReverseGeocodeErrorResult | OpenSearchMultiReverseGeocodeResponseItem]): The
            results for the individual queries which either contain items or an error description
    """

    results: list[
        OpenSearchMultiReverseGeocodeErrorResult
        | OpenSearchMultiReverseGeocodeResponseItem
    ]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.open_search_multi_reverse_geocode_error_result import (
            OpenSearchMultiReverseGeocodeErrorResult,
        )

        results = []
        for results_item_data in self.results:
            results_item: dict[str, Any]
            if isinstance(results_item_data, OpenSearchMultiReverseGeocodeErrorResult):
                results_item = results_item_data.to_dict()
            else:
                results_item = results_item_data.to_dict()

            results.append(results_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "results": results,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.open_search_multi_reverse_geocode_error_result import (
            OpenSearchMultiReverseGeocodeErrorResult,
        )
        from ..models.open_search_multi_reverse_geocode_response_item import (
            OpenSearchMultiReverseGeocodeResponseItem,
        )

        d = dict(src_dict)
        results = []
        _results = d.pop("results")
        for results_item_data in _results:

            def _parse_results_item(
                data: object,
            ) -> (
                OpenSearchMultiReverseGeocodeErrorResult
                | OpenSearchMultiReverseGeocodeResponseItem
            ):
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    results_item_type_0 = (
                        OpenSearchMultiReverseGeocodeErrorResult.from_dict(data)
                    )

                    return results_item_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                results_item_type_1 = (
                    OpenSearchMultiReverseGeocodeResponseItem.from_dict(data)
                )

                return results_item_type_1

            results_item = _parse_results_item(results_item_data)

            results.append(results_item)

        open_search_multi_reverse_geocode_response = cls(
            results=results,
        )

        open_search_multi_reverse_geocode_response.additional_properties = d
        return open_search_multi_reverse_geocode_response

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
