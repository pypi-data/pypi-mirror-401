from enum import Enum


class V1IsolinesCreateTransportMode(str, Enum):
    BICYCLE = "bicycle"
    BUS = "bus"
    CAR = "car"
    PEDESTRIAN = "pedestrian"
    PRIVATEBUS = "privateBus"
    SCOOTER = "scooter"
    TAXI = "taxi"
    TRUCK = "truck"

    def __str__(self) -> str:
        return str(self.value)
