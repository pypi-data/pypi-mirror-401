# bharat-pii 🇮🇳
![PyPI](https://img.shields.io/pypi/v/bharat-pii)
![Python](https://img.shields.io/pypi/pyversions/bharat-pii)
![License](https://img.shields.io/pypi/l/bharat-pii)
![CI](https://github.com/rahulsharma4298/bharat-pii/actions/workflows/ci.yml/badge.svg)

India-first PII detection & redaction library for GenAI pipelines.

**bharat-pii** helps detect and redact **Indian-specific sensitive data**
(PAN, Aadhaar, UPI, IFSC, credit cards, etc.) before sending data to LLMs,
logs, or analytics systems.

It is built with a **regex-first, deterministic core** and designed to be
**extensible with ML / Presidio adapters** in the future.

---

## ✨ Features

- 🇮🇳 India-first PII entities
- ⚡ Fast & deterministic (regex + validation)
- 🔒 Credit card detection with strict Luhn validation
- 🔌 Extensible detector architecture
- 🧱 LLM-safe (local by default)
- 🧪 Fully testable
- 📦 uv / PyPI friendly packaging

---

## 📌 Supported Entities

| Entity | Example |
|------|--------|
| PAN | ABCDE1234F |
| Aadhaar | 2345 6789 0123 |
| Indian Phone | +91 9876543210 |
| Credit Card | 4111 1111 1111 1111 |
| UPI ID | rahul@upi |
| IFSC | HDFC0001234 |

---

## 🛣️ Roadmap

Planned additions:
- Email
- Passport
- Driving License
- Entity severity & priority
- Strict vs loose detection modes
- Presidio (ML) adapter
- CLI tool
- PDF / OCR support

---

## 📦 Installation

Using pip:

    pip install bharat-pii

Using uv:

    uv pip install bharat-pii

---

## 🚀 Usage

### Detect PII

    from bharat_pii.api import detect

    text = "Pay 500 to rahul@upi using card 4111 1111 1111 1111"
    results = detect(text)
    print(results)

---

### Redact PII

    from bharat_pii.api import redact

    safe_text = redact("My IFSC is HDFC0001234 and Aadhaar is 2345 6789 0123")
    print(safe_text)

Output:

    My IFSC is ******1234 and Aadhaar is ********0123

---

## 🧠 Design Philosophy

- Regex-first for precision and predictability
- Validation where applicable (e.g. Luhn for cards)
- Pluggable detector architecture
- No cloud dependency
- Minimal and stable API

Ideal for:
- LLM pipelines
- Fintech & healthcare systems
- Logs & analytics
- Internal tools
- Compliance & PII redaction

---

## 🤝 Contributing

Contributions are welcome.  
Please see `CONTRIBUTING.md` for guidelines.

---

## 📄 License

MIT License © Rahul Sharma
