import os
import json
import pytest
from ai_cli.storage import StorageManager, StorageError


@pytest.fixture
def temp_storage(tmp_path):
    storage = StorageManager(str(tmp_path))
    return storage


class TestSaveSession:
    def test_save_and_list_sessions(self, temp_storage):
        """Test basic save and list functionality."""
        messages = [{"role": "user", "content": "hello"}]
        temp_storage.save_session(messages, "Test Title")
        
        sessions = temp_storage.list_sessions()
        assert len(sessions) == 1
        assert sessions[0]['title'] == "Test Title"

    def test_save_session_with_special_characters(self, temp_storage):
        """Test that special characters in title are sanitized."""
        messages = [{"role": "user", "content": "test"}]
        filename = temp_storage.save_session(messages, "Test<>:\"/\\|?* Title!")
        
        # Verify file was created with sanitized name
        assert "<" not in filename
        assert ">" not in filename

    def test_save_session_with_empty_title(self, temp_storage):
        """Test that empty title fallbacks to 'session'."""
        messages = [{"role": "user", "content": "test"}]
        filename = temp_storage.save_session(messages, "!@#$%^&*()")  # All special chars
        
        # Should fallback to 'session' when all chars are filtered
        assert "session" in filename

    def test_save_session_with_unicode(self, temp_storage):
        """Test saving session with unicode content."""
        messages = [{"role": "user", "content": "Bonjour, comment ça va ? 日本語 🎉"}]
        temp_storage.save_session(messages, "Unicode Test")
        
        sessions = temp_storage.list_sessions()
        loaded = temp_storage.load_session(sessions[0]['file'])
        assert "日本語" in loaded['messages'][0]['content']


class TestListSessions:
    def test_list_sessions_empty(self, temp_storage):
        """Test listing sessions when no sessions exist."""
        sessions = temp_storage.list_sessions()
        assert sessions == []

    def test_list_sessions_limit(self, temp_storage):
        """Test that list_sessions respects limit."""
        for i in range(5):
            temp_storage.save_session([{"role": "user", "content": f"msg{i}"}], f"Session {i}")
        
        sessions = temp_storage.list_sessions(limit=3)
        assert len(sessions) == 3

    def test_list_sessions_corrupted_json(self, temp_storage):
        """Test that corrupted JSON files are skipped gracefully."""
        # Create a valid session first
        temp_storage.save_session([{"role": "user", "content": "valid"}], "Valid Session")
        
        # Create a corrupted JSON file
        corrupted_file = temp_storage.sessions_dir / "corrupted.json"
        corrupted_file.write_text("{ invalid json }")
        
        sessions = temp_storage.list_sessions()
        # Should still return the valid session
        assert len(sessions) == 1
        assert sessions[0]['title'] == "Valid Session"


class TestLoadSession:
    def test_load_session_success(self, temp_storage):
        """Test loading a saved session."""
        messages = [{"role": "user", "content": "test message"}]
        filename = temp_storage.save_session(messages, "Load Test")
        
        loaded = temp_storage.load_session(filename)
        assert loaded['messages'] == messages
        assert loaded['title'] == "Load Test"

    def test_load_session_not_found(self, temp_storage):
        """Test that loading non-existent session raises StorageError."""
        with pytest.raises(StorageError) as exc_info:
            temp_storage.load_session("nonexistent.json")
        
        assert "introuvable" in str(exc_info.value)

    def test_load_session_corrupted(self, temp_storage):
        """Test that loading corrupted session raises StorageError."""
        corrupted_file = temp_storage.sessions_dir / "corrupted.json"
        corrupted_file.write_text("{ invalid json content")
        
        with pytest.raises(StorageError) as exc_info:
            temp_storage.load_session("corrupted.json")
        
        assert "corrompue" in str(exc_info.value)


class TestMemory:
    def test_memory_append(self, temp_storage):
        """Test appending to memory file."""
        temp_storage.save_memory("L'utilisateur aime le café")
        memory = temp_storage.get_memory()
        assert "L'utilisateur aime le café" in memory

    def test_memory_multiple_appends(self, temp_storage):
        """Test multiple memory appends."""
        temp_storage.save_memory("Fact 1")
        temp_storage.save_memory("Fact 2")
        memory = temp_storage.get_memory()
        
        assert "Fact 1" in memory
        assert "Fact 2" in memory

    def test_memory_overwrite(self, temp_storage):
        """Test overwriting memory file."""
        temp_storage.save_memory("Initial content")
        temp_storage.save_memory("Completely new content", mode="overwrite")
        memory = temp_storage.get_memory()
        
        assert memory == "Completely new content"
        assert "Initial content" not in memory

    def test_get_memory_file_not_exists(self, tmp_path):
        """Test get_memory when memory file was deleted."""
        storage = StorageManager(str(tmp_path))
        # Delete the memory file that was auto-created
        storage.memory_file.unlink()
        
        # Should return empty string, not crash
        memory = storage.get_memory()
        assert memory == ""


class TestDeleteSession:
    """Tests for session deletion functionality."""
    
    def test_delete_session_success(self, temp_storage):
        """Test successful session deletion."""
        messages = [{"role": "user", "content": "test"}]
        filename = temp_storage.save_session(messages, "To Delete")
        
        # Verify session exists
        sessions = temp_storage.list_sessions()
        assert len(sessions) == 1
        
        # Delete the session
        result = temp_storage.delete_session(filename)
        assert result is True
        
        # Verify session is gone
        sessions = temp_storage.list_sessions()
        assert len(sessions) == 0
    
    def test_delete_session_not_found(self, temp_storage):
        """Test that deleting non-existent session raises StorageError."""
        with pytest.raises(StorageError) as exc_info:
            temp_storage.delete_session("nonexistent.json")
        
        assert "introuvable" in str(exc_info.value)
    
    def test_delete_session_multiple(self, temp_storage):
        """Test deleting one session among many."""
        # Create 3 sessions
        for i in range(3):
            temp_storage.save_session(
                [{"role": "user", "content": f"msg{i}"}], 
                f"Session {i}"
            )
        
        sessions = temp_storage.list_sessions()
        assert len(sessions) == 3
        
        # Delete the middle one
        temp_storage.delete_session(sessions[1]['file'])
        
        # Verify only 2 remain
        remaining = temp_storage.list_sessions()
        assert len(remaining) == 2


class TestInitialization:
    def test_creates_directories(self, tmp_path):
        """Test that initialization creates required directories."""
        base_dir = tmp_path / "new_dir"
        storage = StorageManager(str(base_dir))
        
        assert storage.sessions_dir.exists()
        assert storage.memory_file.exists()

    def test_expands_home_dir(self):
        """Test that ~ in path is expanded."""
        storage = StorageManager("~/.ai-cli-test")
        assert "~" not in str(storage.base_dir)
        # Cleanup
        import shutil
        if storage.base_dir.exists():
            shutil.rmtree(storage.base_dir)

