import pytest

from openclassifier import OpenClassifier


class TestOpenClassifier:
    def test_init_with_api_key(self, api_key: str):
        client = OpenClassifier(api_key=api_key)
        assert client._http._api_key == api_key
        client.close()

    def test_init_with_env_var(self, api_key: str, monkeypatch):
        monkeypatch.setenv("OPENCLASSIFIER_API_KEY", api_key)
        client = OpenClassifier()
        assert client._http._api_key == api_key
        client.close()

    def test_init_without_api_key_raises(self, monkeypatch):
        monkeypatch.delenv("OPENCLASSIFIER_API_KEY", raising=False)
        with pytest.raises(ValueError, match="API key required"):
            OpenClassifier()

    def test_context_manager(self, api_key: str):
        with OpenClassifier(api_key=api_key) as client:
            assert client._http._api_key == api_key

    def test_has_classify_methods(self, client: OpenClassifier):
        assert hasattr(client, "classify")
        assert hasattr(client.classify, "text")
        assert hasattr(client.classify, "image")
        assert hasattr(client.classify, "pdf")
