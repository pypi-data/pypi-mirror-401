from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.contact import Contact


T = TypeVar("T", bound="ContactInformation")


@_attrs_define
class ContactInformation:
    """
    Attributes:
        phone (list[Contact] | Unset):
        mobile (list[Contact] | Unset):
        toll_free (list[Contact] | Unset):
        fax (list[Contact] | Unset):
        www (list[Contact] | Unset):
        email (list[Contact] | Unset):
    """

    phone: list[Contact] | Unset = UNSET
    mobile: list[Contact] | Unset = UNSET
    toll_free: list[Contact] | Unset = UNSET
    fax: list[Contact] | Unset = UNSET
    www: list[Contact] | Unset = UNSET
    email: list[Contact] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        phone: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.phone, Unset):
            phone = []
            for phone_item_data in self.phone:
                phone_item = phone_item_data.to_dict()
                phone.append(phone_item)

        mobile: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.mobile, Unset):
            mobile = []
            for mobile_item_data in self.mobile:
                mobile_item = mobile_item_data.to_dict()
                mobile.append(mobile_item)

        toll_free: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.toll_free, Unset):
            toll_free = []
            for toll_free_item_data in self.toll_free:
                toll_free_item = toll_free_item_data.to_dict()
                toll_free.append(toll_free_item)

        fax: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.fax, Unset):
            fax = []
            for fax_item_data in self.fax:
                fax_item = fax_item_data.to_dict()
                fax.append(fax_item)

        www: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.www, Unset):
            www = []
            for www_item_data in self.www:
                www_item = www_item_data.to_dict()
                www.append(www_item)

        email: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.email, Unset):
            email = []
            for email_item_data in self.email:
                email_item = email_item_data.to_dict()
                email.append(email_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if phone is not UNSET:
            field_dict["phone"] = phone
        if mobile is not UNSET:
            field_dict["mobile"] = mobile
        if toll_free is not UNSET:
            field_dict["tollFree"] = toll_free
        if fax is not UNSET:
            field_dict["fax"] = fax
        if www is not UNSET:
            field_dict["www"] = www
        if email is not UNSET:
            field_dict["email"] = email

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.contact import Contact

        d = dict(src_dict)
        _phone = d.pop("phone", UNSET)
        phone: list[Contact] | Unset = UNSET
        if _phone is not UNSET:
            phone = []
            for phone_item_data in _phone:
                phone_item = Contact.from_dict(phone_item_data)

                phone.append(phone_item)

        _mobile = d.pop("mobile", UNSET)
        mobile: list[Contact] | Unset = UNSET
        if _mobile is not UNSET:
            mobile = []
            for mobile_item_data in _mobile:
                mobile_item = Contact.from_dict(mobile_item_data)

                mobile.append(mobile_item)

        _toll_free = d.pop("tollFree", UNSET)
        toll_free: list[Contact] | Unset = UNSET
        if _toll_free is not UNSET:
            toll_free = []
            for toll_free_item_data in _toll_free:
                toll_free_item = Contact.from_dict(toll_free_item_data)

                toll_free.append(toll_free_item)

        _fax = d.pop("fax", UNSET)
        fax: list[Contact] | Unset = UNSET
        if _fax is not UNSET:
            fax = []
            for fax_item_data in _fax:
                fax_item = Contact.from_dict(fax_item_data)

                fax.append(fax_item)

        _www = d.pop("www", UNSET)
        www: list[Contact] | Unset = UNSET
        if _www is not UNSET:
            www = []
            for www_item_data in _www:
                www_item = Contact.from_dict(www_item_data)

                www.append(www_item)

        _email = d.pop("email", UNSET)
        email: list[Contact] | Unset = UNSET
        if _email is not UNSET:
            email = []
            for email_item_data in _email:
                email_item = Contact.from_dict(email_item_data)

                email.append(email_item)

        contact_information = cls(
            phone=phone,
            mobile=mobile,
            toll_free=toll_free,
            fax=fax,
            www=www,
            email=email,
        )

        contact_information.additional_properties = d
        return contact_information

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
