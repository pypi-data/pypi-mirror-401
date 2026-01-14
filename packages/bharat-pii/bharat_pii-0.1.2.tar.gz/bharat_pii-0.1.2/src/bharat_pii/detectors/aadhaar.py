import regex as re
from src.bharat_pii.detectors.base import BaseDetector
from src.bharat_pii.entities import EntityType

class AadhaarDetector(BaseDetector):
    AADHAAR_REGEX = re.compile(
        r"\b[2-9]\d{3}\s?\d{4}\s?\d{4}\b"
    )

    def detect(self, text: str):
        results = []
        for m in self.AADHAAR_REGEX.finditer(text):
            results.append({
                "entity": EntityType.AADHAAR,
                "value": m.group(),
                "start": m.start(),
                "end": m.end(),
                "confidence": 0.95
            })
        return results

