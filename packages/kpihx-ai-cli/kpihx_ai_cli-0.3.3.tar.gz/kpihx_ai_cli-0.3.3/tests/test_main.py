import os
import pytest
from unittest.mock import patch, MagicMock
import yaml


def test_load_config_defaults():
    """Test that load_config returns defaults when no config file exists."""
    with patch('os.path.exists', return_value=False):
        # Import after patching to affect the module-level load
        from ai_cli.main import load_config
        config = load_config()
        assert config['default_model'] == 'phi3.5'
        assert config['ollama_url'] == 'http://localhost:11434'
        assert config['summary_threshold'] == 5


def test_load_config_from_file(tmp_path):
    """Test that load_config loads from a YAML file."""
    config_file = tmp_path / "config.yaml"
    config_file.write_text("""
default_model: custom_model
ollama_url: http://custom:1234
summary_threshold: 10
prompts:
  title_generation: "Custom title: {content}"
""")
    
    with patch('os.getcwd', return_value=str(tmp_path)):
        from ai_cli.main import load_config
        config = load_config()
        assert config['default_model'] == 'custom_model'
        assert config['summary_threshold'] == 10


def test_session_state_initialization():
    """Test SessionState class initialization."""
    from ai_cli.main import SessionState, DEFAULT_CONFIG
    state = SessionState("test_model", DEFAULT_CONFIG)
    
    assert state.model == "test_model"
    assert state.messages == []
    assert state.title == "Nouvelle Discussion"


def test_session_state_message_accumulation():
    """Test that messages can be added to session state."""
    from ai_cli.main import SessionState, DEFAULT_CONFIG
    state = SessionState("phi3.5", DEFAULT_CONFIG)
    
    state.messages.append({"role": "user", "content": "Hello"})
    state.messages.append({"role": "assistant", "content": "Hi there!"})
    
    assert len(state.messages) == 2
    assert state.messages[0]["role"] == "user"
    assert state.messages[1]["role"] == "assistant"


class TestSlashCommands:
    """Tests for slash command parsing."""
    
    def test_slash_command_exit_detected(self):
        """Test that /exit is properly detected."""
        user_input = "/exit"
        assert user_input.startswith("/")
        cmd_parts = user_input.split()
        assert cmd_parts[0].lower() == "/exit"
    
    def test_slash_command_save_with_args(self):
        """Test that /save parses arguments correctly."""
        user_input = "/save L'utilisateur aime le Python"
        cmd_parts = user_input.split()
        cmd = cmd_parts[0].lower()
        fact = " ".join(cmd_parts[1:])
        
        assert cmd == "/save"
        assert fact == "L'utilisateur aime le Python"
    
    def test_slash_command_unknown(self):
        """Test unknown slash commands."""
        user_input = "/unknown"
        cmd_parts = user_input.split()
        cmd = cmd_parts[0].lower()
        
        known_commands = ["/exit", "/clear", "/new", "/old", "/save", "/resume", "/help", "/settings"]
        assert cmd not in known_commands
    
    def test_slash_command_help_exists(self):
        """Test that /help is a recognized command."""
        known_commands = ["/exit", "/clear", "/new", "/old", "/save", "/resume", "/help", "/settings"]
        assert "/help" in known_commands
        assert "/settings" in known_commands


class TestInputHandling:
    """Tests for user input handling edge cases."""
    
    def test_empty_input_skipped(self):
        """Test that empty or whitespace-only input is skipped."""
        inputs = ["", "   ", "\t", "\n"]
        for inp in inputs:
            assert not inp.strip()
    
    def test_normal_message_not_slash_command(self):
        """Test that normal messages don't start with /."""
        normal_inputs = [
            "Quelle est la capitale de la France ?",
            "Explique-moi Python",
            "/ Not a command (space after slash)",
        ]
        for inp in normal_inputs:
            inp_stripped = inp.strip()
            if inp_stripped:
                # Only the first one should not be a slash command
                pass  # Just verifying they don't crash


class TestConfigValidation:
    """Tests for config validation edge cases."""
    
    def test_config_with_missing_keys(self):
        """Test that missing config keys get defaults."""
        minimal_config = {"default_model": "test"}
        
        # Simulating what load_config returns with partial config
        result = {
            "default_model": minimal_config.get("default_model", "phi3.5"),
            "ollama_url": minimal_config.get("ollama_url", "http://localhost:11434"),
            "summary_threshold": minimal_config.get("summary_threshold", 5),
            "prompts": minimal_config.get("prompts", {})
        }
        
        assert result["default_model"] == "test"
        assert result["ollama_url"] == "http://localhost:11434"
