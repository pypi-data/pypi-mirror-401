# neuroembed/integrations/llamaindex.py
"""
LlamaIndex integration for NeuroEmbed.

Provides a LlamaIndex-compatible embedding wrapper that enables
context-aware embeddings in LlamaIndex pipelines.

Example:
    from neuroembed.integrations.llamaindex import NeuroEmbedLlamaIndex
    from neuroembed.encoders.sentence_transformer import SentenceTransformerEncoder
    
    encoder = SentenceTransformerEncoder()
    embed_model = NeuroEmbedLlamaIndex(
        encoder=encoder,
        alpha=0.6,
        default_context=["technical documentation", "software engineering"]
    )
    
    # Use with LlamaIndex
    from llama_index.core import VectorStoreIndex, Settings
    Settings.embed_model = embed_model
    index = VectorStoreIndex.from_documents(documents)
"""

from typing import List, Optional, Any, Union, Callable
import numpy as np

try:
    from llama_index.core.embeddings import BaseEmbedding
    from llama_index.core.bridge.pydantic import Field, PrivateAttr
    LLAMAINDEX_AVAILABLE = True
except ImportError:
    try:
        from llama_index.embeddings.base import BaseEmbedding
        from pydantic import Field, PrivateAttr
        LLAMAINDEX_AVAILABLE = True
    except ImportError:
        LLAMAINDEX_AVAILABLE = False
        BaseEmbedding = object
        Field = lambda **kwargs: None
        PrivateAttr = lambda **kwargs: None

from ..core import NeuroEmbed
from ..encoders.base import BaseEncoder
from ..strategies import BlendStrategy


