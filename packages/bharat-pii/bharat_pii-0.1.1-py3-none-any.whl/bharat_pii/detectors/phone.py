import regex as re
from src.bharat_pii.detectors.base import BaseDetector
from src.bharat_pii.entities import EntityType

class PhoneDetector(BaseDetector):
    PHONE_REGEX = re.compile(r"\b(\+91[\-\s]?)?[6-9]\d{9}\b")

    def detect(self, text: str):
        results = []
        for m in self.PHONE_REGEX.finditer(text):
            results.append({
                "entity": EntityType.PHONE,
                "value": m.group(),
                "start": m.start(),
                "end": m.end(),
                "confidence": 0.90
            })
        return results
