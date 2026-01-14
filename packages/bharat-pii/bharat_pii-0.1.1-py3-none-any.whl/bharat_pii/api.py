from bharat_pii.redaction.masker import mask_value
from bharat_pii.utils import DEFAULT_DETECTORS

def detect(text: str, detectors=None):
    detectors = detectors or DEFAULT_DETECTORS
    results = []

    for detector in detectors:
        results.extend(detector.detect(text))

    # sort + dedupe later
    results = sorted(results, key=lambda x: x["start"])
    return _resolve_overlaps(results)


def redact(text: str, strategy="mask"):
    entities = detect(text)
    redacted = text

    for ent in reversed(entities):
        replacement = (
            mask_value(ent["value"])
            if strategy == "mask"
            else "[REDACTED]"
        )

        redacted = (
            redacted[:ent["start"]] +
            replacement +
            redacted[ent["end"]:]
        )

    return redacted


def _resolve_overlaps(entities):
    resolved = []

    for ent in sorted(entities, key=lambda x: (x["start"], -x["end"])):
        overlap = False
        for r in resolved:
            if not (ent["end"] <= r["start"] or ent["start"] >= r["end"]):
                # overlap detected
                if (
                    ent["confidence"] > r["confidence"]
                    or (ent["end"] - ent["start"]) > (r["end"] - r["start"])
                ):
                    resolved.remove(r)
                else:
                    overlap = True
                break

        if not overlap:
            resolved.append(ent)

    return resolved
