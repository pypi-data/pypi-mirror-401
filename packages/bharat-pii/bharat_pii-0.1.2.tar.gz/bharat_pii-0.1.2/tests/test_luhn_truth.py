from bharat_pii.validators import luhn_check

def test_known_valid_cards():
    assert luhn_check("4111111111111111") is True  # Visa
    assert luhn_check("4012888888881881") is True  # Visa
    assert luhn_check("5555555555554444") is True  # Mastercard
    assert luhn_check("378282246310005") is True   # Amex
    assert luhn_check("3566002020360505") is True  # JCB
    assert luhn_check("6522438148680455") is True # RuPay