"""Tests for tilde configuration module."""

import os
from unittest.mock import MagicMock, patch

import pytest

from tilde.config import TildeConfig, _map_to_openai_model, get_config


class TestTildeConfig:
    """Tests for TildeConfig dataclass."""

    def test_default_values(self):
        """Test default configuration values."""
        # Clear any cached config
        get_config.cache_clear()
        
        with patch.dict(os.environ, {}, clear=True):
            config = TildeConfig()
            
            assert config.llm_model == "gemini-3-flash-preview"
            assert config.llm_temperature == 0.7
            assert config.embedding_model == "gemini-embedding-001"
            assert config.embedding_dimensions == 768
            assert config.google_api_key is None
            assert config.openai_api_key is None

    def test_loads_google_api_key_from_env(self):
        """Test that GOOGLE_API_KEY is loaded from environment."""
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "test-google-key"}, clear=True):
            config = TildeConfig()
            assert config.google_api_key == "test-google-key"

    def test_loads_gemini_api_key_as_fallback(self):
        """Test that GEMINI_API_KEY works as fallback for GOOGLE_API_KEY."""
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-gemini-key"}, clear=True):
            config = TildeConfig()
            assert config.google_api_key == "test-gemini-key"

    def test_google_key_takes_priority_over_gemini(self):
        """Test GOOGLE_API_KEY takes priority over GEMINI_API_KEY."""
        with patch.dict(os.environ, {
            "GOOGLE_API_KEY": "google-key",
            "GEMINI_API_KEY": "gemini-key"
        }, clear=True):
            config = TildeConfig()
            assert config.google_api_key == "google-key"

    def test_loads_openai_api_key_from_env(self):
        """Test that OPENAI_API_KEY is loaded from environment."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-openai-key"}, clear=True):
            config = TildeConfig()
            assert config.openai_api_key == "test-openai-key"

    def test_provider_returns_google_when_google_key_set(self):
        """Test provider property returns 'google' when Google key is set."""
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "test-key"}, clear=True):
            config = TildeConfig()
            assert config.provider == "google"

    def test_provider_returns_openai_when_only_openai_key_set(self):
        """Test provider property returns 'openai' when only OpenAI key is set."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=True):
            config = TildeConfig()
            assert config.provider == "openai"

    def test_provider_prefers_google_over_openai(self):
        """Test that Google is preferred when both keys are available."""
        with patch.dict(os.environ, {
            "GOOGLE_API_KEY": "google-key",
            "OPENAI_API_KEY": "openai-key"
        }, clear=True):
            config = TildeConfig()
            assert config.provider == "google"

    def test_provider_raises_when_no_key(self):
        """Test that provider raises RuntimeError when no key is available."""
        with patch.dict(os.environ, {}, clear=True):
            config = TildeConfig()
            with pytest.raises(RuntimeError, match="No API key found"):
                _ = config.provider

    def test_api_key_returns_google_key(self):
        """Test api_key property returns Google key when available."""
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "test-google"}, clear=True):
            config = TildeConfig()
            assert config.api_key == "test-google"

    def test_api_key_returns_openai_key_as_fallback(self):
        """Test api_key property returns OpenAI key when Google key is not available."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-openai"}, clear=True):
            config = TildeConfig()
            assert config.api_key == "test-openai"

    def test_api_key_raises_when_no_key(self):
        """Test that api_key raises RuntimeError when no key is available."""
        with patch.dict(os.environ, {}, clear=True):
            config = TildeConfig()
            with pytest.raises(RuntimeError, match="No API key available"):
                _ = config.api_key

    def test_explicit_key_overrides_env(self):
        """Test that explicitly provided keys override environment variables."""
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "env-key"}, clear=True):
            config = TildeConfig(google_api_key="explicit-key")
            assert config.google_api_key == "explicit-key"


class TestGetConfig:
    """Tests for get_config function."""

    def test_returns_config_instance(self):
        """Test that get_config returns a TildeConfig instance."""
        get_config.cache_clear()
        
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "test"}, clear=True):
            config = get_config()
            assert isinstance(config, TildeConfig)

    def test_reads_tilde_llm_model_from_env(self):
        """Test that TILDE_LLM_MODEL overrides default."""
        get_config.cache_clear()
        
        with patch.dict(os.environ, {
            "GOOGLE_API_KEY": "test",
            "TILDE_LLM_MODEL": "gemini-1.5-pro"
        }, clear=True):
            config = get_config()
            assert config.llm_model == "gemini-1.5-pro"

    def test_reads_tilde_embedding_model_from_env(self):
        """Test that TILDE_EMBEDDING_MODEL overrides default."""
        get_config.cache_clear()
        
        with patch.dict(os.environ, {
            "GOOGLE_API_KEY": "test",
            "TILDE_EMBEDDING_MODEL": "text-embedding-005"
        }, clear=True):
            config = get_config()
            assert config.embedding_model == "text-embedding-005"

    def test_config_is_cached(self):
        """Test that get_config returns the same instance on subsequent calls."""
        get_config.cache_clear()
        
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "test"}, clear=True):
            config1 = get_config()
            config2 = get_config()
            assert config1 is config2


class TestConfigFilePersistence:
    """Tests for config file loading and saving."""

    def test_load_config_file_returns_empty_if_no_file(self, tmp_path):
        """Test that load_config_file returns empty dict if file doesn't exist."""
        from tilde.config import load_config_file
        
        result = load_config_file(tmp_path / "nonexistent.yaml")
        assert result == {}

    def test_save_and_load_config_file(self, tmp_path):
        """Test saving and loading config file."""
        from tilde.config import TildeConfig, load_config_file, save_config
        
        config_path = tmp_path / "config.yaml"
        config = TildeConfig(
            llm_model="test-model",
            embedding_model="test-embedding",
        )
        
        # Save config
        save_config(config, config_path)
        
        # Load it back
        loaded = load_config_file(config_path)
        
        assert loaded["llm_model"] == "test-model"
        assert loaded["embedding_model"] == "test-embedding"
        assert "google_api_key" not in loaded  # API keys should not be saved

    def test_save_config_creates_directory(self, tmp_path):
        """Test that save_config creates parent directories."""
        from tilde.config import TildeConfig, save_config
        
        config_path = tmp_path / "nested" / "dir" / "config.yaml"
        config = TildeConfig()
        
        save_config(config, config_path)
        
        assert config_path.exists()

    def test_save_config_excludes_api_keys(self, tmp_path):
        """Test that API keys are never saved to file."""
        from tilde.config import TildeConfig, save_config
        
        config_path = tmp_path / "config.yaml"
        config = TildeConfig(
            google_api_key="secret-google-key",
            openai_api_key="secret-openai-key",
        )
        
        save_config(config, config_path)
        
        # Read raw file content
        content = config_path.read_text()
        assert "secret-google-key" not in content
        assert "secret-openai-key" not in content

    def test_get_config_loads_from_file(self, tmp_path):
        """Test that get_config loads settings from config file."""
        from tilde.config import save_config, TildeConfig, reset_config
        
        # Create a config file
        config_path = tmp_path / "config.yaml"
        config = TildeConfig(llm_model="file-based-model")
        save_config(config, config_path)
        
        # Patch CONFIG_FILE_PATH and reset cache
        with patch("tilde.config.CONFIG_FILE_PATH", config_path):
            with patch.dict(os.environ, {}, clear=True):
                reset_config()
                from tilde.config import get_config
                loaded_config = get_config()
                
                assert loaded_config.llm_model == "file-based-model"
                reset_config()

    def test_env_var_overrides_file_config(self, tmp_path):
        """Test that environment variables override file settings."""
        from tilde.config import save_config, TildeConfig, reset_config
        
        # Create a config file
        config_path = tmp_path / "config.yaml"
        config = TildeConfig(llm_model="file-model")
        save_config(config, config_path)
        
        # Patch and test with env var override
        with patch("tilde.config.CONFIG_FILE_PATH", config_path):
            with patch.dict(os.environ, {"TILDE_LLM_MODEL": "env-model"}, clear=True):
                reset_config()
                from tilde.config import get_config
                loaded_config = get_config()
                
                assert loaded_config.llm_model == "env-model"
                reset_config()

    def test_reset_config_clears_cache(self):
        """Test that reset_config clears the config cache."""
        from tilde.config import reset_config
        
        get_config.cache_clear()
        
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "test"}, clear=True):
            config1 = get_config()
            reset_config()
            config2 = get_config()
            
            # After reset, should be a different instance
            assert config1 is not config2

    def test_to_dict_returns_saveable_config(self):
        """Test that to_dict returns config without API keys."""
        config = TildeConfig(
            llm_model="test",
            google_api_key="secret",
        )
        
        result = config.to_dict()
        
        assert "llm_model" in result
        assert "google_api_key" not in result
        assert "openai_api_key" not in result


