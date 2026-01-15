from enum import Enum


class Spans(str, Enum):
    BASEDURATION = "baseDuration"
    CARATTRIBUTES = "carAttributes"
    CONSUMPTION = "consumption"
    COUNTRYCODE = "countryCode"
    DURATION = "duration"
    DYNAMICSPEEDINFO = "dynamicSpeedInfo"
    FUNCTIONALCLASS = "functionalClass"
    GATES = "gates"
    INCIDENTS = "incidents"
    LENGTH = "length"
    MAXSPEED = "maxSpeed"
    NAMES = "names"
    NOTHROUGHRESTRICTIONS = "noThroughRestrictions"
    NOTICES = "notices"
    RAILWAYCROSSINGS = "railwayCrossings"
    ROUTENUMBERS = "routeNumbers"
    ROUTINGZONES = "routingZones"
    SCOOTERATTRIBUTES = "scooterAttributes"
    SEGMENTID = "segmentId"
    SEGMENTREF = "segmentRef"
    SPEEDLIMIT = "speedLimit"
    STATECODE = "stateCode"
    STREETATTRIBUTES = "streetAttributes"
    TOLLSYSTEMS = "tollSystems"
    TRUCKATTRIBUTES = "truckAttributes"
    TRUCKROADTYPES = "truckRoadTypes"
    TYPICALDURATION = "typicalDuration"
    WALKATTRIBUTES = "walkAttributes"

    def __str__(self) -> str:
        return str(self.value)
