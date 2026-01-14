import regex as re
from src.bharat_pii.detectors.base import BaseDetector
from src.bharat_pii.entities import EntityType

class PanDetector(BaseDetector):
    PAN_REGEX = re.compile(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b")

    def detect(self, text: str):
        results = []
        for m in self.PAN_REGEX.finditer(text):
            results.append({
                "entity": EntityType.PAN,
                "value": m.group(),
                "start": m.start(),
                "end": m.end(),
                "confidence": 0.99
            })
        return results
