from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.ev_payment_support_id import EvPaymentSupportId

T = TypeVar("T", bound="EvPaymentSupport")


@_attrs_define
class EvPaymentSupport:
    """
    Attributes:
        id (EvPaymentSupportId): payment method identifier.

            Description of supported values:

            - `authByCarPlugAndCharge`: indicates whether this EV station supports Plug&Charge.ISO 15118 Plug&Charge enables
            drivers to plug in and charge up instantly using automatic EV-to-charging station authentication technology.
            - `creditCard`: indicates if this EV station accepts credit card payment or not.
            - `debitCard`: indicates if this EV station accepts debit card payment or not.
            - `onlineApplePay`: indicates whether this EV station accepts Apple Pay (TM) authentication and payment method.
            - `onlineGooglePay`:  indicates whether this EV station accepts Google Pay (TM) authentication and payment
            method.
            - `onlinePaypal`: indicates whether this EV station accepts PayPal (TM) authentication and payment method.
            - `operatorApp`: indicates whether this EV station support authentication and payment through an app from the
            Charging Point Operator.
        accepted (bool): set to `true` if the related payment method is accepted at the EV station
    """

    id: EvPaymentSupportId
    accepted: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id.value

        accepted = self.accepted

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "accepted": accepted,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = EvPaymentSupportId(d.pop("id"))

        accepted = d.pop("accepted")

        ev_payment_support = cls(
            id=id,
            accepted=accepted,
        )

        ev_payment_support.additional_properties = d
        return ev_payment_support

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
