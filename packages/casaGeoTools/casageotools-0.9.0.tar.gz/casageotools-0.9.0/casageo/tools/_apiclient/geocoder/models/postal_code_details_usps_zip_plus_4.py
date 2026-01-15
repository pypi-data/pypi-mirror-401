from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.postal_code_details_usps_zip_plus_4_postal_code_type import (
    PostalCodeDetailsUspsZipPlus4PostalCodeType,
)
from ..models.postal_code_details_usps_zip_plus_4_postal_entity import (
    PostalCodeDetailsUspsZipPlus4PostalEntity,
)
from ..models.postal_code_details_usps_zip_plus_4_record_type_code import (
    PostalCodeDetailsUspsZipPlus4RecordTypeCode,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="PostalCodeDetailsUspsZipPlus4")


@_attrs_define
class PostalCodeDetailsUspsZipPlus4:
    """
    Attributes:
        postal_code (str): The postal code.
        postal_entity (PostalCodeDetailsUspsZipPlus4PostalEntity | Unset): The postal entity. This could be a
            governmental authority, a regulatory authority, or a designated postal operator.

            Description of supported values:

            - `USPS`: The USPS postal code system.
        postal_code_type (PostalCodeDetailsUspsZipPlus4PostalCodeType | Unset): The postal code type. Currently
            supported values: `ZIP` and `ZIP+4`

            Description of supported values:

            - `ZIP+4`: Nine-digit code that identifies a small geographic delivery area that is serviceable by a single
            carrier; appears in the last line of the address on a mail piece.
        record_type_code (PostalCodeDetailsUspsZipPlus4RecordTypeCode | Unset): The USPS ZIP+4 Record Type Code.

            Description of supported values:

            - `F`: Firm
            - `G`: General delivery
            - `H`: High-rise
            - `P`: PO Box
            - `R`: Rural route/contract
            - `S`: Street
    """

    postal_code: str
    postal_entity: PostalCodeDetailsUspsZipPlus4PostalEntity | Unset = UNSET
    postal_code_type: PostalCodeDetailsUspsZipPlus4PostalCodeType | Unset = UNSET
    record_type_code: PostalCodeDetailsUspsZipPlus4RecordTypeCode | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        postal_code = self.postal_code

        postal_entity: str | Unset = UNSET
        if not isinstance(self.postal_entity, Unset):
            postal_entity = self.postal_entity.value

        postal_code_type: str | Unset = UNSET
        if not isinstance(self.postal_code_type, Unset):
            postal_code_type = self.postal_code_type.value

        record_type_code: str | Unset = UNSET
        if not isinstance(self.record_type_code, Unset):
            record_type_code = self.record_type_code.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "postalCode": postal_code,
        })
        if postal_entity is not UNSET:
            field_dict["postalEntity"] = postal_entity
        if postal_code_type is not UNSET:
            field_dict["postalCodeType"] = postal_code_type
        if record_type_code is not UNSET:
            field_dict["recordTypeCode"] = record_type_code

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        postal_code = d.pop("postalCode")

        _postal_entity = d.pop("postalEntity", UNSET)
        postal_entity: PostalCodeDetailsUspsZipPlus4PostalEntity | Unset
        if isinstance(_postal_entity, Unset):
            postal_entity = UNSET
        else:
            postal_entity = PostalCodeDetailsUspsZipPlus4PostalEntity(_postal_entity)

        _postal_code_type = d.pop("postalCodeType", UNSET)
        postal_code_type: PostalCodeDetailsUspsZipPlus4PostalCodeType | Unset
        if isinstance(_postal_code_type, Unset):
            postal_code_type = UNSET
        else:
            postal_code_type = PostalCodeDetailsUspsZipPlus4PostalCodeType(
                _postal_code_type
            )

        _record_type_code = d.pop("recordTypeCode", UNSET)
        record_type_code: PostalCodeDetailsUspsZipPlus4RecordTypeCode | Unset
        if isinstance(_record_type_code, Unset):
            record_type_code = UNSET
        else:
            record_type_code = PostalCodeDetailsUspsZipPlus4RecordTypeCode(
                _record_type_code
            )

        postal_code_details_usps_zip_plus_4 = cls(
            postal_code=postal_code,
            postal_entity=postal_entity,
            postal_code_type=postal_code_type,
            record_type_code=record_type_code,
        )

        postal_code_details_usps_zip_plus_4.additional_properties = d
        return postal_code_details_usps_zip_plus_4

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
