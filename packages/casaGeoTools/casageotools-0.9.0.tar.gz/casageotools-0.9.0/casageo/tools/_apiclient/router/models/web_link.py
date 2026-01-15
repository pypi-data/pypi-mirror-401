from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="WebLink")


@_attrs_define
class WebLink:
    """The URL address to an external resource.

    Example:
        {'id': '88-7568-21.07.2023', 'text': 'Information for public transit provided by ThePublicTransit GmbH'}

    Attributes:
        id (str): Unique identifier for the web link. It is used to deduplicate links defined in multiple sections.
        text (str): Text describing the url address (e.g. The example website).
        href (str | Unset): An URL address that links to a particular resource. Example:
            https://url.address.com/resource.
        href_text (str | Unset): The interactive (or clickable) portion of the text. If not present (default), the
            entire content of the text attribute will be considered.
    """

    id: str
    text: str
    href: str | Unset = UNSET
    href_text: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        text = self.text

        href = self.href

        href_text = self.href_text

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "text": text,
        })
        if href is not UNSET:
            field_dict["href"] = href
        if href_text is not UNSET:
            field_dict["hrefText"] = href_text

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        text = d.pop("text")

        href = d.pop("href", UNSET)

        href_text = d.pop("hrefText", UNSET)

        web_link = cls(
            id=id,
            text=text,
            href=href,
            href_text=href_text,
        )

        web_link.additional_properties = d
        return web_link

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
