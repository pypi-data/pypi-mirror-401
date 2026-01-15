from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.editorial_media_collection import EditorialMediaCollection
    from ..models.image_media_collection import ImageMediaCollection
    from ..models.rating_media_collection import RatingMediaCollection


T = TypeVar("T", bound="Media")


@_attrs_define
class Media:
    """
    Attributes:
        images (ImageMediaCollection | Unset):
        editorials (EditorialMediaCollection | Unset):
        ratings (RatingMediaCollection | Unset):
    """

    images: ImageMediaCollection | Unset = UNSET
    editorials: EditorialMediaCollection | Unset = UNSET
    ratings: RatingMediaCollection | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        images: dict[str, Any] | Unset = UNSET
        if not isinstance(self.images, Unset):
            images = self.images.to_dict()

        editorials: dict[str, Any] | Unset = UNSET
        if not isinstance(self.editorials, Unset):
            editorials = self.editorials.to_dict()

        ratings: dict[str, Any] | Unset = UNSET
        if not isinstance(self.ratings, Unset):
            ratings = self.ratings.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if images is not UNSET:
            field_dict["images"] = images
        if editorials is not UNSET:
            field_dict["editorials"] = editorials
        if ratings is not UNSET:
            field_dict["ratings"] = ratings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.editorial_media_collection import EditorialMediaCollection
        from ..models.image_media_collection import ImageMediaCollection
        from ..models.rating_media_collection import RatingMediaCollection

        d = dict(src_dict)
        _images = d.pop("images", UNSET)
        images: ImageMediaCollection | Unset
        if isinstance(_images, Unset):
            images = UNSET
        else:
            images = ImageMediaCollection.from_dict(_images)

        _editorials = d.pop("editorials", UNSET)
        editorials: EditorialMediaCollection | Unset
        if isinstance(_editorials, Unset):
            editorials = UNSET
        else:
            editorials = EditorialMediaCollection.from_dict(_editorials)

        _ratings = d.pop("ratings", UNSET)
        ratings: RatingMediaCollection | Unset
        if isinstance(_ratings, Unset):
            ratings = UNSET
        else:
            ratings = RatingMediaCollection.from_dict(_ratings)

        media = cls(
            images=images,
            editorials=editorials,
            ratings=ratings,
        )

        media.additional_properties = d
        return media

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
