from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.postal_code_details_usps_zip_postal_code_type import (
    PostalCodeDetailsUspsZipPostalCodeType,
)
from ..models.postal_code_details_usps_zip_postal_entity import (
    PostalCodeDetailsUspsZipPostalEntity,
)
from ..models.postal_code_details_usps_zip_zip_classification_code import (
    PostalCodeDetailsUspsZipZipClassificationCode,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="PostalCodeDetailsUspsZip")


@_attrs_define
class PostalCodeDetailsUspsZip:
    """
    Attributes:
        postal_code (str): The postal code.
        postal_entity (PostalCodeDetailsUspsZipPostalEntity | Unset): The postal entity. This could be a governmental
            authority, a regulatory authority, or a designated postal operator.

            Description of supported values:

            - `USPS`: The USPS postal code system.
        postal_code_type (PostalCodeDetailsUspsZipPostalCodeType | Unset): The postal code type. Currently supported
            values: `ZIP` and `ZIP+4`

            Description of supported values:

            - `ZIP`: A 5-digit code that identifies a specific geographic delivery area. ZIP codes can represent an area
            within a state, or a single building or company that has a very high mail volume.
        zip_classification_code (PostalCodeDetailsUspsZipZipClassificationCode | Unset): The ZIP Classification Code.

            Description of supported values:

            - `M`: Military ZIP code.
            - `P`: ZIP code having only Post Office boxes.
            - `U`: Unique ZIP code: A ZIP assigned to a company, agency, or entity with sufficient mail volume, based on
            average daily volume of letter-size pieces.
    """

    postal_code: str
    postal_entity: PostalCodeDetailsUspsZipPostalEntity | Unset = UNSET
    postal_code_type: PostalCodeDetailsUspsZipPostalCodeType | Unset = UNSET
    zip_classification_code: PostalCodeDetailsUspsZipZipClassificationCode | Unset = (
        UNSET
    )
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        postal_code = self.postal_code

        postal_entity: str | Unset = UNSET
        if not isinstance(self.postal_entity, Unset):
            postal_entity = self.postal_entity.value

        postal_code_type: str | Unset = UNSET
        if not isinstance(self.postal_code_type, Unset):
            postal_code_type = self.postal_code_type.value

        zip_classification_code: str | Unset = UNSET
        if not isinstance(self.zip_classification_code, Unset):
            zip_classification_code = self.zip_classification_code.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "postalCode": postal_code,
        })
        if postal_entity is not UNSET:
            field_dict["postalEntity"] = postal_entity
        if postal_code_type is not UNSET:
            field_dict["postalCodeType"] = postal_code_type
        if zip_classification_code is not UNSET:
            field_dict["zipClassificationCode"] = zip_classification_code

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        postal_code = d.pop("postalCode")

        _postal_entity = d.pop("postalEntity", UNSET)
        postal_entity: PostalCodeDetailsUspsZipPostalEntity | Unset
        if isinstance(_postal_entity, Unset):
            postal_entity = UNSET
        else:
            postal_entity = PostalCodeDetailsUspsZipPostalEntity(_postal_entity)

        _postal_code_type = d.pop("postalCodeType", UNSET)
        postal_code_type: PostalCodeDetailsUspsZipPostalCodeType | Unset
        if isinstance(_postal_code_type, Unset):
            postal_code_type = UNSET
        else:
            postal_code_type = PostalCodeDetailsUspsZipPostalCodeType(_postal_code_type)

        _zip_classification_code = d.pop("zipClassificationCode", UNSET)
        zip_classification_code: PostalCodeDetailsUspsZipZipClassificationCode | Unset
        if isinstance(_zip_classification_code, Unset):
            zip_classification_code = UNSET
        else:
            zip_classification_code = PostalCodeDetailsUspsZipZipClassificationCode(
                _zip_classification_code
            )

        postal_code_details_usps_zip = cls(
            postal_code=postal_code,
            postal_entity=postal_entity,
            postal_code_type=postal_code_type,
            zip_classification_code=zip_classification_code,
        )

        postal_code_details_usps_zip.additional_properties = d
        return postal_code_details_usps_zip

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
