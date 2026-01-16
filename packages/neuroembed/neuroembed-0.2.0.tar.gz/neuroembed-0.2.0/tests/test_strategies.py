# tests/test_strategies.py
"""
Tests for NeuroEmbed blending strategies.
"""

import numpy as np
import pytest
from neuroembed.strategies import (
    LinearBlend,
    AttentionBlend,
    GatedBlend,
    TimeDecayBlend,
    MultiContextBlend,
    MultiContextConfig,
    get_strategy,
)


@pytest.fixture
def sample_embeddings():
    """Create sample embeddings for testing."""
    np.random.seed(42)
    dim = 384
    
    base = np.random.randn(dim)
    base = base / np.linalg.norm(base)
    
    context = np.random.randn(5, dim)
    context = context / np.linalg.norm(context, axis=1, keepdims=True)
    
    return base, context, dim


class TestLinearBlend:
    def test_blend_preserves_norm(self, sample_embeddings):
        base, context, dim = sample_embeddings
        strategy = LinearBlend(alpha=0.7)
        
        result = strategy.blend(base, context)
        
        assert np.isclose(np.linalg.norm(result), 1.0, atol=1e-6)
    
    def test_alpha_1_returns_base(self, sample_embeddings):
        base, context, dim = sample_embeddings
        strategy = LinearBlend(alpha=1.0)
        
        result = strategy.blend(base, context)
        
        # Should be very close to base (normalized)
        assert np.allclose(result, base, atol=1e-6)
    
    def test_alpha_0_returns_context_mean(self, sample_embeddings):
        base, context, dim = sample_embeddings
        strategy = LinearBlend(alpha=0.0)
        
        result = strategy.blend(base, context)
        
        context_mean = np.mean(context, axis=0)
        context_mean = context_mean / np.linalg.norm(context_mean)
        
        assert np.allclose(result, context_mean, atol=1e-6)
    
    def test_empty_context_returns_base(self, sample_embeddings):
        base, _, dim = sample_embeddings
        strategy = LinearBlend(alpha=0.7)
        
        result = strategy.blend(base, np.array([]))
        
        assert np.allclose(result, base)
    
    def test_none_context_returns_base(self, sample_embeddings):
        base, _, dim = sample_embeddings
        strategy = LinearBlend(alpha=0.7)
        
        result = strategy.blend(base, None)
        
        assert np.allclose(result, base)


class TestAttentionBlend:
    def test_blend_preserves_norm(self, sample_embeddings):
        base, context, dim = sample_embeddings
        strategy = AttentionBlend(alpha=0.7, temperature=1.0)
        
        result = strategy.blend(base, context)
        
        assert np.isclose(np.linalg.norm(result), 1.0, atol=1e-6)
    
    def test_high_temperature_approaches_uniform(self, sample_embeddings):
        base, context, dim = sample_embeddings
        
        # Very high temperature should give nearly uniform weights
        strategy_high = AttentionBlend(alpha=0.5, temperature=100.0)
        result_high = strategy_high.blend(base, context)
        
        # Compare with linear blend (uniform weights)
        linear = LinearBlend(alpha=0.5)
        result_linear = linear.blend(base, context)
        
        # Should be similar (not exact due to numerical precision)
        similarity = result_high @ result_linear
        assert similarity > 0.99
    
    def test_empty_context_returns_base(self, sample_embeddings):
        base, _, dim = sample_embeddings
        strategy = AttentionBlend(alpha=0.7)
        
        result = strategy.blend(base, np.array([]))
        
        assert np.allclose(result, base)


class TestGatedBlend:
    def test_blend_preserves_norm(self, sample_embeddings):
        base, context, dim = sample_embeddings
        strategy = GatedBlend(dim=dim, alpha=0.7)
        
        result = strategy.blend(base, context)
        
        assert np.isclose(np.linalg.norm(result), 1.0, atol=1e-6)
    
    def test_get_gate_values(self, sample_embeddings):
        base, context, dim = sample_embeddings
        strategy = GatedBlend(dim=dim, alpha=0.7)
        
        gate = strategy.get_gate_values(base)
        
        assert gate.shape == (dim,)
        assert np.all(gate >= 0) and np.all(gate <= 1)
    
    def test_empty_context_returns_base(self, sample_embeddings):
        base, _, dim = sample_embeddings
        strategy = GatedBlend(dim=dim, alpha=0.7)
        
        result = strategy.blend(base, np.array([]))
        
        assert np.allclose(result, base)


