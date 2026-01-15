"""Contains all the data models used in inputs/outputs"""

from .allow import Allow
from .auth_error_response_schema import AuthErrorResponseSchema
from .avoid import Avoid
from .avoid_post import AvoidPost
from .base_ev_empirical_model import BaseEVEmpiricalModel
from .base_ev_physical_model import BaseEVPhysicalModel
from .base_notice_detail import BaseNoticeDetail
from .base_place import BasePlace
from .base_place_side_of_street import BasePlaceSideOfStreet
from .bounding_box_area import BoundingBoxArea
from .bounding_box_area_with_exceptions import BoundingBoxAreaWithExceptions
from .calculate_isolines_optimize_for import CalculateIsolinesOptimizeFor
from .calculate_isolines_post_optimize_for import CalculateIsolinesPostOptimizeFor
from .calculate_isolines_post_parameters import CalculateIsolinesPostParameters
from .connection import Connection
from .coordinate import Coordinate
from .corridor_area import CorridorArea
from .corridor_area_with_exceptions import CorridorAreaWithExceptions
from .data_version import DataVersion
from .departure import Departure
from .encoded_corridor_area import EncodedCorridorArea
from .encoded_corridor_area_with_exceptions import EncodedCorridorAreaWithExceptions
from .encoded_polygon_area import EncodedPolygonArea
from .encoded_polygon_area_with_exceptions import EncodedPolygonAreaWithExceptions
from .error_response import ErrorResponse
from .exclude import Exclude
from .exclude_post import ExcludePost
from .fuel import Fuel
from .health_response_fail_schema import HealthResponseFailSchema
from .health_response_fail_schema_status import HealthResponseFailSchemaStatus
from .health_response_ok_schema import HealthResponseOKSchema
from .health_response_ok_schema_status import HealthResponseOKSchemaStatus
from .isoline import Isoline
from .isoline_error_response import IsolineErrorResponse
from .isoline_response import IsolineResponse
from .isoline_response_notice import IsolineResponseNotice
from .location import Location
from .max_speed_on_segment_post_inner import MaxSpeedOnSegmentPostInner
from .not_allowed import NotAllowed
from .notice_severity import NoticeSeverity
from .polygon import Polygon
from .polygon_area import PolygonArea
from .polygon_area_with_exceptions import PolygonAreaWithExceptions
from .range_ import Range
from .response_range import ResponseRange
from .router_mode import RouterMode
from .routing_mode import RoutingMode
from .server_internal import ServerInternal
from .shape import Shape
from .taxi import Taxi
from .traffic import Traffic
from .traffic_mode import TrafficMode
from .truck import Truck
from .truck_category import TruckCategory
from .truck_engine_type import TruckEngineType
from .truck_type_with_default import TruckTypeWithDefault
from .tunnel_category import TunnelCategory
from .vehicle import Vehicle
from .vehicle_category import VehicleCategory
from .vehicle_engine_type import VehicleEngineType
from .vehicle_type import VehicleType
from .version_response import VersionResponse

__all__ = (
    "Allow",
    "AuthErrorResponseSchema",
    "Avoid",
    "AvoidPost",
    "BaseEVEmpiricalModel",
    "BaseEVPhysicalModel",
    "BaseNoticeDetail",
    "BasePlace",
    "BasePlaceSideOfStreet",
    "BoundingBoxArea",
    "BoundingBoxAreaWithExceptions",
    "CalculateIsolinesOptimizeFor",
    "CalculateIsolinesPostOptimizeFor",
    "CalculateIsolinesPostParameters",
    "Connection",
    "Coordinate",
    "CorridorArea",
    "CorridorAreaWithExceptions",
    "DataVersion",
    "Departure",
    "EncodedCorridorArea",
    "EncodedCorridorAreaWithExceptions",
    "EncodedPolygonArea",
    "EncodedPolygonAreaWithExceptions",
    "ErrorResponse",
    "Exclude",
    "ExcludePost",
    "Fuel",
    "HealthResponseFailSchema",
    "HealthResponseFailSchemaStatus",
    "HealthResponseOKSchema",
    "HealthResponseOKSchemaStatus",
    "Isoline",
    "IsolineErrorResponse",
    "IsolineResponse",
    "IsolineResponseNotice",
    "Location",
    "MaxSpeedOnSegmentPostInner",
    "NotAllowed",
    "NoticeSeverity",
    "Polygon",
    "PolygonArea",
    "PolygonAreaWithExceptions",
    "Range",
    "ResponseRange",
    "RouterMode",
    "RoutingMode",
    "ServerInternal",
    "Shape",
    "Taxi",
    "Traffic",
    "TrafficMode",
    "Truck",
    "TruckCategory",
    "TruckEngineType",
    "TruckTypeWithDefault",
    "TunnelCategory",
    "Vehicle",
    "VehicleCategory",
    "VehicleEngineType",
    "VehicleType",
    "VersionResponse",
)
