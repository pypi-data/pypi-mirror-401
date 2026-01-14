from bharat_pii.api import detect

def test_aadhaar():
    text = "My Aadhaar is 7704 7741 2433"
    results = detect(text)
    print(results)
    assert any(r["entity"] == "AADHAAR" for r in results)
