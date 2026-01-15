from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.ev_station_connector_type_ids_item import EvStationConnectorTypeIdsItem
from ..models.ev_station_current import EvStationCurrent
from ..models.ev_station_payment_method_ids_item import EvStationPaymentMethodIdsItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="EvStation")


@_attrs_define
class EvStation:
    """
    Attributes:
        payment_method_ids (list[EvStationPaymentMethodIdsItem] | Unset): Filter to retrieve Electric Vehicle charging
            stations by supported payment types

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
        e_mobility_service_provider_partner_ids (list[str] | Unset): Filter to retrieve Electric Vehicle charging
            stations by value of e-Mobility Service Providers
            (eMSP) partner ID. EV roaming enables EV drivers to be charged using subscription cards from eMSP.
            Several partner IDs can be set as value this filter, separated with a comma.
            The list of eMSP partner IDs supported by this filter can be retrieved using the EV Charge Points API
            [`roaming`](https://www.here.com/docs/bundle/ev-charge-points-api-developer-guide/page/topics/resource-
            roamings.html)
            resource. Example: ['1f351b84-cca5-11ed-8155-42010aa40002', '1f39ad02-cca5-11ed-9d1a-42010aa40002'].
        current (EvStationCurrent | Unset): Filter to retrieve Electric Vehicle charging stations by current type

            Description of supported values:

            - `AC`: Alternating current
            - `DC`: Direct current Example: AC.
        supplier_names (list[str] | Unset): Filter to retrieve Electric Vehicle charging stations with at least one
            connector of supplier name in the filter
        connector_type_ids (list[EvStationConnectorTypeIdsItem] | Unset): Filter to retrieve Electric Vehicle charging
            stations with at least a connector type ID

            Description of supported values:

            - `10`: Domestic plug/socket type E+F (CEE 7/7)
            - `11`: Domestic plug/socket type G (BS 1363, IS 401 & 411, MS 58)
            - `12`: Domestic plug/socket type H (SI 32)
            - `13`: Domestic plug/socket type I (AS/NZS 3112)
            - `14`: Domestic plug/socket type I (CPCS-CCC)
            - `15`: Domestic plug/socket type I (IRAM 2073)
            - `20`: Domestic plug/socket type K (Section 107-2-D1)
            - `21`: Domestic plug/socket type K (Thailand TIS 166 - 2549)
            - `22`: Domestic plug/socket type L (CEI 23-16/VII)
            - `23`: Domestic plug/socket type M (South African 15 A/250 V)
            - `24`: Domestic plug/socket type IEC 60906-1 (3 pin)
            - `25`: AVCON Connector
            - `29`: JEVS G 105 (CHAdeMO)
            - `30`: IEC 62196-2 type 1 (SAE J1772)
            - `31`: IEC 62196-2 type 2 (Mennekes)
            - `32`: IEC 62196-2 type 3c (SCAME)
            - `33`: IEC 62196-3 type 1 combo (SAE J1772)
            - `34`: IEC 62196-3 type 2 combo (Mennekes)
            - `35`: IEC 60309 : industrial P + N + E (AC)
            - `36`: IEC 60309 : industrial 3P + E + N (AC)
            - `37`: IEC 60309 : industrial 2P + E (AC)
            - `42`: Domestic plug/socket type J (SEV 1011) (T13, T23)
            - `43`: Tesla Connector
            - `46`: IEC 60309 : industrial 2P + E (DC)
            - `48`: Domestic plug/socket type A (NEMA 1-15, 2 pins)
            - `49`: Domestic plug/socket type C (CEE 7/17, 2 pins)
            - `5`: Domestic plug/socket type B (NEMA 5-15)
            - `50`: IEC 62196-2 type 3a (SCAME)
            - `52`: GB/T (Chinese) AC connector
            - `53`: GB/T (Chinese) DC connector
            - `6`: Domestic plug/socket type B (NEMA 5-20)
            - `7`: Domestic plug/socket type D (BS 546 (3 pin))
            - `8`: Domestic plug/socket type E (CEE 7/5)
            - `9`: Domestic plug/socket type F (CEE 7/4 (Schuko))
        min_power (float | Unset): Minimum charging power in KW that each returned EV station must support in at least
            one of its supply element Example: 6.6.
    """

    payment_method_ids: list[EvStationPaymentMethodIdsItem] | Unset = UNSET
    e_mobility_service_provider_partner_ids: list[str] | Unset = UNSET
    current: EvStationCurrent | Unset = UNSET
    supplier_names: list[str] | Unset = UNSET
    connector_type_ids: list[EvStationConnectorTypeIdsItem] | Unset = UNSET
    min_power: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payment_method_ids: list[str] | Unset = UNSET
        if not isinstance(self.payment_method_ids, Unset):
            payment_method_ids = []
            for payment_method_ids_item_data in self.payment_method_ids:
                payment_method_ids_item = payment_method_ids_item_data.value
                payment_method_ids.append(payment_method_ids_item)

        e_mobility_service_provider_partner_ids: list[str] | Unset = UNSET
        if not isinstance(self.e_mobility_service_provider_partner_ids, Unset):
            e_mobility_service_provider_partner_ids = (
                self.e_mobility_service_provider_partner_ids
            )

        current: str | Unset = UNSET
        if not isinstance(self.current, Unset):
            current = self.current.value

        supplier_names: list[str] | Unset = UNSET
        if not isinstance(self.supplier_names, Unset):
            supplier_names = self.supplier_names

        connector_type_ids: list[str] | Unset = UNSET
        if not isinstance(self.connector_type_ids, Unset):
            connector_type_ids = []
            for connector_type_ids_item_data in self.connector_type_ids:
                connector_type_ids_item = connector_type_ids_item_data.value
                connector_type_ids.append(connector_type_ids_item)

        min_power = self.min_power

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if payment_method_ids is not UNSET:
            field_dict["paymentMethodIds"] = payment_method_ids
        if e_mobility_service_provider_partner_ids is not UNSET:
            field_dict["eMobilityServiceProviderPartnerIds"] = (
                e_mobility_service_provider_partner_ids
            )
        if current is not UNSET:
            field_dict["current"] = current
        if supplier_names is not UNSET:
            field_dict["supplierNames"] = supplier_names
        if connector_type_ids is not UNSET:
            field_dict["connectorTypeIds"] = connector_type_ids
        if min_power is not UNSET:
            field_dict["minPower"] = min_power

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _payment_method_ids = d.pop("paymentMethodIds", UNSET)
        payment_method_ids: list[EvStationPaymentMethodIdsItem] | Unset = UNSET
        if _payment_method_ids is not UNSET:
            payment_method_ids = []
            for payment_method_ids_item_data in _payment_method_ids:
                payment_method_ids_item = EvStationPaymentMethodIdsItem(
                    payment_method_ids_item_data
                )

                payment_method_ids.append(payment_method_ids_item)

        e_mobility_service_provider_partner_ids = cast(
            list[str], d.pop("eMobilityServiceProviderPartnerIds", UNSET)
        )

        _current = d.pop("current", UNSET)
        current: EvStationCurrent | Unset
        if isinstance(_current, Unset):
            current = UNSET
        else:
            current = EvStationCurrent(_current)

        supplier_names = cast(list[str], d.pop("supplierNames", UNSET))

        _connector_type_ids = d.pop("connectorTypeIds", UNSET)
        connector_type_ids: list[EvStationConnectorTypeIdsItem] | Unset = UNSET
        if _connector_type_ids is not UNSET:
            connector_type_ids = []
            for connector_type_ids_item_data in _connector_type_ids:
                connector_type_ids_item = EvStationConnectorTypeIdsItem(
                    connector_type_ids_item_data
                )

                connector_type_ids.append(connector_type_ids_item)

        min_power = d.pop("minPower", UNSET)

        ev_station = cls(
            payment_method_ids=payment_method_ids,
            e_mobility_service_provider_partner_ids=e_mobility_service_provider_partner_ids,
            current=current,
            supplier_names=supplier_names,
            connector_type_ids=connector_type_ids,
            min_power=min_power,
        )

        ev_station.additional_properties = d
        return ev_station

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
