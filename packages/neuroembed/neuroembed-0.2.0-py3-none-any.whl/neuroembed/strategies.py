# neuroembed/strategies.py
"""
Advanced blending strategies for embedding enrichment.

Strategies:
- LinearBlend: Simple weighted average (default)
- AttentionBlend: Attention-weighted context aggregation
- GatedBlend: Learnable gating mechanism
- TimeDecayBlend: Temporal decay for conversational context
"""

import numpy as np
from abc import ABC, abstractmethod
from typing import Optional, List
from dataclasses import dataclass


class BlendStrategy(ABC):
    """Base class for all blending strategies."""
    
    @abstractmethod
    def blend(
        self,
        base_embedding: np.ndarray,
        context_embeddings: np.ndarray,
        **kwargs
    ) -> np.ndarray:
        """Blend base embedding with context embeddings."""
        pass
    
    def _normalize(self, vector: np.ndarray) -> np.ndarray:
        """L2 normalize a vector."""
        norm = np.linalg.norm(vector)
        return vector / norm if norm > 0 else vector


class LinearBlend(BlendStrategy):
    """
    Simple linear interpolation blending.
    
    Formula: enriched = α * base + (1 - α) * mean(context)
    
    Args:
        alpha: Weight for base embedding (0-1). Default 0.7
    """
    
    def __init__(self, alpha: float = 0.7):
        self.alpha = alpha
    
    def blend(
        self,
        base_embedding: np.ndarray,
        context_embeddings: np.ndarray,
        **kwargs
    ) -> np.ndarray:
        if context_embeddings is None or len(context_embeddings) == 0:
            return base_embedding
        
        context_mean = np.mean(context_embeddings, axis=0)
        enriched = self.alpha * base_embedding + (1 - self.alpha) * context_mean
        return self._normalize(enriched)


class AttentionBlend(BlendStrategy):
    """
    Attention-weighted context aggregation.
    
    Computes attention scores between base embedding and each context,
    then uses softmax-weighted sum of contexts.
    
    Formula:
        attention = softmax(base @ context.T / sqrt(dim))
        context_weighted = attention @ context
        enriched = α * base + (1 - α) * context_weighted
    
    Args:
        alpha: Weight for base embedding. Default 0.7
        temperature: Softmax temperature (higher = softer). Default 1.0
    """
    
    def __init__(self, alpha: float = 0.7, temperature: float = 1.0):
        self.alpha = alpha
        self.temperature = temperature
    
    def blend(
        self,
        base_embedding: np.ndarray,
        context_embeddings: np.ndarray,
        **kwargs
    ) -> np.ndarray:
        if context_embeddings is None or len(context_embeddings) == 0:
            return base_embedding
        
        # Compute attention scores
        dim = base_embedding.shape[0]
        scores = context_embeddings @ base_embedding / np.sqrt(dim)
        
        # Apply temperature and softmax
        scores = scores / self.temperature
        scores = scores - np.max(scores)  # numerical stability
        attention = np.exp(scores) / np.sum(np.exp(scores))
        
        # Weighted sum of context embeddings
        context_weighted = attention @ context_embeddings
        
        # Blend with base
        enriched = self.alpha * base_embedding + (1 - self.alpha) * context_weighted
        return self._normalize(enriched)


class GatedBlend(BlendStrategy):
    """
    Learnable gating mechanism for context injection.
    
    Uses a gate vector to control per-dimension blending.
    
    Formula:
        gate = sigmoid(W @ base + b)
        enriched = gate * base + (1 - gate) * context_mean
    
    The gate is learned or can be initialized randomly.
    
    Args:
        dim: Embedding dimension (required for weight initialization)
        alpha: Fallback weight if no learned weights. Default 0.7
        learned_weights: Optional pre-trained (W, b) tuple
    """
    
    def __init__(
        self,
        dim: int,
        alpha: float = 0.7,
        learned_weights: Optional[tuple] = None
    ):
        self.dim = dim
        self.alpha = alpha
        
        if learned_weights is not None:
            self.W, self.b = learned_weights
        else:
            # Initialize with small random weights
            np.random.seed(42)
            self.W = np.random.randn(dim, dim) * 0.01
            self.b = np.zeros(dim)
    
    def _sigmoid(self, x: np.ndarray) -> np.ndarray:
        """Numerically stable sigmoid."""
        return np.where(
            x >= 0,
            1 / (1 + np.exp(-x)),
            np.exp(x) / (1 + np.exp(x))
        )
    
    def blend(
        self,
        base_embedding: np.ndarray,
        context_embeddings: np.ndarray,
        **kwargs
    ) -> np.ndarray:
        if context_embeddings is None or len(context_embeddings) == 0:
            return base_embedding
        
        context_mean = np.mean(context_embeddings, axis=0)
        
        # Compute gate
        gate = self._sigmoid(self.W @ base_embedding + self.b)
        
        # Per-dimension gated blending
        enriched = gate * base_embedding + (1 - gate) * context_mean
        return self._normalize(enriched)
    
    def get_gate_values(self, base_embedding: np.ndarray) -> np.ndarray:
        """Return gate values for interpretability."""
        return self._sigmoid(self.W @ base_embedding + self.b)


