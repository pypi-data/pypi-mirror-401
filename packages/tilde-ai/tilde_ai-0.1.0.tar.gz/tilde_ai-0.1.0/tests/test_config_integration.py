"""Integration tests for tilde configuration module.

These tests make actual API calls and require a valid GOOGLE_API_KEY.
Run with: pytest tests/test_config_integration.py -v

To skip in CI without API keys, these tests are marked with @pytest.mark.integration.
"""

import os

import pytest

# Skip all tests in this module if no API key is available
pytestmark = pytest.mark.skipif(
    not os.environ.get("GOOGLE_API_KEY") and not os.environ.get("OPENAI_API_KEY"),
    reason="No API key available for integration tests"
)


class TestCallLlmIntegration:
    """Integration tests for call_llm function."""

    def test_call_llm_returns_response(self):
        """Test that call_llm returns a non-empty response."""
        from tilde.config import call_llm, get_config
        
        get_config.cache_clear()
        
        response = call_llm("Say 'hello' and nothing else.")
        
        assert response is not None
        assert len(response) > 0
        assert "hello" in response.lower()

    def test_call_llm_with_custom_model(self):
        """Test that call_llm works with a custom model."""
        from tilde.config import call_llm, get_config
        
        get_config.cache_clear()
        config = get_config()
        
        # Use a different model if available
        if config.provider == "google":
            model = "gemini-1.5-flash"
        else:
            model = "gpt-4o-mini"
        
        response = call_llm("Say 'test' and nothing else.", model=model)
        
        assert response is not None
        assert len(response) > 0

    def test_call_llm_handles_long_prompt(self):
        """Test that call_llm can handle longer prompts."""
        from tilde.config import call_llm, get_config
        
        get_config.cache_clear()
        
        long_prompt = "Summarize the following text: " + "word " * 100
        response = call_llm(long_prompt)
        
        assert response is not None
        assert len(response) > 0


class TestGetEmbeddingIntegration:
    """Integration tests for get_embedding function."""

    def test_get_embedding_returns_vector(self):
        """Test that get_embedding returns a valid embedding vector."""
        from tilde.config import get_config, get_embedding
        
        get_config.cache_clear()
        
        embedding = get_embedding("Hello, world!")
        
        assert embedding is not None
        assert isinstance(embedding, list)
        assert len(embedding) > 0
        assert all(isinstance(x, float) for x in embedding)

    def test_get_embedding_returns_consistent_dimensions(self):
        """Test that embeddings have consistent dimensions."""
        from tilde.config import get_config, get_embedding
        
        get_config.cache_clear()
        
        embedding1 = get_embedding("First text")
        embedding2 = get_embedding("Second text")
        
        assert len(embedding1) == len(embedding2)
        # Gemini embedding-001 returns 768 dimensions
        assert len(embedding1) >= 256  # Reasonable minimum

    def test_get_embedding_different_texts_different_embeddings(self):
        """Test that different texts produce different embeddings."""
        from tilde.config import get_config, get_embedding
        
        get_config.cache_clear()
        
        embedding1 = get_embedding("Python programming language")
        embedding2 = get_embedding("Cooking recipes for dinner")
        
        # Calculate simple cosine similarity
        dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
        norm1 = sum(a * a for a in embedding1) ** 0.5
        norm2 = sum(b * b for b in embedding2) ** 0.5
        similarity = dot_product / (norm1 * norm2) if norm1 > 0 and norm2 > 0 else 0
        
        # Different texts should have lower similarity (not identical)
        assert similarity < 0.99

    def test_get_embedding_similar_texts_higher_similarity(self):
        """Test that similar texts have higher embedding similarity."""
        from tilde.config import get_config, get_embedding
        
        get_config.cache_clear()
        
        embedding1 = get_embedding("Python is a programming language")
        embedding2 = get_embedding("Python programming language for software")
        embedding3 = get_embedding("Baking chocolate cake recipe")
        
        # Calculate similarities
        def cosine_sim(e1, e2):
            dot = sum(a * b for a, b in zip(e1, e2))
            n1 = sum(a * a for a in e1) ** 0.5
            n2 = sum(b * b for b in e2) ** 0.5
            return dot / (n1 * n2) if n1 > 0 and n2 > 0 else 0
        
        sim_similar = cosine_sim(embedding1, embedding2)
        sim_different = cosine_sim(embedding1, embedding3)
        
        # Similar texts should have higher similarity
        assert sim_similar > sim_different


class TestConfigIntegration:
    """Integration tests for get_config function."""

    def test_config_provider_is_valid(self):
        """Test that config returns a valid provider."""
        from tilde.config import get_config
        
        get_config.cache_clear()
        config = get_config()
        
        assert config.provider in ["google", "openai"]

    def test_config_has_api_key(self):
        """Test that config has an API key when provider is set."""
        from tilde.config import get_config
        
        get_config.cache_clear()
        config = get_config()
        
        assert config.api_key is not None
        assert len(config.api_key) > 0

    def test_config_models_are_set(self):
        """Test that config has model names set."""
        from tilde.config import get_config
        
        get_config.cache_clear()
        config = get_config()
        
        assert config.llm_model is not None
        assert config.embedding_model is not None
        assert len(config.llm_model) > 0
        assert len(config.embedding_model) > 0
