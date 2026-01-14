from bharat_pii.validators import luhn_check

def test_luhn_visa():
    assert luhn_check("4012001037141112") is True

def test_luhn_jcb():
    assert luhn_check("3550998167531014") is True

def test_luhn_mastercard():
    assert luhn_check("374355640665754") is True

def test_luhn_rupay():
    assert luhn_check("6522438148680455") is True

def test_luhn_invalid():
    assert luhn_check("4111111111111112") is False

