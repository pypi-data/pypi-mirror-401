# neuroembed/context.py
"""
Context injection module for embedding enrichment.

Provides the ContextInjector class that wraps blending strategies
and offers a clean API for embedding enrichment.
"""

import numpy as np
from typing import Optional, Union, Dict, List
from .strategies import (
    BlendStrategy,
    LinearBlend,
    AttentionBlend,
    GatedBlend,
    TimeDecayBlend,
    MultiContextBlend,
    MultiContextConfig,
    get_strategy,
)


class ContextInjector:
    """
    Context injection engine for embedding enrichment.
    
    Supports multiple blending strategies and multi-context sources.
    
    Args:
        alpha: Base embedding weight (0-1). Default 0.7
        strategy: Blending strategy name or BlendStrategy instance.
                  Options: 'linear', 'attention', 'gated', 'time_decay', 'multi_context'
        **strategy_kwargs: Additional arguments passed to strategy constructor
    
    Examples:
        # Simple linear blend
        injector = ContextInjector(alpha=0.7)
        
        # Attention-weighted blending
        injector = ContextInjector(alpha=0.6, strategy='attention', temperature=0.5)
        
        # Time-decay for conversations
        injector = ContextInjector(alpha=0.7, strategy='time_decay', decay_rate=0.5)
        
        # Custom strategy instance
        strategy = GatedBlend(dim=384, alpha=0.7)
        injector = ContextInjector(strategy=strategy)
    """
    
    def __init__(
        self,
        alpha: float = 0.7,
        strategy: Union[str, BlendStrategy] = 'linear',
        **strategy_kwargs
    ):
        self.alpha = alpha
        
        if isinstance(strategy, BlendStrategy):
            self._strategy = strategy
        elif isinstance(strategy, str):
            # Pass alpha to strategy if not already in kwargs
            if 'alpha' not in strategy_kwargs:
                strategy_kwargs['alpha'] = alpha
            self._strategy = get_strategy(strategy, **strategy_kwargs)
        else:
            raise ValueError(f"strategy must be str or BlendStrategy, got {type(strategy)}")
    
    @property
    def strategy(self) -> BlendStrategy:
        """Get the current blending strategy."""
        return self._strategy
    
    @strategy.setter
    def strategy(self, value: Union[str, BlendStrategy]):
        """Set a new blending strategy."""
        if isinstance(value, BlendStrategy):
            self._strategy = value
        elif isinstance(value, str):
            self._strategy = get_strategy(value, alpha=self.alpha)
        else:
            raise ValueError(f"strategy must be str or BlendStrategy")
    
    def enrich(
        self,
        base_embedding: np.ndarray,
        context_embeddings: Optional[np.ndarray] = None,
        context_dict: Optional[Dict[str, np.ndarray]] = None,
        **kwargs
    ) -> np.ndarray:
        """
        Enrich a base embedding with context.
        
        Args:
            base_embedding: The base text embedding (1D array)
            context_embeddings: Context embeddings array (2D: n_contexts x dim)
            context_dict: For multi-context: dict mapping source name -> embeddings
            **kwargs: Additional arguments passed to the strategy
        
        Returns:
            Enriched embedding (1D array, L2 normalized)
        """
        if context_embeddings is None and context_dict is None:
            return base_embedding
        
        if context_embeddings is not None and len(context_embeddings) == 0:
            return base_embedding
        
        return self._strategy.blend(
            base_embedding=base_embedding,
            context_embeddings=context_embeddings,
            context_dict=context_dict,
            **kwargs
        )
    
    def enrich_batch(
        self,
        base_embeddings: np.ndarray,
        context_embeddings: Optional[np.ndarray] = None,
        shared_context: bool = True
    ) -> np.ndarray:
        """
        Enrich a batch of embeddings.
        
        Args:
            base_embeddings: Batch of base embeddings (2D: batch x dim)
            context_embeddings: Context embeddings (2D: n_contexts x dim)
            shared_context: If True, same context for all. If False, 
                           context_embeddings should be (batch x n_contexts x dim)
        
        Returns:
            Batch of enriched embeddings (2D: batch x dim)
        """
        results = []
        
        for i, base in enumerate(base_embeddings):
            if shared_context:
                ctx = context_embeddings
            else:
                ctx = context_embeddings[i] if context_embeddings is not None else None
            
            enriched = self.enrich(base, ctx)
            results.append(enriched)
        
        return np.array(results)


# Convenience factory functions
def create_linear_injector(alpha: float = 0.7) -> ContextInjector:
    """Create a ContextInjector with linear blending."""
    return ContextInjector(alpha=alpha, strategy='linear')


def create_attention_injector(
    alpha: float = 0.7,
    temperature: float = 1.0
) -> ContextInjector:
    """Create a ContextInjector with attention-weighted blending."""
    return ContextInjector(alpha=alpha, strategy='attention', temperature=temperature)


def create_gated_injector(
    dim: int,
    alpha: float = 0.7,
    learned_weights: Optional[tuple] = None
) -> ContextInjector:
    """Create a ContextInjector with gated blending."""
    return ContextInjector(
        alpha=alpha,
        strategy='gated',
        dim=dim,
        learned_weights=learned_weights
    )


def create_conversation_injector(
    alpha: float = 0.7,
    decay_rate: float = 0.3
) -> ContextInjector:
    """Create a ContextInjector with time-decay for conversations."""
    return ContextInjector(alpha=alpha, strategy='time_decay', decay_rate=decay_rate)


def create_multi_context_injector(
    configs: List[MultiContextConfig],
    alpha: float = 0.6
) -> ContextInjector:
    """Create a ContextInjector for multi-context blending."""
    strategy = MultiContextBlend(configs=configs, alpha=alpha)
    return ContextInjector(strategy=strategy)
