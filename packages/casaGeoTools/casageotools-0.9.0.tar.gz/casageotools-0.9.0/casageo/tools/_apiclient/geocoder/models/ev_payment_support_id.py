from enum import Enum


class EvPaymentSupportId(str, Enum):
    AUTHBYCARPLUGANDCHARGE = "authByCarPlugAndCharge"
    CREDITCARD = "creditCard"
    DEBITCARD = "debitCard"
    ONLINEAPPLEPAY = "onlineApplePay"
    ONLINEGOOGLEPAY = "onlineGooglePay"
    ONLINEPAYPAL = "onlinePaypal"
    OPERATORAPP = "operatorApp"

    def __str__(self) -> str:
        return str(self.value)
