import regex as re

def test_regex_matches():
    pattern = re.compile(r"\b(?:\d[ -]*?){13,19}\b")
    text = "3509146551669239"

    matches = list(pattern.finditer(text))
    print("MATCHES:", matches)

    assert len(matches) == 1
