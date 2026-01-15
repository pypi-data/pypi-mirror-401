from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.departure import Departure
    from ..models.isoline import Isoline
    from ..models.isoline_response_notice import IsolineResponseNotice


T = TypeVar("T", bound="IsolineResponse")


@_attrs_define
class IsolineResponse:
    """
    Attributes:
        isolines (list[Isoline]): List of polygons calculated per specified range.
        notices (list[IsolineResponseNotice] | Unset): Contains a list of issues related to this isoline calculation.
            Please refer to the `code` attribute for possible values.
        departure (Departure | Unset): Describe a departure or arrival location and time.
        arrival (Departure | Unset): Describe a departure or arrival location and time.
    """

    isolines: list[Isoline]
    notices: list[IsolineResponseNotice] | Unset = UNSET
    departure: Departure | Unset = UNSET
    arrival: Departure | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        isolines = []
        for isolines_item_data in self.isolines:
            isolines_item = isolines_item_data.to_dict()
            isolines.append(isolines_item)

        notices: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.notices, Unset):
            notices = []
            for notices_item_data in self.notices:
                notices_item = notices_item_data.to_dict()
                notices.append(notices_item)

        departure: dict[str, Any] | Unset = UNSET
        if not isinstance(self.departure, Unset):
            departure = self.departure.to_dict()

        arrival: dict[str, Any] | Unset = UNSET
        if not isinstance(self.arrival, Unset):
            arrival = self.arrival.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "isolines": isolines,
        })
        if notices is not UNSET:
            field_dict["notices"] = notices
        if departure is not UNSET:
            field_dict["departure"] = departure
        if arrival is not UNSET:
            field_dict["arrival"] = arrival

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.departure import Departure
        from ..models.isoline import Isoline
        from ..models.isoline_response_notice import IsolineResponseNotice

        d = dict(src_dict)
        isolines = []
        _isolines = d.pop("isolines")
        for isolines_item_data in _isolines:
            isolines_item = Isoline.from_dict(isolines_item_data)

            isolines.append(isolines_item)

        _notices = d.pop("notices", UNSET)
        notices: list[IsolineResponseNotice] | Unset = UNSET
        if _notices is not UNSET:
            notices = []
            for notices_item_data in _notices:
                notices_item = IsolineResponseNotice.from_dict(notices_item_data)

                notices.append(notices_item)

        _departure = d.pop("departure", UNSET)
        departure: Departure | Unset
        if isinstance(_departure, Unset):
            departure = UNSET
        else:
            departure = Departure.from_dict(_departure)

        _arrival = d.pop("arrival", UNSET)
        arrival: Departure | Unset
        if isinstance(_arrival, Unset):
            arrival = UNSET
        else:
            arrival = Departure.from_dict(_arrival)

        isoline_response = cls(
            isolines=isolines,
            notices=notices,
            departure=departure,
            arrival=arrival,
        )

        isoline_response.additional_properties = d
        return isoline_response

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
