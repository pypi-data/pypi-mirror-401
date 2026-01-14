import regex as re
from bharat_pii.detectors.base import BaseDetector
from bharat_pii.entities import EntityType
from bharat_pii.validators import luhn_check

class CreditCardDetector(BaseDetector):
    CARD_REGEX = re.compile(
        r"\b(?:\d[ -]*?){13,19}\b"
    )

    def detect(self, text: str):
        results = []

        for m in self.CARD_REGEX.finditer(text):
            raw = m.group()
            digits = "".join(d for d in raw if d.isdigit())

            if 13 <= len(digits) <= 19 and luhn_check(digits):
                results.append({
                    "entity": EntityType.CREDIT_CARD,
                    "value": raw,
                    "start": m.start(),
                    "end": m.end(),
                    "confidence": 0.97
                })

        return results
