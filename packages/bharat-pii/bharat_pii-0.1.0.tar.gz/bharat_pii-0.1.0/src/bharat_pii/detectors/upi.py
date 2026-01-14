import regex as re
from bharat_pii.detectors.base import BaseDetector
from bharat_pii.entities import EntityType

class UPIDetector(BaseDetector):
    # Common UPI PSP suffixes (extendable)
    PSP_SUFFIXES = (
        "upi|okhdfcbank|okicici|oksbi|okaxis|okybl|"
        "paytm|phonepe|ybl|ibl|axl|apl"
    )

    UPI_REGEX = re.compile(
        rf"\b[a-zA-Z0-9._-]{{2,}}@({PSP_SUFFIXES})\b",
        re.IGNORECASE
    )

    def detect(self, text: str):
        results = []

        for m in self.UPI_REGEX.finditer(text):
            results.append({
                "entity": EntityType.UPI_ID,
                "value": m.group(),
                "start": m.start(),
                "end": m.end(),
                "confidence": 0.96
            })

        return results