class TestMapToOpenaiModel:
    """Tests for _map_to_openai_model function."""

    def test_maps_gemini_flash_to_gpt4o_mini(self):
        """Test gemini-3-flash-preview maps to gpt-4o-mini."""
        assert _map_to_openai_model("gemini-3-flash-preview") == "gpt-4o-mini"

    def test_maps_gemini_15_pro_to_gpt4o(self):
        """Test gemini-1.5-pro maps to gpt-4o."""
        assert _map_to_openai_model("gemini-1.5-pro") == "gpt-4o"

    def test_maps_gemini_15_flash_to_gpt4o_mini(self):
        """Test gemini-1.5-flash maps to gpt-4o-mini."""
        assert _map_to_openai_model("gemini-1.5-flash") == "gpt-4o-mini"

    def test_returns_unknown_model_unchanged(self):
        """Test that unknown model names are returned as-is."""
        assert _map_to_openai_model("gpt-4") == "gpt-4"
        assert _map_to_openai_model("claude-3") == "claude-3"


class TestCallLlm:
    """Tests for call_llm function."""

    def test_call_llm_uses_google_when_available(self):
        """Test that call_llm uses Google Gemini when key is available."""
        get_config.cache_clear()
        
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "test-key"}, clear=True):
            with patch("tilde.config.get_config") as mock_get_config:
                mock_config = MagicMock()
                mock_config.provider = "google"
                mock_config.google_api_key = "test-key"
                mock_config.llm_model = "gemini-3-flash-preview"
                mock_get_config.return_value = mock_config
                
                with patch("google.genai.Client") as mock_client:
                    mock_response = MagicMock()
                    mock_response.text = "Test response"
                    mock_client.return_value.models.generate_content.return_value = mock_response
                    
                    from tilde.config import call_llm
                    result = call_llm("Test prompt")
                    
                    assert result == "Test response"

    def test_call_llm_uses_custom_model(self):
        """Test that call_llm uses provided model override."""
        get_config.cache_clear()
        
        with patch("tilde.config.get_config") as mock_get_config:
            mock_config = MagicMock()
            mock_config.provider = "google"
            mock_config.google_api_key = "test-key"
            mock_config.llm_model = "gemini-3-flash-preview"
            mock_get_config.return_value = mock_config
            
            with patch("google.genai.Client") as mock_client:
                mock_response = MagicMock()
                mock_response.text = "Response"
                mock_client.return_value.models.generate_content.return_value = mock_response
                
                from tilde.config import call_llm
                call_llm("Test", model="gemini-1.5-pro")
                
                mock_client.return_value.models.generate_content.assert_called_once()
                call_args = mock_client.return_value.models.generate_content.call_args
                assert call_args.kwargs["model"] == "gemini-1.5-pro"


