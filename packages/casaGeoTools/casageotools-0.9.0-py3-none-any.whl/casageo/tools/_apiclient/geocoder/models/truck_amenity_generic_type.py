from enum import Enum


class TruckAmenityGenericType(str, Enum):
    CARWASH = "carWash"
    CHEMICALTOILETDISPOSAL = "chemicalToiletDisposal"
    CONVENIENCESTORE = "convenienceStore"
    HIGHCANOPY = "highCanopy"
    IDLEREDUCTION = "idleReduction"
    NIGHTPARKINGONLY = "nightParkingOnly"
    PAIDPARKING = "paidParking"
    PARKING = "parking"
    POWERSUPPLY = "powerSupply"
    RESERVABLEPARKING = "reservableParking"
    SECUREPARKING = "secureParking"
    TRUCKSCALES = "truckScales"
    TRUCKSERVICE = "truckService"
    TRUCKSTOP = "truckStop"
    TRUCKWASH = "truckWash"
    WIFI = "wifi"

    def __str__(self) -> str:
        return str(self.value)
