# tests/test_core.py
"""
Tests for the core NeuroEmbed class.
"""

import numpy as np
import pytest
from neuroembed import NeuroEmbed, MultiContextConfig
from neuroembed.encoders.sentence_transformer import SentenceTransformerEncoder


@pytest.fixture(scope="module")
def encoder():
    """Shared encoder for all tests."""
    return SentenceTransformerEncoder()


@pytest.fixture(scope="module")
def ne(encoder):
    """Shared NeuroEmbed instance."""
    return NeuroEmbed(encoder=encoder, alpha=0.6)


class TestNeuroEmbedBasic:
    def test_embed_without_context(self, ne, encoder):
        text = "hello world"
        
        result = ne.embed(text)
        expected = encoder.encode([text])[0]
        
        assert np.allclose(result, expected)
    
    def test_embed_with_context(self, ne, encoder):
        text = "bank interest rate"
        context = ["finance", "loans", "banking"]
        
        result = ne.embed(text, context)
        base = encoder.encode([text])[0]
        
        # Should be different from base
        assert not np.allclose(result, base)
        
        # Should be normalized
        assert np.isclose(np.linalg.norm(result), 1.0, atol=1e-6)
    
    def test_embed_returns_components(self, ne):
        text = "test query"
        context = ["context1", "context2"]
        
        result = ne.embed(text, context, return_components=True)
        
        assert "base" in result
        assert "enriched" in result
        assert "context" in result
        assert "context_texts" in result
        assert result["context_texts"] == context
    
    def test_get_embedding_dim(self, ne):
        dim = ne.get_embedding_dim()
        
        # all-MiniLM-L6-v2 has 384 dimensions
        assert dim == 384


class TestNeuroEmbedStrategies:
    def test_linear_strategy(self, encoder):
        ne = NeuroEmbed(encoder=encoder, alpha=0.7, strategy='linear')
        
        result = ne.embed("test", ["context"])
        
        assert np.isclose(np.linalg.norm(result), 1.0, atol=1e-6)
    
    def test_attention_strategy(self, encoder):
        ne = NeuroEmbed(encoder=encoder, alpha=0.7, strategy='attention')
        
        result = ne.embed("test", ["context1", "context2"])
        
        assert np.isclose(np.linalg.norm(result), 1.0, atol=1e-6)
    
    def test_time_decay_strategy(self, encoder):
        ne = NeuroEmbed(encoder=encoder, alpha=0.7, strategy='time_decay', decay_rate=0.3)
        
        result = ne.embed("test", ["old context", "recent context"])
        
        assert np.isclose(np.linalg.norm(result), 1.0, atol=1e-6)


class TestNeuroEmbedBatch:
    def test_embed_batch_shared_context(self, ne):
        texts = ["query 1", "query 2", "query 3"]
        context = ["shared context"]
        
        results = ne.embed_batch(texts, context, shared_context=True)
        
        assert results.shape[0] == 3
        assert results.shape[1] == 384
        
        # All should be normalized
        norms = np.linalg.norm(results, axis=1)
        assert np.allclose(norms, 1.0, atol=1e-6)
    
    def test_embed_batch_no_context(self, ne, encoder):
        texts = ["query 1", "query 2"]
        
        results = ne.embed_batch(texts)
        expected = encoder.encode(texts)
        
        assert np.allclose(results, expected)


class TestNeuroEmbedConversation:
    def test_embed_conversation(self, ne):
        query = "What about the rates?"
        history = [
            "I need a home loan",
            "What banks offer good deals?"
        ]
        
        result = ne.embed_conversation(query, history, decay_rate=0.3)
        
        assert np.isclose(np.linalg.norm(result), 1.0, atol=1e-6)
    
    def test_embed_conversation_empty_history(self, ne, encoder):
        query = "test query"
        
        result = ne.embed_conversation(query, [], decay_rate=0.3)
        expected = encoder.encode([query])[0]
        
        assert np.allclose(result, expected)


class TestNeuroEmbedMultiContext:
    def test_embed_multi_context(self, ne):
        text = "search query"
        context_sources = {
            "topic": ["AI", "machine learning"],
            "user": ["software developer"],
        }
        
        configs = [
            MultiContextConfig("topic", weight=0.6),
            MultiContextConfig("user", weight=0.4),
        ]
        
        result = ne.embed_multi_context(text, context_sources, configs)
        
        assert np.isclose(np.linalg.norm(result), 1.0, atol=1e-6)
    
    def test_embed_multi_context_without_configs(self, ne):
        text = "search query"
        context_sources = {
            "topic": ["AI"],
            "user": ["developer"],
        }
        
        # Should work with default equal weights
        result = ne.embed_multi_context(text, context_sources)
        
        assert np.isclose(np.linalg.norm(result), 1.0, atol=1e-6)


class TestNeuroEmbedCompare:
    def test_compare_embeddings(self, ne):
        text = "bank interest rate"
        context = ["finance", "loans"]
        
        metrics = ne.compare_embeddings(text, context)
        
        assert "cosine_similarity" in metrics
        assert "l2_distance" in metrics
        assert "context_influence" in metrics
        assert "base_norm" in metrics
        assert "enriched_norm" in metrics
        
        # Cosine similarity should be between 0 and 1 for related embeddings
        assert 0 < metrics["cosine_similarity"] <= 1
        
        # Norms should be 1 (normalized embeddings)
        assert np.isclose(metrics["enriched_norm"], 1.0, atol=1e-6)
