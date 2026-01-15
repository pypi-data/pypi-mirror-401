from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.admin_names_preference import AdminNamesPreference
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.name import Name


T = TypeVar("T", bound="AdminNames")


@_attrs_define
class AdminNames:
    """
    Attributes:
        names (list[Name]): The list of all values for a name. Those might be for different languages or different name
            types.
        preference (AdminNamesPreference | Unset): The preference of the view on an address field expressed by this
            group of names.

            Description of supported values:

            - `alternative`: Alternative view on this address field. Names of this group are exposed in the result only if
            matching to the query so that the end-user can better recognize the result.
            - `primary`: The default or only view on this address filed. These are the names which are exposed in the result
            by default.
    """

    names: list[Name]
    preference: AdminNamesPreference | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        names = []
        for names_item_data in self.names:
            names_item = names_item_data.to_dict()
            names.append(names_item)

        preference: str | Unset = UNSET
        if not isinstance(self.preference, Unset):
            preference = self.preference.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "names": names,
        })
        if preference is not UNSET:
            field_dict["preference"] = preference

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.name import Name

        d = dict(src_dict)
        names = []
        _names = d.pop("names")
        for names_item_data in _names:
            names_item = Name.from_dict(names_item_data)

            names.append(names_item)

        _preference = d.pop("preference", UNSET)
        preference: AdminNamesPreference | Unset
        if isinstance(_preference, Unset):
            preference = UNSET
        else:
            preference = AdminNamesPreference(_preference)

        admin_names = cls(
            names=names,
            preference=preference,
        )

        admin_names.additional_properties = d
        return admin_names

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
