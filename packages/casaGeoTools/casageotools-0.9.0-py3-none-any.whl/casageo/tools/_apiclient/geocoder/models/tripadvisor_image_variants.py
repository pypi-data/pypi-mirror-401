from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.tripadvisor_image_variant import TripadvisorImageVariant


T = TypeVar("T", bound="TripadvisorImageVariants")


@_attrs_define
class TripadvisorImageVariants:
    """
    Attributes:
        thumbnail (TripadvisorImageVariant | Unset):
        small (TripadvisorImageVariant | Unset):
        medium (TripadvisorImageVariant | Unset):
        large (TripadvisorImageVariant | Unset):
        original (TripadvisorImageVariant | Unset):
    """

    thumbnail: TripadvisorImageVariant | Unset = UNSET
    small: TripadvisorImageVariant | Unset = UNSET
    medium: TripadvisorImageVariant | Unset = UNSET
    large: TripadvisorImageVariant | Unset = UNSET
    original: TripadvisorImageVariant | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        thumbnail: dict[str, Any] | Unset = UNSET
        if not isinstance(self.thumbnail, Unset):
            thumbnail = self.thumbnail.to_dict()

        small: dict[str, Any] | Unset = UNSET
        if not isinstance(self.small, Unset):
            small = self.small.to_dict()

        medium: dict[str, Any] | Unset = UNSET
        if not isinstance(self.medium, Unset):
            medium = self.medium.to_dict()

        large: dict[str, Any] | Unset = UNSET
        if not isinstance(self.large, Unset):
            large = self.large.to_dict()

        original: dict[str, Any] | Unset = UNSET
        if not isinstance(self.original, Unset):
            original = self.original.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if thumbnail is not UNSET:
            field_dict["thumbnail"] = thumbnail
        if small is not UNSET:
            field_dict["small"] = small
        if medium is not UNSET:
            field_dict["medium"] = medium
        if large is not UNSET:
            field_dict["large"] = large
        if original is not UNSET:
            field_dict["original"] = original

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tripadvisor_image_variant import TripadvisorImageVariant

        d = dict(src_dict)
        _thumbnail = d.pop("thumbnail", UNSET)
        thumbnail: TripadvisorImageVariant | Unset
        if isinstance(_thumbnail, Unset):
            thumbnail = UNSET
        else:
            thumbnail = TripadvisorImageVariant.from_dict(_thumbnail)

        _small = d.pop("small", UNSET)
        small: TripadvisorImageVariant | Unset
        if isinstance(_small, Unset):
            small = UNSET
        else:
            small = TripadvisorImageVariant.from_dict(_small)

        _medium = d.pop("medium", UNSET)
        medium: TripadvisorImageVariant | Unset
        if isinstance(_medium, Unset):
            medium = UNSET
        else:
            medium = TripadvisorImageVariant.from_dict(_medium)

        _large = d.pop("large", UNSET)
        large: TripadvisorImageVariant | Unset
        if isinstance(_large, Unset):
            large = UNSET
        else:
            large = TripadvisorImageVariant.from_dict(_large)

        _original = d.pop("original", UNSET)
        original: TripadvisorImageVariant | Unset
        if isinstance(_original, Unset):
            original = UNSET
        else:
            original = TripadvisorImageVariant.from_dict(_original)

        tripadvisor_image_variants = cls(
            thumbnail=thumbnail,
            small=small,
            medium=medium,
            large=large,
            original=original,
        )

        tripadvisor_image_variants.additional_properties = d
        return tripadvisor_image_variants

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
