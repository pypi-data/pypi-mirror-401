import regex as re
from bharat_pii.detectors.base import BaseDetector
from bharat_pii.entities import EntityType

class IFSCDetector(BaseDetector):
    IFSC_REGEX = re.compile(
        r"\b[A-Z]{4}0[A-Z0-9]{6}\b",
        re.IGNORECASE
    )

    def detect(self, text: str):
        results = []

        for m in self.IFSC_REGEX.finditer(text):
            results.append({
                "entity": EntityType.IFSC,
                "value": m.group(),
                "start": m.start(),
                "end": m.end(),
                "confidence": 0.98
            })

        return results
