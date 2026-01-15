from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.ev_charging_attributes_access import EvChargingAttributesAccess
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.e_mobility_service_provider import EMobilityServiceProvider
    from ..models.ev_connector import EvConnector
    from ..models.ev_payment_support import EvPaymentSupport


T = TypeVar("T", bound="EvChargingAttributes")


@_attrs_define
class EvChargingAttributes:
    """
    Attributes:
        connectors (list[EvConnector] | Unset): List of EV pool groups of connectors. Each group is defined by a common
            charging connector type and max power level. The numberOfConnectors field contains the number of connectors in
            the group.
        total_number_of_connectors (int | Unset): Total number of charging connectors in the EV charging pool
        access (EvChargingAttributesAccess | Unset): Information about accessibility
        e_mobility_service_providers (list[EMobilityServiceProvider] | Unset): The list of eMSP (e-Mobility Service
            Provider) for which the EV station operator has EV roaming agreements.
            Each element contains both the name and the partner ID of the eMSP.
        payment_methods (list[EvPaymentSupport] | Unset): List of payment methods supported at the EV station
    """

    connectors: list[EvConnector] | Unset = UNSET
    total_number_of_connectors: int | Unset = UNSET
    access: EvChargingAttributesAccess | Unset = UNSET
    e_mobility_service_providers: list[EMobilityServiceProvider] | Unset = UNSET
    payment_methods: list[EvPaymentSupport] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        connectors: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.connectors, Unset):
            connectors = []
            for connectors_item_data in self.connectors:
                connectors_item = connectors_item_data.to_dict()
                connectors.append(connectors_item)

        total_number_of_connectors = self.total_number_of_connectors

        access: str | Unset = UNSET
        if not isinstance(self.access, Unset):
            access = self.access.value

        e_mobility_service_providers: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.e_mobility_service_providers, Unset):
            e_mobility_service_providers = []
            for (
                e_mobility_service_providers_item_data
            ) in self.e_mobility_service_providers:
                e_mobility_service_providers_item = (
                    e_mobility_service_providers_item_data.to_dict()
                )
                e_mobility_service_providers.append(e_mobility_service_providers_item)

        payment_methods: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.payment_methods, Unset):
            payment_methods = []
            for payment_methods_item_data in self.payment_methods:
                payment_methods_item = payment_methods_item_data.to_dict()
                payment_methods.append(payment_methods_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if connectors is not UNSET:
            field_dict["connectors"] = connectors
        if total_number_of_connectors is not UNSET:
            field_dict["totalNumberOfConnectors"] = total_number_of_connectors
        if access is not UNSET:
            field_dict["access"] = access
        if e_mobility_service_providers is not UNSET:
            field_dict["eMobilityServiceProviders"] = e_mobility_service_providers
        if payment_methods is not UNSET:
            field_dict["paymentMethods"] = payment_methods

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.e_mobility_service_provider import EMobilityServiceProvider
        from ..models.ev_connector import EvConnector
        from ..models.ev_payment_support import EvPaymentSupport

        d = dict(src_dict)
        _connectors = d.pop("connectors", UNSET)
        connectors: list[EvConnector] | Unset = UNSET
        if _connectors is not UNSET:
            connectors = []
            for connectors_item_data in _connectors:
                connectors_item = EvConnector.from_dict(connectors_item_data)

                connectors.append(connectors_item)

        total_number_of_connectors = d.pop("totalNumberOfConnectors", UNSET)

        _access = d.pop("access", UNSET)
        access: EvChargingAttributesAccess | Unset
        if isinstance(_access, Unset):
            access = UNSET
        else:
            access = EvChargingAttributesAccess(_access)

        _e_mobility_service_providers = d.pop("eMobilityServiceProviders", UNSET)
        e_mobility_service_providers: list[EMobilityServiceProvider] | Unset = UNSET
        if _e_mobility_service_providers is not UNSET:
            e_mobility_service_providers = []
            for e_mobility_service_providers_item_data in _e_mobility_service_providers:
                e_mobility_service_providers_item = EMobilityServiceProvider.from_dict(
                    e_mobility_service_providers_item_data
                )

                e_mobility_service_providers.append(e_mobility_service_providers_item)

        _payment_methods = d.pop("paymentMethods", UNSET)
        payment_methods: list[EvPaymentSupport] | Unset = UNSET
        if _payment_methods is not UNSET:
            payment_methods = []
            for payment_methods_item_data in _payment_methods:
                payment_methods_item = EvPaymentSupport.from_dict(
                    payment_methods_item_data
                )

                payment_methods.append(payment_methods_item)

        ev_charging_attributes = cls(
            connectors=connectors,
            total_number_of_connectors=total_number_of_connectors,
            access=access,
            e_mobility_service_providers=e_mobility_service_providers,
            payment_methods=payment_methods,
        )

        ev_charging_attributes.additional_properties = d
        return ev_charging_attributes

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
