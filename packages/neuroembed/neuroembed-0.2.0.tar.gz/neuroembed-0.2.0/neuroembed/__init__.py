# neuroembed/__init__.py
"""
NeuroEmbed - Model-agnostic semantic embedding enrichment framework.

NeuroEmbed modulates embeddings using semantic context, producing
controlled directional shifts in vector space while preserving
dimensionality and normalization.

Quick Start:
    from neuroembed import NeuroEmbed
    from neuroembed.encoders.sentence_transformer import SentenceTransformerEncoder
    
    encoder = SentenceTransformerEncoder()
    ne = NeuroEmbed(encoder=encoder, alpha=0.6)
    
    embedding = ne.embed("bank interest rate", ["finance", "RBI policy"])

Blending Strategies:
    - 'linear': Simple weighted average (default)
    - 'attention': Attention-weighted context aggregation
    - 'gated': Learnable per-dimension gating
    - 'time_decay': Temporal decay for conversations

Integrations:
    - LangChain: neuroembed.integrations.langchain
    - LlamaIndex: neuroembed.integrations.llamaindex
    - Vector DBs: neuroembed.integrations.vectordb
"""

__version__ = "0.2.0"

from .core import NeuroEmbed
from .context import (
    ContextInjector,
    create_linear_injector,
    create_attention_injector,
    create_gated_injector,
    create_conversation_injector,
    create_multi_context_injector,
)
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
from .explainability import (
    EmbeddingAnalysis,
    EmbeddingExplainer,
    EmbeddingVisualizer,
    SimilarityMatrix,
)

__all__ = [
    # Core
    "NeuroEmbed",
    "__version__",
    
    # Context injection
    "ContextInjector",
    "create_linear_injector",
    "create_attention_injector",
    "create_gated_injector",
    "create_conversation_injector",
    "create_multi_context_injector",
    
    # Strategies
    "BlendStrategy",
    "LinearBlend",
    "AttentionBlend",
    "GatedBlend",
    "TimeDecayBlend",
    "MultiContextBlend",
    "MultiContextConfig",
    "get_strategy",
    
    # Explainability
    "EmbeddingAnalysis",
    "EmbeddingExplainer",
    "EmbeddingVisualizer",
    "SimilarityMatrix",
]