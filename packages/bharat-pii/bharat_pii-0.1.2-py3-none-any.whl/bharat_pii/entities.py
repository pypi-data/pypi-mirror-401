from enum import Enum

class EntityType(str, Enum):
    PAN = "PAN"
    AADHAAR = "AADHAAR"
    PHONE = "PHONE"
    CREDIT_CARD = "CREDIT_CARD"
    UPI_ID = "UPI_ID"
    IFSC = "IFSC"

