# neuroembed/core.py
"""
Core NeuroEmbed module.

Provides the main NeuroEmbed class for semantic embedding enrichment.
"""

import numpy as np
from typing import Optional, Union, Dict, List

from .context import ContextInjector
from .encoders.base import BaseEncoder
from .strategies import BlendStrategy, MultiContextConfig


class NeuroEmbed:
    """
    Model-agnostic semantic embedding enrichment framework.
    
    NeuroEmbed modulates embeddings using semantic context, producing
    controlled directional shifts in vector space while preserving
    dimensionality and normalization.
    
    Args:
        encoder: BaseEncoder instance for text encoding
        alpha: Base embedding weight (0-1). Default 0.7
        strategy: Blending strategy ('linear', 'attention', 'gated', 'time_decay')
        **strategy_kwargs: Additional arguments for the strategy
    
    Examples:
        # Basic usage
        encoder = SentenceTransformerEncoder()
        ne = NeuroEmbed(encoder=encoder, alpha=0.6)
        embedding = ne.embed("bank interest rate", ["finance", "RBI policy"])
        
        # With attention blending
        ne = NeuroEmbed(encoder=encoder, alpha=0.7, strategy='attention')
        
        # For conversations with time decay
        ne = NeuroEmbed(encoder=encoder, strategy='time_decay', decay_rate=0.5)
    """
    
    def __init__(
        self,
        encoder: BaseEncoder,
        alpha: float = 0.7,
        strategy: Union[str, BlendStrategy] = 'linear',
        **strategy_kwargs
    ):
        self.encoder = encoder
        self.alpha = alpha
        self.contextor = ContextInjector(
            alpha=alpha,
            strategy=strategy,
            **strategy_kwargs
        )
    
    @property
    def strategy(self) -> BlendStrategy:
        """Get the current blending strategy."""
        return self.contextor.strategy
    
    @strategy.setter
    def strategy(self, value: Union[str, BlendStrategy]):
        """Set a new blending strategy."""
        self.contextor.strategy = value
    
    def embed(
        self,
        text: str,
        context: Optional[List[str]] = None,
        return_components: bool = False
    ) -> Union[np.ndarray, Dict[str, np.ndarray]]:
        """
        Generate an enriched embedding for text with optional context.
        
        Args:
            text: Input text to embed
            context: Optional list of context strings
            return_components: If True, return dict with base, context, and enriched
        
        Returns:
            Enriched embedding (or dict if return_components=True)
        """
        base_emb = self.encoder.encode([text])[0]
        
        if context:
            ctx_embs = self.encoder.encode(context)
            enriched = self.contextor.enrich(base_emb, ctx_embs)
        else:
            enriched = base_emb
        
        if return_components:
            return {
                "base": base_emb,
                "context": ctx_embs if context else None,
                "enriched": enriched,
                "context_texts": context
            }
        
        return enriched
    
    def embed_multi_context(
        self,
        text: str,
        context_sources: Dict[str, List[str]],
        configs: Optional[List[MultiContextConfig]] = None
    ) -> np.ndarray:
        """
        Embed with multiple context sources.
        
        Args:
            text: Input text to embed
            context_sources: Dict mapping source name -> list of context strings
                            e.g., {"topic": ["AI", "ML"], "user": ["preferences..."]}
            configs: Optional list of MultiContextConfig for custom weights
        
        Returns:
            Enriched embedding
        """
        base_emb = self.encoder.encode([text])[0]
        
        if not context_sources:
            return base_emb
        
        # Encode all context sources
        context_dict = {}
        for name, texts in context_sources.items():
            if texts:
                context_dict[name] = self.encoder.encode(texts)
        
        if not context_dict:
            return base_emb
        
        # Create multi-context injector if configs provided
        if configs:
            from .strategies import MultiContextBlend
            strategy = MultiContextBlend(configs=configs, alpha=self.alpha)
            return strategy.blend(base_emb, context_dict=context_dict)
        
        # Default: equal weight for all sources
        combined = []
        for embs in context_dict.values():
            combined.extend(embs)
        
        return self.contextor.enrich(base_emb, np.array(combined))
    
    def embed_batch(
        self,
        texts: List[str],
        context: Optional[List[str]] = None,
        shared_context: bool = True
    ) -> np.ndarray:
        """
        Batch embed multiple texts.
        
        Args:
            texts: List of input texts
            context: Context strings (shared across all texts if shared_context=True)
            shared_context: Whether to use same context for all texts
        
        Returns:
            Array of enriched embeddings (batch x dim)
        """
        base_embs = self.encoder.encode(texts)
        
        if context is None:
            return base_embs
        
        ctx_embs = self.encoder.encode(context) if context else None
        return self.contextor.enrich_batch(base_embs, ctx_embs, shared_context)
    
    def embed_conversation(
        self,
        query: str,
        history: List[str],
        decay_rate: float = 0.3
    ) -> np.ndarray:
        """
        Embed a query with conversational history using time decay.
        
        More recent history has higher influence.
        
        Args:
            query: Current query/message
            history: List of previous messages (oldest first)
            decay_rate: How fast to decay older messages (0-1)
        
        Returns:
            Enriched embedding
        """
        from .strategies import TimeDecayBlend
        
        base_emb = self.encoder.encode([query])[0]
        
        if not history:
            return base_emb
        
        history_embs = self.encoder.encode(history)
        
        strategy = TimeDecayBlend(alpha=self.alpha, decay_rate=decay_rate)
        return strategy.blend(base_emb, history_embs)
    
    def get_embedding_dim(self) -> int:
        """Get the embedding dimension of the encoder."""
        sample = self.encoder.encode(["test"])[0]
        return sample.shape[0]
    
    def compare_embeddings(
        self,
        text: str,
        context: Optional[List[str]] = None
    ) -> Dict[str, float]:
        """
        Compare base vs enriched embedding metrics.
        
        Args:
            text: Input text
            context: Optional context strings
        
        Returns:
            Dict with similarity metrics
        """
        result = self.embed(text, context, return_components=True)
        
        base = result["base"]
        enriched = result["enriched"]
        
        # Compute metrics
        cosine_sim = float(base @ enriched)
        l2_distance = float(np.linalg.norm(base - enriched))
        
        # Compute shift magnitude
        if context and result["context"] is not None:
            context_mean = np.mean(result["context"], axis=0)
            context_influence = float(context_mean @ enriched)
        else:
            context_influence = None
        
        return {
            "cosine_similarity": cosine_sim,
            "l2_distance": l2_distance,
            "context_influence": context_influence,
            "base_norm": float(np.linalg.norm(base)),
            "enriched_norm": float(np.linalg.norm(enriched)),
        }
