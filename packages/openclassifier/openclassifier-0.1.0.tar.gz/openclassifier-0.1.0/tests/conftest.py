import os

import pytest
from dotenv import load_dotenv

from openclassifier import OpenClassifier

load_dotenv()


@pytest.fixture
def api_key() -> str:
    key = os.environ.get("OPENCLASSIFIER_API_KEY")
    if not key:
        pytest.skip("OPENCLASSIFIER_API_KEY not set")
    return key


@pytest.fixture
def client(api_key: str) -> OpenClassifier:
    return OpenClassifier(api_key=api_key)
