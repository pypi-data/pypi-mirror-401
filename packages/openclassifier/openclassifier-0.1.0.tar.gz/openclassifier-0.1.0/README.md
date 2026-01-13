# OpenClassifier Python SDK

Python SDK for the OpenClassifier API - ultra fast classification for text, images, and PDFs.

## Installation

```bash
pip install openclassifier
```

## Quick Start

```python
from openclassifier import OpenClassifier

client = OpenClassifier(api_key="sk_live_...")

result = client.classify.text(
    "Hello, how can I help you today?",
    ["greeting", "question", "complaint"]
)
print(result["results"]["label"])  # "greeting"
print(result["results"]["confidence"])  # 0.95
```

## Usage

### Text Classification

```python
# Single label (default)
result = client.classify.text(
    content="I need help with my order",
    labels=["support", "sales", "billing"]
)

# Multi-label classification
result = client.classify.text(
    content="Great product but shipping was slow",
    labels=["positive", "negative", "shipping", "product"],
    multi_label=True
)
```

### Image Classification

```python
# From URL
result = client.classify.image(
    inputs=["https://example.com/photo.jpg"],
    labels=["cat", "dog", "bird"]
)

# From base64
result = client.classify.image(
    inputs=[{"base64": "...", "media_type": "image/jpeg"}],
    labels=["cat", "dog", "bird"],
    detail="high"  # "low", "high", or "auto"
)

# Multiple images
result = client.classify.image(
    inputs=[
        "https://example.com/photo1.jpg",
        "https://example.com/photo2.jpg"
    ],
    labels=["landscape", "portrait", "abstract"]
)
```

### PDF Classification

```python
# From URL
result = client.classify.pdf(
    input="https://example.com/document.pdf",
    labels=["invoice", "receipt", "contract"]
)

# With options
result = client.classify.pdf(
    input="https://example.com/document.pdf",
    labels=["invoice", "receipt", "contract"],
    aggregation="both",  # "per_page", "document", or "both"
    page_range={"start": 1, "end": 10}
)

print(result["document_label"]["label"])  # Overall classification
print(result["results"])  # Per-page results
```

## Configuration

```python
client = OpenClassifier(
    api_key="sk_live_...",  # Or set OPENCLASSIFIER_API_KEY env var
    base_url="https://api.openclassifier.com",  # Optional
    timeout=60.0  # Request timeout in seconds
)
```

## Error Handling

```python
from openclassifier import (
    OpenClassifier,
    AuthenticationError,
    InvalidRequestError,
    RateLimitError,
    InsufficientBalanceError,
    ClassificationError,
)

try:
    result = client.classify.text("Hello", ["a", "b"])
except AuthenticationError:
    print("Invalid API key")
except InvalidRequestError as e:
    print(f"Bad request: {e.message}")
except RateLimitError:
    print("Rate limit exceeded, retry later")
except InsufficientBalanceError:
    print("Add credits to your account")
except ClassificationError:
    print("Classification failed")
```

## License

Apache 2.0
