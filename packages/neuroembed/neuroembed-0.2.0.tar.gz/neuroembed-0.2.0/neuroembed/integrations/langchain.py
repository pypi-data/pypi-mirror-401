# neuroembed/integrations/langchain.py
"""
LangChain integration for NeuroEmbed.

Provides a LangChain-compatible Embeddings class that wraps NeuroEmbed
for seamless integration with LangChain pipelines.

Example:
    from neuroembed.integrations.langchain import NeuroEmbedLangChain
    from neuroembed.encoders.sentence_transformer import SentenceTransformerEncoder
    
    encoder = SentenceTransformerEncoder()
    embeddings = NeuroEmbedLangChain(
        encoder=encoder,
        alpha=0.6,
        default_context=["AI assistant", "helpful responses"]
    )
    
    # Use with LangChain
    from langchain.vectorstores import Chroma
    vectorstore = Chroma.from_documents(docs, embeddings)
"""

from typing import List, Optional, Dict, Any, Union
import numpy as np

try:
    from langchain_core.embeddings import Embeddings
    LANGCHAIN_AVAILABLE = True
except ImportError:
    # Fallback for older versions or missing langchain
    try:
        from langchain.embeddings.base import Embeddings
        LANGCHAIN_AVAILABLE = True
    except ImportError:
        LANGCHAIN_AVAILABLE = False
        Embeddings = object  # Dummy base class

from ..core import NeuroEmbed
from ..encoders.base import BaseEncoder
from ..strategies import BlendStrategy


class NeuroEmbedLangChain(Embeddings):
    """
    LangChain-compatible embedding wrapper for NeuroEmbed.
    
    Implements the LangChain Embeddings interface, allowing NeuroEmbed
    to be used with any LangChain component that accepts embeddings.
    
    Args:
        encoder: BaseEncoder instance for text encoding
        alpha: Base embedding weight (0-1). Default 0.7
        strategy: Blending strategy name or instance
        default_context: Default context for all embeddings (optional)
        query_context: Context specifically for query embeddings (optional)
        document_context: Context specifically for document embeddings (optional)
        **strategy_kwargs: Additional strategy parameters
    
    Features:
        - Separate context for queries vs documents
        - Dynamic context setting per-call
        - Full LangChain compatibility
    """
    
    def __init__(
        self,
        encoder: BaseEncoder,
        alpha: float = 0.7,
        strategy: Union[str, BlendStrategy] = 'linear',
        default_context: Optional[List[str]] = None,
        query_context: Optional[List[str]] = None,
        document_context: Optional[List[str]] = None,
        **strategy_kwargs
    ):
        if not LANGCHAIN_AVAILABLE:
            raise ImportError(
                "LangChain is not installed. Install with: pip install langchain-core"
            )
        
        self.ne = NeuroEmbed(
            encoder=encoder,
            alpha=alpha,
            strategy=strategy,
            **strategy_kwargs
        )
        self.encoder = encoder
        self.alpha = alpha
        self.default_context = default_context
        self.query_context = query_context or default_context
        self.document_context = document_context or default_context
    
    def set_query_context(self, context: List[str]) -> None:
        """Set the context for query embeddings."""
        self.query_context = context
    
    def set_document_context(self, context: List[str]) -> None:
        """Set the context for document embeddings."""
        self.document_context = context
    
    def set_context(self, context: List[str]) -> None:
        """Set context for both queries and documents."""
        self.query_context = context
        self.document_context = context
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of documents.
        
        Uses document_context for enrichment.
        
        Args:
            texts: List of document texts to embed
        
        Returns:
            List of embedding vectors as lists of floats
        """
        embeddings = []
        for text in texts:
            emb = self.ne.embed(text, self.document_context)
            embeddings.append(emb.tolist())
        return embeddings
    
    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query.
        
        Uses query_context for enrichment.
        
        Args:
            text: Query text to embed
        
        Returns:
            Embedding vector as a list of floats
        """
        emb = self.ne.embed(text, self.query_context)
        return emb.tolist()
    
    def embed_with_context(
        self,
        text: str,
        context: List[str]
    ) -> List[float]:
        """
        Embed a single text with custom context.
        
        Args:
            text: Text to embed
            context: Custom context for this embedding
        
        Returns:
            Embedding vector as a list of floats
        """
        emb = self.ne.embed(text, context)
        return emb.tolist()
    
    async def aembed_documents(self, texts: List[str]) -> List[List[float]]:
        """Async version of embed_documents."""
        return self.embed_documents(texts)
    
    async def aembed_query(self, text: str) -> List[float]:
        """Async version of embed_query."""
        return self.embed_query(text)
    
    @property
    def embedding_dimension(self) -> int:
        """Get the embedding dimension."""
        return self.ne.get_embedding_dim()


class NeuroEmbedLangChainRetriever:
    """
    Enhanced retriever that uses NeuroEmbed for context-aware retrieval.
    
    Provides methods to dynamically adjust context based on:
    - Conversation history
    - User profile
    - Session data
    
    Example:
        retriever = NeuroEmbedLangChainRetriever(
            encoder=encoder,
            vectorstore=chroma_db,
            alpha=0.6
        )
        
        # Search with conversation context
        docs = retriever.search_with_history(
            query="What about the rates?",
            history=["I'm interested in home loans", "What banks offer the best deals?"]
        )
    """
    
    def __init__(
        self,
        encoder: BaseEncoder,
        vectorstore: Any,
        alpha: float = 0.6,
        strategy: str = 'linear'
    ):
        self.ne = NeuroEmbed(encoder=encoder, alpha=alpha, strategy=strategy)
        self.encoder = encoder
        self.vectorstore = vectorstore
    
    def search_with_context(
        self,
        query: str,
        context: List[str],
        k: int = 4
    ) -> List[Any]:
        """
        Search with explicit context.
        
        Args:
            query: Search query
            context: Context strings for enrichment
            k: Number of results to return
        
        Returns:
            List of retrieved documents
        """
        enriched_query = self.ne.embed(query, context)
        return self.vectorstore.similarity_search_by_vector(
            enriched_query.tolist(), k=k
        )
    
    def search_with_history(
        self,
        query: str,
        history: List[str],
        k: int = 4,
        decay_rate: float = 0.3
    ) -> List[Any]:
        """
        Search with conversation history using time decay.
        
        Args:
            query: Current query
            history: Previous messages (oldest first)
            k: Number of results
            decay_rate: Time decay rate for history
        
        Returns:
            List of retrieved documents
        """
        enriched_query = self.ne.embed_conversation(query, history, decay_rate)
        return self.vectorstore.similarity_search_by_vector(
            enriched_query.tolist(), k=k
        )
