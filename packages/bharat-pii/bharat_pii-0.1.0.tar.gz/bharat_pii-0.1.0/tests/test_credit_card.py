from bharat_pii.api import detect

def test_credit_card_detection():
    text = "My card number is 4012001037141112"
    results = detect(text)
    print(results)
    assert any(r["entity"] == "CREDIT_CARD" for r in results)