class NeuroEmbedLlamaIndex(BaseEmbedding if LLAMAINDEX_AVAILABLE else object):
    """
    LlamaIndex-compatible embedding model using NeuroEmbed.
    
    Implements the LlamaIndex BaseEmbedding interface for seamless
    integration with LlamaIndex indexing and querying.
    
    Args:
        encoder: BaseEncoder instance for text encoding
        alpha: Base embedding weight (0-1). Default 0.7
        strategy: Blending strategy name or instance
        default_context: Default context for embeddings
        query_context: Context for query embeddings (overrides default)
        text_context: Context for text/document embeddings (overrides default)
        embed_batch_size: Batch size for embedding. Default 10
    """
    
    # Pydantic fields for LlamaIndex compatibility
    model_name: str = Field(default="neuroembed", description="Model name")
    embed_batch_size: int = Field(default=10, description="Batch size")
    
    # Private attributes
    _encoder: Any = PrivateAttr()
    _ne: Any = PrivateAttr()
    _alpha: float = PrivateAttr()
    _default_context: Optional[List[str]] = PrivateAttr()
    _query_context: Optional[List[str]] = PrivateAttr()
    _text_context: Optional[List[str]] = PrivateAttr()
    
    def __init__(
        self,
        encoder: BaseEncoder,
        alpha: float = 0.7,
        strategy: Union[str, BlendStrategy] = 'linear',
        default_context: Optional[List[str]] = None,
        query_context: Optional[List[str]] = None,
        text_context: Optional[List[str]] = None,
        embed_batch_size: int = 10,
        **kwargs
    ):
        if not LLAMAINDEX_AVAILABLE:
            raise ImportError(
                "LlamaIndex is not installed. Install with: pip install llama-index-core"
            )
        
        # Initialize parent class
        super().__init__(
            model_name="neuroembed",
            embed_batch_size=embed_batch_size,
            **kwargs
        )
        
        # Set private attributes
        self._encoder = encoder
        self._alpha = alpha
        self._ne = NeuroEmbed(
            encoder=encoder,
            alpha=alpha,
            strategy=strategy
        )
        self._default_context = default_context
        self._query_context = query_context or default_context
        self._text_context = text_context or default_context
    
    @classmethod
    def class_name(cls) -> str:
        """Return class name for LlamaIndex."""
        return "NeuroEmbedLlamaIndex"
    
    def set_query_context(self, context: List[str]) -> None:
        """Set context for query embeddings."""
        self._query_context = context
    
    def set_text_context(self, context: List[str]) -> None:
        """Set context for text/document embeddings."""
        self._text_context = context
    
    def set_context(self, context: List[str]) -> None:
        """Set context for both queries and texts."""
        self._query_context = context
        self._text_context = context
    
    def _get_query_embedding(self, query: str) -> List[float]:
        """
        Get embedding for a query string.
        
        Args:
            query: Query text
        
        Returns:
            Embedding as list of floats
        """
        emb = self._ne.embed(query, self._query_context)
        return emb.tolist()
    
    def _get_text_embedding(self, text: str) -> List[float]:
        """
        Get embedding for a text/document string.
        
        Args:
            text: Text to embed
        
        Returns:
            Embedding as list of floats
        """
        emb = self._ne.embed(text, self._text_context)
        return emb.tolist()
    
    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Get embeddings for multiple texts.
        
        Args:
            texts: List of texts
        
        Returns:
            List of embeddings
        """
        embeddings = []
        for text in texts:
            emb = self._ne.embed(text, self._text_context)
            embeddings.append(emb.tolist())
        return embeddings
    
    async def _aget_query_embedding(self, query: str) -> List[float]:
        """Async version of _get_query_embedding."""
        return self._get_query_embedding(query)
    
    async def _aget_text_embedding(self, text: str) -> List[float]:
        """Async version of _get_text_embedding."""
        return self._get_text_embedding(text)
    
    def embed_with_context(
        self,
        text: str,
        context: List[str]
    ) -> List[float]:
        """
        Embed text with custom context.
        
        Args:
            text: Text to embed
            context: Custom context
        
        Returns:
            Embedding as list of floats
        """
        emb = self._ne.embed(text, context)
        return emb.tolist()
    
    @property
    def embedding_dimension(self) -> int:
        """Get the embedding dimension."""
        return self._ne.get_embedding_dim()


class NeuroEmbedNodePostprocessor:
    """
    LlamaIndex node postprocessor that re-ranks using context-aware embeddings.
    
    This postprocessor can re-compute similarity scores using NeuroEmbed
    with additional context from the query or conversation history.
    
    Example:
        postprocessor = NeuroEmbedNodePostprocessor(
            encoder=encoder,
            alpha=0.6
        )
        
        query_engine = index.as_query_engine(
            node_postprocessors=[postprocessor]
        )
    """
    
    def __init__(
        self,
        encoder: BaseEncoder,
        alpha: float = 0.6,
        strategy: str = 'linear',
        top_k: int = 5
    ):
        self.ne = NeuroEmbed(encoder=encoder, alpha=alpha, strategy=strategy)
        self.encoder = encoder
        self.top_k = top_k
        self._context: Optional[List[str]] = None
    
    def set_context(self, context: List[str]) -> None:
        """Set the context for re-ranking."""
        self._context = context
    
    def postprocess_nodes(
        self,
        nodes: List[Any],
        query_str: str,
        context: Optional[List[str]] = None
    ) -> List[Any]:
        """
        Re-rank nodes using context-aware embeddings.
        
        Args:
            nodes: List of retrieved nodes
            query_str: Original query string
            context: Optional context (uses stored context if None)
        
        Returns:
            Re-ranked list of nodes
        """
        ctx = context or self._context
        
        # Get enriched query embedding
        query_emb = self.ne.embed(query_str, ctx)
        
        # Re-score each node
        scored_nodes = []
        for node in nodes:
            # Get node text and compute embedding
            node_text = node.get_content() if hasattr(node, 'get_content') else str(node)
            node_emb = self.encoder.encode([node_text])[0]
            
            # Compute new similarity score
            score = float(query_emb @ node_emb)
            scored_nodes.append((node, score))
        
        # Sort by score and return top_k
        scored_nodes.sort(key=lambda x: x[1], reverse=True)
        return [node for node, _ in scored_nodes[:self.top_k]]
