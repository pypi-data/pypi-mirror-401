from enum import Enum


class Return(str, Enum):
    ACTIONS = "actions"
    ELEVATION = "elevation"
    INCIDENTS = "incidents"
    INSTRUCTIONS = "instructions"
    MLDURATION = "mlDuration"
    NOTHROUGHRESTRICTIONS = "noThroughRestrictions"
    PASSTHROUGH = "passthrough"
    POLYLINE = "polyline"
    POTENTIALTIMEDEPENDENTVIOLATIONS = "potentialTimeDependentViolations"
    ROUTEHANDLE = "routeHandle"
    ROUTELABELS = "routeLabels"
    ROUTINGZONES = "routingZones"
    SUMMARY = "summary"
    TOLLS = "tolls"
    TRAVELSUMMARY = "travelSummary"
    TRUCKROADTYPES = "truckRoadTypes"
    TURNBYTURNACTIONS = "turnByTurnActions"
    TYPICALDURATION = "typicalDuration"

    def __str__(self) -> str:
        return str(self.value)
