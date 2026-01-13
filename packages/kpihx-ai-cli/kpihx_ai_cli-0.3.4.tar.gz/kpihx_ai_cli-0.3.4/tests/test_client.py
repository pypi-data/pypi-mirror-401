import pytest
import json
from unittest.mock import patch, Mock, MagicMock
import requests

from ai_cli.ollama_client import OllamaClient, OllamaConnectionError


@pytest.fixture
def mock_prompts():
    return {
        "title_generation": "Titre pour: {content}",
        "summarization": "Résumé de: {content}"
    }


@pytest.fixture
def client(mock_prompts):
    return OllamaClient("http://localhost:11434", mock_prompts)


class TestGenerateTitle:
    def test_generate_title_with_messages(self, mocker, client):
        """Test title generation with valid messages."""
        mocker.patch.object(client, 'chat_sync', return_value="Mon Super Titre")
        
        messages = [{"role": "user", "content": "Quelle est la capitale de la France ?"}]
        title = client.generate_title("phi3.5", messages)
        
        assert title == "Mon Super Titre"
        client.chat_sync.assert_called_once()

    def test_generate_title_empty_messages(self, client):
        """Test that empty messages return default title."""
        title = client.generate_title("phi3.5", [])
        assert title == "Nouvelle Discussion"

    def test_generate_title_connection_error(self, mocker, client):
        """Test that connection error returns default title."""
        mocker.patch.object(client, 'chat_sync', side_effect=OllamaConnectionError("Connection refused"))
        
        messages = [{"role": "user", "content": "Test"}]
        title = client.generate_title("phi3.5", messages)
        
        assert title == "Nouvelle Discussion"


class TestSummarize:
    def test_summarize_success(self, mocker, client):
        """Test successful summarization."""
        mocker.patch.object(client, 'chat_sync', return_value="Un résumé court")
        
        messages = [{"role": "user", "content": "msg1"}, {"role": "assistant", "content": "msg2"}]
        summary = client.summarize("phi3.5", messages)
        
        assert summary == "Un résumé court"

    def test_summarize_connection_error(self, mocker, client):
        """Test that connection error returns error message."""
        mocker.patch.object(client, 'chat_sync', side_effect=OllamaConnectionError("Timeout"))
        
        messages = [{"role": "user", "content": "msg1"}]
        summary = client.summarize("phi3.5", messages)
        
        assert "[Erreur de résumé:" in summary


class TestIsRunning:
    def test_is_running_true(self, mocker, client):
        """Test is_running returns True when server responds."""
        mock_response = Mock()
        mock_response.status_code = 200
        mocker.patch('requests.get', return_value=mock_response)
        
        assert client.is_running() is True

    def test_is_running_false_connection_error(self, mocker, client):
        """Test is_running returns False on connection error."""
        mocker.patch('requests.get', side_effect=requests.exceptions.ConnectionError())
        
        assert client.is_running() is False

    def test_is_running_false_timeout(self, mocker, client):
        """Test is_running returns False on timeout."""
        mocker.patch('requests.get', side_effect=requests.exceptions.Timeout())
        
        assert client.is_running() is False


class TestChatStream:
    def test_chat_stream_yields_content(self, mocker, client):
        """Test that chat_stream yields content chunks."""
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.iter_lines = Mock(return_value=[
            json.dumps({"message": {"content": "Hello "}}).encode(),
            json.dumps({"message": {"content": "World!"}}).encode(),
        ])
        mocker.patch('requests.post', return_value=mock_response)
        
        chunks = list(client.chat_stream("phi3.5", [{"role": "user", "content": "Hi"}]))
        
        assert chunks == ["Hello ", "World!"]

    def test_chat_stream_handles_invalid_json(self, mocker, client):
        """Test that invalid JSON lines are skipped."""
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.iter_lines = Mock(return_value=[
            b"invalid json",
            json.dumps({"message": {"content": "Valid"}}).encode(),
        ])
        mocker.patch('requests.post', return_value=mock_response)
        
        chunks = list(client.chat_stream("phi3.5", [{"role": "user", "content": "Hi"}]))
        
        assert chunks == ["Valid"]

    def test_chat_stream_connection_error(self, mocker, client):
        """Test that connection error yields error message."""
        mocker.patch('requests.post', side_effect=requests.exceptions.ConnectionError("Connection refused"))
        
        chunks = list(client.chat_stream("phi3.5", [{"role": "user", "content": "Hi"}]))
        
        assert len(chunks) == 1
        assert "[Erreur]" in chunks[0]


class TestChatSync:
    def test_chat_sync_returns_content(self, mocker, client):
        """Test that chat_sync returns response content."""
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {"message": {"content": "Response text"}}
        mocker.patch('requests.post', return_value=mock_response)
        
        result = client.chat_sync("phi3.5", [{"role": "user", "content": "Hi"}])
        
        assert result == "Response text"

    def test_chat_sync_raises_on_connection_error(self, mocker, client):
        """Test that connection error raises OllamaConnectionError."""
        mocker.patch('requests.post', side_effect=requests.exceptions.ConnectionError())
        
        with pytest.raises(OllamaConnectionError):
            client.chat_sync("phi3.5", [{"role": "user", "content": "Hi"}])

    def test_chat_sync_raises_on_invalid_response(self, mocker, client):
        """Test that invalid response structure raises OllamaConnectionError."""
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {"unexpected": "structure"}
        mocker.patch('requests.post', return_value=mock_response)
        
        with pytest.raises(OllamaConnectionError) as exc_info:
            client.chat_sync("phi3.5", [{"role": "user", "content": "Hi"}])
        
        assert "invalide" in str(exc_info.value)


class TestBackwardCompatibility:
    def test_chat_with_stream_true(self, mocker, client):
        """Test that chat() with stream=True calls chat_stream."""
        mocker.patch.object(client, 'chat_stream', return_value=iter(["test"]))
        
        result = client.chat("phi3.5", [], stream=True)
        
        client.chat_stream.assert_called_once()
        assert list(result) == ["test"]

    def test_chat_with_stream_false(self, mocker, client):
        """Test that chat() with stream=False calls chat_sync."""
        mocker.patch.object(client, 'chat_sync', return_value="sync result")
        
        result = client.chat("phi3.5", [], stream=False)
        
        client.chat_sync.assert_called_once()
        assert result == "sync result"

