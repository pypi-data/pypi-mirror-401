from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RoutingZone")


@_attrs_define
class RoutingZone:
    r"""Information about a routing zone.

    Attributes:
        ref (str | Unset): A reference to a routing zone in HMC.

            The standard representation of a routing zone reference has the following structure:
            `{catalogHrn}:{catalogVersion}:({layerId})?:{tileId}:{zoneId}`

            The individual parts are:
            * `catalogHrn`: The HERE Resource Name that identifies the source catalog of the routing zone, example:
            `hrn:here:data::olp-here:rib-2`
            * `catalogVersion`: The catalog version
            * `layerId` (optional): The layer inside the catalog where the routing zone is located, example: `environmental-
            zones`
            * `tileId`: The HERE tile key of the partition/tile where the routing zone is located in the given version of
            the catalog
            * `zoneId`: The identifier of the referenced routing zone within the catalog, example: `here:cm:envzone:3455277`

            Example of a reference to an environmental zone in standard form:
            `hrn:here:data::olp-here:rib-2:1557:environmental-zones:all:here:cm:envzone:3455277`

            In order to reduce response size, routing zone references can also be provided in a compact representation.
            In compact form, parts of a reference are replaced by placeholders, which can be resolved using the
            `refReplacements` dictionary in the parent section.
            The placeholder format is ```\$\d+``` and needs to be surrounded by colons or string start/end. It can be
            captured with the following regular expression: ```(^|:)\$\d+(:|$)``` .

            Example of the aforementioned environmental zone reference in compact form: `$0:$1:3455277`
            With the corresponding `refReplacements`:
            ```
            "refReplacements": {
              "0": "hrn:here:data::olp-here:rib-2:1557",
              "1": "environmental-zones:all:here:cm:envzone"
            }
            ```
        type_ (str | Unset): Extensible enum: `environmental` `vignette` `...`
            The type of the routing zone. A routing zone is defined based on an underlying feature/resource.
            The standard representation of a routing zone reference is
            `{catalogHrn}:{catalogVersion}:({layerId})?:{tileId}:{zoneId}` (refer to `RoutingZoneReference` description in
            this document for details).
            `{zoneId}` represents the identifier of the underlying feature/resource within the catalog, in the
            `"domain:system:type:id"` format.
            This attribute corresponds to the `"domain:system:type"` portion of the identifier.
            E.g. `type=environmental` corresponds to the `"here:cm:envzone"` portion of the identifiers of all environmental
            zones within a catalog.

            To further distinguish between the sub-categories of the `type` (if applicable) use the `category` attribute.

            NOTE: To maintain legacy support `type=vignette` is not renamed but corresponds to the `"here:cm:tollsystem"`
            portion of the identifier for all toll cost features.
        name (str | Unset): The routing zone's name.
        category (str | Unset): Extensible enum: `environmental` `vignette` `congestionPricing` `...`
            The category of the routing zone. Corresponds to the sub-category (if applicable) of the feature/resource
            defining a routing zone, e.g. `vignette` and `congestionPricing` sub-categories of the toll cost features.
    """

    ref: str | Unset = UNSET
    type_: str | Unset = UNSET
    name: str | Unset = UNSET
    category: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ref = self.ref

        type_ = self.type_

        name = self.name

        category = self.category

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if ref is not UNSET:
            field_dict["ref"] = ref
        if type_ is not UNSET:
            field_dict["type"] = type_
        if name is not UNSET:
            field_dict["name"] = name
        if category is not UNSET:
            field_dict["category"] = category

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ref = d.pop("ref", UNSET)

        type_ = d.pop("type", UNSET)

        name = d.pop("name", UNSET)

        category = d.pop("category", UNSET)

        routing_zone = cls(
            ref=ref,
            type_=type_,
            name=name,
            category=category,
        )

        routing_zone.additional_properties = d
        return routing_zone

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