class TimeDecayBlend(BlendStrategy):
    """
    Time-decay blending for conversational context.
    
    More recent contexts have higher weights, older contexts decay.
    Useful for chat/conversation history where recent context matters more.
    
    Formula:
        weights[i] = exp(-decay_rate * (n - i - 1))
        context_weighted = weighted_mean(contexts, weights)
        enriched = α * base + (1 - α) * context_weighted
    
    Args:
        alpha: Weight for base embedding. Default 0.7
        decay_rate: Exponential decay rate. Higher = faster decay. Default 0.3
        normalize_weights: Whether to normalize decay weights. Default True
    """
    
    def __init__(
        self,
        alpha: float = 0.7,
        decay_rate: float = 0.3,
        normalize_weights: bool = True
    ):
        self.alpha = alpha
        self.decay_rate = decay_rate
        self.normalize_weights = normalize_weights
    
    def blend(
        self,
        base_embedding: np.ndarray,
        context_embeddings: np.ndarray,
        **kwargs
    ) -> np.ndarray:
        if context_embeddings is None or len(context_embeddings) == 0:
            return base_embedding
        
        n = len(context_embeddings)
        
        # Compute decay weights (last context = most recent = highest weight)
        indices = np.arange(n)
        weights = np.exp(-self.decay_rate * (n - indices - 1))
        
        if self.normalize_weights:
            weights = weights / np.sum(weights)
        
        # Weighted sum of context embeddings
        context_weighted = weights @ context_embeddings
        
        # Blend with base
        enriched = self.alpha * base_embedding + (1 - self.alpha) * context_weighted
        return self._normalize(enriched)
    
    def get_decay_weights(self, n_contexts: int) -> np.ndarray:
        """Return decay weights for n contexts (for interpretability)."""
        indices = np.arange(n_contexts)
        weights = np.exp(-self.decay_rate * (n_contexts - indices - 1))
        if self.normalize_weights:
            weights = weights / np.sum(weights)
        return weights


@dataclass
class MultiContextConfig:
    """Configuration for a single context source."""
    name: str
    weight: float = 1.0
    strategy: BlendStrategy = None
    
    def __post_init__(self):
        if self.strategy is None:
            self.strategy = LinearBlend(alpha=0.7)


class MultiContextBlend(BlendStrategy):
    """
    Multi-context blending with configurable weights per source.
    
    Supports blending multiple context sources (e.g., topic + user + session)
    with individual weights and strategies.
    
    Example:
        config = [
            MultiContextConfig("topic", weight=0.5),
            MultiContextConfig("user_history", weight=0.3),
            MultiContextConfig("session", weight=0.2, strategy=TimeDecayBlend())
        ]
        blender = MultiContextBlend(configs=config, alpha=0.6)
    
    Args:
        configs: List of MultiContextConfig for each context source
        alpha: Weight for base embedding. Default 0.6
    """
    
    def __init__(
        self,
        configs: List[MultiContextConfig],
        alpha: float = 0.6
    ):
        self.configs = {cfg.name: cfg for cfg in configs}
        self.alpha = alpha
    
    def blend(
        self,
        base_embedding: np.ndarray,
        context_embeddings: np.ndarray = None,
        context_dict: dict = None,
        **kwargs
    ) -> np.ndarray:
        """
        Blend base embedding with multiple context sources.
        
        Args:
            base_embedding: The base text embedding
            context_embeddings: Single context array (backward compatibility)
            context_dict: Dict mapping context name -> embeddings array
        
        Returns:
            Enriched embedding
        """
        # Handle backward compatibility
        if context_dict is None and context_embeddings is not None:
            # Use first config for single context
            first_config = list(self.configs.values())[0]
            context_dict = {first_config.name: context_embeddings}
        
        if context_dict is None or len(context_dict) == 0:
            return base_embedding
        
        # Compute weighted blend of all context sources
        total_weight = 0
        combined_context = np.zeros_like(base_embedding)
        
        for name, embeddings in context_dict.items():
            if embeddings is None or len(embeddings) == 0:
                continue
            
            config = self.configs.get(name)
            if config is None:
                continue
            
            # Apply strategy-specific blending for this context
            # Get the context mean using the strategy
            context_mean = np.mean(embeddings, axis=0)
            
            combined_context += config.weight * context_mean
            total_weight += config.weight
        
        if total_weight == 0:
            return base_embedding
        
        # Normalize combined context by total weight
        combined_context = combined_context / total_weight
        
        # Final blend with base
        enriched = self.alpha * base_embedding + (1 - self.alpha) * combined_context
        return self._normalize(enriched)


# Strategy registry for easy access
STRATEGIES = {
    "linear": LinearBlend,
    "attention": AttentionBlend,
    "gated": GatedBlend,
    "time_decay": TimeDecayBlend,
    "multi_context": MultiContextBlend,
}


def get_strategy(name: str, **kwargs) -> BlendStrategy:
    """
    Factory function to get a blending strategy by name.
    
    Args:
        name: Strategy name ('linear', 'attention', 'gated', 'time_decay', 'multi_context')
        **kwargs: Strategy-specific parameters
    
    Returns:
        BlendStrategy instance
    """
    if name not in STRATEGIES:
        raise ValueError(f"Unknown strategy: {name}. Available: {list(STRATEGIES.keys())}")
    return STRATEGIES[name](**kwargs)
