from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.postal_code_details_japan_post_postal_code_type import (
    PostalCodeDetailsJapanPostPostalCodeType,
)
from ..models.postal_code_details_japan_post_postal_entity import (
    PostalCodeDetailsJapanPostPostalEntity,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="PostalCodeDetailsJapanPost")


@_attrs_define
class PostalCodeDetailsJapanPost:
    """
    Attributes:
        postal_code (str): **ALPHA**

            7-digit business postal code in `XXX-XXXX` format (separated by dash)
        postal_entity (PostalCodeDetailsJapanPostPostalEntity | Unset): **ALPHA**

            The postal entity. This could be a governmental authority, a regulatory authority, or a designated postal
            operator.

            Description of supported values:

            - **ALPHA** `Japan Post`: Field indicating the data source (fixed as `Japan Post` for Japan)
        postal_code_type (PostalCodeDetailsJapanPostPostalCodeType | Unset): **ALPHA**

            The postal code type.

            Description of supported values:

            - **ALPHA** `ZIP`: Field describing the postal code type (fixed as `ZIP` for Japan)
        business_name (str | Unset): **ALPHA**

            Detailed information specifies company name, building name, floor number, etc. mapped to the corresponding
            business postal code
    """

    postal_code: str
    postal_entity: PostalCodeDetailsJapanPostPostalEntity | Unset = UNSET
    postal_code_type: PostalCodeDetailsJapanPostPostalCodeType | Unset = UNSET
    business_name: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        postal_code = self.postal_code

        postal_entity: str | Unset = UNSET
        if not isinstance(self.postal_entity, Unset):
            postal_entity = self.postal_entity.value

        postal_code_type: str | Unset = UNSET
        if not isinstance(self.postal_code_type, Unset):
            postal_code_type = self.postal_code_type.value

        business_name = self.business_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "postalCode": postal_code,
        })
        if postal_entity is not UNSET:
            field_dict["postalEntity"] = postal_entity
        if postal_code_type is not UNSET:
            field_dict["postalCodeType"] = postal_code_type
        if business_name is not UNSET:
            field_dict["businessName"] = business_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        postal_code = d.pop("postalCode")

        _postal_entity = d.pop("postalEntity", UNSET)
        postal_entity: PostalCodeDetailsJapanPostPostalEntity | Unset
        if isinstance(_postal_entity, Unset):
            postal_entity = UNSET
        else:
            postal_entity = PostalCodeDetailsJapanPostPostalEntity(_postal_entity)

        _postal_code_type = d.pop("postalCodeType", UNSET)
        postal_code_type: PostalCodeDetailsJapanPostPostalCodeType | Unset
        if isinstance(_postal_code_type, Unset):
            postal_code_type = UNSET
        else:
            postal_code_type = PostalCodeDetailsJapanPostPostalCodeType(
                _postal_code_type
            )

        business_name = d.pop("businessName", UNSET)

        postal_code_details_japan_post = cls(
            postal_code=postal_code,
            postal_entity=postal_entity,
            postal_code_type=postal_code_type,
            business_name=business_name,
        )

        postal_code_details_japan_post.additional_properties = d
        return postal_code_details_japan_post

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
