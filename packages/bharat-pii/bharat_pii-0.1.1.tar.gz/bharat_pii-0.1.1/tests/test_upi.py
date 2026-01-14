from bharat_pii.api import detect
from bharat_pii.entities import EntityType

def test_upi_detection_basic():
    text = "My UPI is rahul@upi"
    results = detect(text)
    print(results)
    assert any(r["entity"] == EntityType.UPI_ID for r in results)

def test_upi_detection_bank():
    text = "Pay to name.singh@okicici"
    results = detect(text)
    assert any(r["entity"] == EntityType.UPI_ID for r in results)

def test_email_not_upi():
    text = "Contact me at test@gmail.com"
    results = detect(text)
    assert not any(r["entity"] == EntityType.UPI_ID for r in results)
