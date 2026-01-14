from bharat_pii.api import detect
from bharat_pii.entities import EntityType

def test_ifsc_detection():
    text = "My IFSC is HDFC0001234"
    results = detect(text)
    assert any(r["entity"] == EntityType.IFSC for r in results)

def test_ifsc_lowercase():
    text = "bank code sbin0000456"
    results = detect(text)
    assert any(r["entity"] == EntityType.IFSC for r in results)

def test_invalid_ifsc():
    text = "invalid IFSC HDFC1234567"
    results = detect(text)
    assert not any(r["entity"] == EntityType.IFSC for r in results)