class TestTimeDecayBlend:
    def test_blend_preserves_norm(self, sample_embeddings):
        base, context, dim = sample_embeddings
        strategy = TimeDecayBlend(alpha=0.7, decay_rate=0.3)
        
        result = strategy.blend(base, context)
        
        assert np.isclose(np.linalg.norm(result), 1.0, atol=1e-6)
    
    def test_decay_weights_sum_to_one(self, sample_embeddings):
        strategy = TimeDecayBlend(alpha=0.7, decay_rate=0.3, normalize_weights=True)
        
        weights = strategy.get_decay_weights(5)
        
        assert np.isclose(np.sum(weights), 1.0)
    
    def test_recent_has_higher_weight(self, sample_embeddings):
        strategy = TimeDecayBlend(alpha=0.7, decay_rate=0.5)
        
        weights = strategy.get_decay_weights(5)
        
        # Last weight should be highest
        assert weights[-1] > weights[-2] > weights[-3]
    
    def test_zero_decay_gives_uniform_weights(self, sample_embeddings):
        strategy = TimeDecayBlend(alpha=0.7, decay_rate=0.0, normalize_weights=True)
        
        weights = strategy.get_decay_weights(5)
        
        assert np.allclose(weights, 0.2)  # Uniform


class TestMultiContextBlend:
    def test_blend_with_dict(self, sample_embeddings):
        base, context, dim = sample_embeddings
        
        configs = [
            MultiContextConfig("source1", weight=0.6),
            MultiContextConfig("source2", weight=0.4),
        ]
        strategy = MultiContextBlend(configs=configs, alpha=0.7)
        
        context_dict = {
            "source1": context[:3],
            "source2": context[3:],
        }
        
        result = strategy.blend(base, context_dict=context_dict)
        
        assert np.isclose(np.linalg.norm(result), 1.0, atol=1e-6)
    
    def test_weights_affect_result(self, sample_embeddings):
        base, context, dim = sample_embeddings
        
        # All weight on source1
        configs1 = [
            MultiContextConfig("source1", weight=1.0),
            MultiContextConfig("source2", weight=0.0),
        ]
        strategy1 = MultiContextBlend(configs=configs1, alpha=0.5)
        
        # All weight on source2
        configs2 = [
            MultiContextConfig("source1", weight=0.0),
            MultiContextConfig("source2", weight=1.0),
        ]
        strategy2 = MultiContextBlend(configs=configs2, alpha=0.5)
        
        context_dict = {
            "source1": context[:2],
            "source2": context[3:],
        }
        
        result1 = strategy1.blend(base, context_dict=context_dict)
        result2 = strategy2.blend(base, context_dict=context_dict)
        
        # Results should be different
        assert not np.allclose(result1, result2)


class TestGetStrategy:
    def test_get_linear(self):
        strategy = get_strategy("linear", alpha=0.8)
        assert isinstance(strategy, LinearBlend)
        assert strategy.alpha == 0.8
    
    def test_get_attention(self):
        strategy = get_strategy("attention", alpha=0.7, temperature=0.5)
        assert isinstance(strategy, AttentionBlend)
        assert strategy.temperature == 0.5
    
    def test_get_gated(self):
        strategy = get_strategy("gated", dim=384, alpha=0.6)
        assert isinstance(strategy, GatedBlend)
        assert strategy.dim == 384
    
    def test_get_time_decay(self):
        strategy = get_strategy("time_decay", alpha=0.7, decay_rate=0.5)
        assert isinstance(strategy, TimeDecayBlend)
        assert strategy.decay_rate == 0.5
    
    def test_unknown_strategy_raises(self):
        with pytest.raises(ValueError):
            get_strategy("unknown")
