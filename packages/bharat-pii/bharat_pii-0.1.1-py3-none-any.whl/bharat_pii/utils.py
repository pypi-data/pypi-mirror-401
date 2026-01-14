from bharat_pii.detectors.credit_card import CreditCardDetector
from bharat_pii.detectors.ifsc import IFSCDetector
from bharat_pii.detectors.pan import PanDetector
from bharat_pii.detectors.aadhaar import AadhaarDetector
from bharat_pii.detectors.phone import PhoneDetector
from bharat_pii.detectors.upi import UPIDetector

DEFAULT_DETECTORS = [
    PanDetector(),
    AadhaarDetector(),
    PhoneDetector(),
    CreditCardDetector(),
    UPIDetector(),
    IFSCDetector()
]