class TestGetEmbedding:
    """Tests for get_embedding function."""

    def test_get_embedding_uses_google_when_available(self):
        """Test that get_embedding uses Google when key is available."""
        get_config.cache_clear()
        
        with patch("tilde.config.get_config") as mock_get_config:
            mock_config = MagicMock()
            mock_config.provider = "google"
            mock_config.google_api_key = "test-key"
            mock_config.embedding_model = "gemini-embedding-001"
            mock_get_config.return_value = mock_config
            
            with patch("google.genai.Client") as mock_client:
                mock_embedding = MagicMock()
                mock_embedding.values = [0.1, 0.2, 0.3]
                mock_response = MagicMock()
                mock_response.embeddings = [mock_embedding]
                mock_client.return_value.models.embed_content.return_value = mock_response
                
                from tilde.config import get_embedding
                result = get_embedding("Test text")
                
                assert result == [0.1, 0.2, 0.3]

    def test_get_embedding_uses_custom_model(self):
        """Test that get_embedding uses provided model override."""
        with patch("tilde.config.get_config") as mock_get_config:
            mock_config = MagicMock()
            mock_config.provider = "google"
            mock_config.google_api_key = "test-key"
            mock_config.embedding_model = "gemini-embedding-001"
            mock_get_config.return_value = mock_config
            
            with patch("google.genai.Client") as mock_client:
                mock_embedding = MagicMock()
                mock_embedding.values = [0.1]
                mock_response = MagicMock()
                mock_response.embeddings = [mock_embedding]
                mock_client.return_value.models.embed_content.return_value = mock_response
                
                from tilde.config import get_embedding
                get_embedding("Test", model="custom-model")
                
                mock_client.return_value.models.embed_content.assert_called_once()
                call_args = mock_client.return_value.models.embed_content.call_args
                assert call_args.kwargs["model"] == "custom-model"
