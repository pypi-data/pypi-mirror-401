# neuroembed/integrations/vectordb.py
"""
Vector Database pre-processors for NeuroEmbed.

Provides pre-processing layers for popular vector databases that
inject context-awareness into embeddings before storage/querying.

Supported databases:
- ChromaDB
- Pinecone
- Weaviate

Example:
    from neuroembed.integrations.vectordb import ChromaPreprocessor
    from neuroembed.encoders.sentence_transformer import SentenceTransformerEncoder
    
    encoder = SentenceTransformerEncoder()
    preprocessor = ChromaPreprocessor(
        encoder=encoder,
        alpha=0.6,
        collection_context={"tech_docs": ["software", "engineering"]}
    )
    
    # Get enriched embeddings for a collection
    embeddings = preprocessor.prepare_documents(
        texts=["Python tutorial", "API reference"],
        collection_name="tech_docs"
    )
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Tuple, Union
import numpy as np
from dataclasses import dataclass

from ..core import NeuroEmbed
from ..encoders.base import BaseEncoder
from ..strategies import BlendStrategy


@dataclass
class VectorRecord:
    """A single vector record for database insertion."""
    id: str
    embedding: List[float]
    metadata: Dict[str, Any]
    text: Optional[str] = None


class VectorDBPreprocessor(ABC):
    """
    Abstract base class for vector database preprocessors.
    
    Provides common functionality for preparing context-enriched
    embeddings for vector database operations.
    """
    
    def __init__(
        self,
        encoder: BaseEncoder,
        alpha: float = 0.7,
        strategy: Union[str, BlendStrategy] = 'linear',
        default_context: Optional[List[str]] = None,
        collection_context: Optional[Dict[str, List[str]]] = None,
        **strategy_kwargs
    ):
        """
        Initialize the preprocessor.
        
        Args:
            encoder: BaseEncoder instance
            alpha: Base embedding weight
            strategy: Blending strategy
            default_context: Default context for all embeddings
            collection_context: Dict mapping collection/index name to context
        """
        self.ne = NeuroEmbed(
            encoder=encoder,
            alpha=alpha,
            strategy=strategy,
            **strategy_kwargs
        )
        self.encoder = encoder
        self.alpha = alpha
        self.default_context = default_context
        self.collection_context = collection_context or {}
    
    def get_context_for_collection(
        self,
        collection_name: Optional[str] = None
    ) -> Optional[List[str]]:
        """Get context for a specific collection."""
        if collection_name and collection_name in self.collection_context:
            return self.collection_context[collection_name]
        return self.default_context
    
    def set_collection_context(
        self,
        collection_name: str,
        context: List[str]
    ) -> None:
        """Set context for a specific collection."""
        self.collection_context[collection_name] = context
    
    def embed_text(
        self,
        text: str,
        context: Optional[List[str]] = None,
        collection_name: Optional[str] = None
    ) -> np.ndarray:
        """
        Embed a single text with context.
        
        Args:
            text: Text to embed
            context: Explicit context (overrides collection context)
            collection_name: Collection to get context from
        
        Returns:
            Enriched embedding
        """
        ctx = context or self.get_context_for_collection(collection_name)
        return self.ne.embed(text, ctx)
    
    def embed_texts(
        self,
        texts: List[str],
        context: Optional[List[str]] = None,
        collection_name: Optional[str] = None
    ) -> np.ndarray:
        """
        Embed multiple texts with shared context.
        
        Args:
            texts: Texts to embed
            context: Explicit context
            collection_name: Collection to get context from
        
        Returns:
            Array of enriched embeddings
        """
        ctx = context or self.get_context_for_collection(collection_name)
        embeddings = [self.ne.embed(text, ctx) for text in texts]
        return np.array(embeddings)
    
    @abstractmethod
    def prepare_documents(
        self,
        texts: List[str],
        ids: Optional[List[str]] = None,
        metadatas: Optional[List[Dict[str, Any]]] = None,
        collection_name: Optional[str] = None,
        context: Optional[List[str]] = None
    ) -> List[VectorRecord]:
        """Prepare documents for database insertion."""
        pass
    
    @abstractmethod
    def prepare_query(
        self,
        query: str,
        collection_name: Optional[str] = None,
        context: Optional[List[str]] = None
    ) -> List[float]:
        """Prepare a query embedding."""
        pass


class ChromaPreprocessor(VectorDBPreprocessor):
    """
    ChromaDB preprocessor for context-enriched embeddings.
    
    Provides methods to prepare embeddings for ChromaDB collections
    with automatic context injection.
    
    Example:
        preprocessor = ChromaPreprocessor(
            encoder=encoder,
            collection_context={
                "technical": ["software", "API", "documentation"],
                "general": ["help", "support", "FAQ"]
            }
        )
        
        # Prepare for insertion
        records = preprocessor.prepare_documents(
            texts=["How to use the API", "Getting started guide"],
            collection_name="technical"
        )
        
        # Use with ChromaDB
        collection.add(
            embeddings=[r.embedding for r in records],
            documents=[r.text for r in records],
            ids=[r.id for r in records],
            metadatas=[r.metadata for r in records]
        )
    """
    
    def prepare_documents(
        self,
        texts: List[str],
        ids: Optional[List[str]] = None,
        metadatas: Optional[List[Dict[str, Any]]] = None,
        collection_name: Optional[str] = None,
        context: Optional[List[str]] = None
    ) -> List[VectorRecord]:
        """
        Prepare documents for ChromaDB insertion.
        
        Args:
            texts: Document texts
            ids: Optional document IDs (auto-generated if not provided)
            metadatas: Optional metadata dicts
            collection_name: Collection name for context lookup
            context: Explicit context (overrides collection context)
        
        Returns:
            List of VectorRecord objects ready for insertion
        """
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(texts))]
        
        if metadatas is None:
            metadatas = [{} for _ in texts]
        
        embeddings = self.embed_texts(texts, context, collection_name)
        
        records = []
        for i, (text, emb, meta) in enumerate(zip(texts, embeddings, metadatas)):
            # Add NeuroEmbed metadata
            enriched_meta = {
                **meta,
                "_neuroembed_enriched": True,
                "_neuroembed_alpha": self.alpha,
            }
            
            records.append(VectorRecord(
                id=ids[i],
                embedding=emb.tolist(),
                metadata=enriched_meta,
                text=text
            ))
        
        return records
    
    def prepare_query(
        self,
        query: str,
        collection_name: Optional[str] = None,
        context: Optional[List[str]] = None
    ) -> List[float]:
        """
        Prepare a query embedding for ChromaDB search.
        
        Args:
            query: Query text
            collection_name: Collection name for context lookup
            context: Explicit context
        
        Returns:
            Query embedding as list of floats
        """
        emb = self.embed_text(query, context, collection_name)
        return emb.tolist()
    
    def add_to_collection(
        self,
        collection: Any,
        texts: List[str],
        ids: Optional[List[str]] = None,
        metadatas: Optional[List[Dict[str, Any]]] = None,
        context: Optional[List[str]] = None
    ) -> None:
        """
        Add documents directly to a ChromaDB collection.
        
        Args:
            collection: ChromaDB collection object
            texts: Document texts
            ids: Optional IDs
            metadatas: Optional metadata
            context: Optional context
        """
        records = self.prepare_documents(texts, ids, metadatas, context=context)
        
        collection.add(
            embeddings=[r.embedding for r in records],
            documents=[r.text for r in records],
            ids=[r.id for r in records],
            metadatas=[r.metadata for r in records]
        )
    
    def query_collection(
        self,
        collection: Any,
        query: str,
        n_results: int = 10,
        context: Optional[List[str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Query a ChromaDB collection with context-enriched embedding.
        
        Args:
            collection: ChromaDB collection object
            query: Query text
            n_results: Number of results
            context: Query context
            **kwargs: Additional ChromaDB query arguments
        
        Returns:
            ChromaDB query results
        """
        query_emb = self.prepare_query(query, context=context)
        
        return collection.query(
            query_embeddings=[query_emb],
            n_results=n_results,
            **kwargs
        )


class PineconePreprocessor(VectorDBPreprocessor):
    """
    Pinecone preprocessor for context-enriched embeddings.
    
    Example:
        preprocessor = PineconePreprocessor(
            encoder=encoder,
            namespace_context={
                "products": ["e-commerce", "catalog", "shopping"],
                "support": ["customer service", "help", "FAQ"]
            }
        )
        
        # Prepare vectors for upsert
        vectors = preprocessor.prepare_for_upsert(
            texts=["Product description"],
            ids=["prod_1"],
            namespace="products"
        )
        
        # Use with Pinecone
        index.upsert(vectors=vectors, namespace="products")
    """
    
    def __init__(
        self,
        encoder: BaseEncoder,
        alpha: float = 0.7,
        strategy: Union[str, BlendStrategy] = 'linear',
        default_context: Optional[List[str]] = None,
        namespace_context: Optional[Dict[str, List[str]]] = None,
        **strategy_kwargs
    ):
        super().__init__(
            encoder=encoder,
            alpha=alpha,
            strategy=strategy,
            default_context=default_context,
            collection_context=namespace_context,
            **strategy_kwargs
        )
    
    def prepare_documents(
        self,
        texts: List[str],
        ids: Optional[List[str]] = None,
        metadatas: Optional[List[Dict[str, Any]]] = None,
        collection_name: Optional[str] = None,
        context: Optional[List[str]] = None
    ) -> List[VectorRecord]:
        """Prepare documents as VectorRecord objects."""
        if ids is None:
            ids = [f"vec_{i}" for i in range(len(texts))]
        
        if metadatas is None:
            metadatas = [{} for _ in texts]
        
        embeddings = self.embed_texts(texts, context, collection_name)
        
        records = []
        for i, (text, emb, meta) in enumerate(zip(texts, embeddings, metadatas)):
            enriched_meta = {
                **meta,
                "text": text,
                "_neuroembed_enriched": True,
            }
            
            records.append(VectorRecord(
                id=ids[i],
                embedding=emb.tolist(),
                metadata=enriched_meta,
                text=text
            ))
        
        return records
    
    def prepare_query(
        self,
        query: str,
        collection_name: Optional[str] = None,
        context: Optional[List[str]] = None
    ) -> List[float]:
        """Prepare a query embedding."""
        emb = self.embed_text(query, context, collection_name)
        return emb.tolist()
    
    def prepare_for_upsert(
        self,
        texts: List[str],
        ids: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        namespace: Optional[str] = None,
        context: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Prepare vectors in Pinecone upsert format.
        
        Args:
            texts: Document texts
            ids: Vector IDs
            metadatas: Optional metadata
            namespace: Namespace for context lookup
            context: Explicit context
        
        Returns:
            List of dicts ready for Pinecone upsert
        """
        records = self.prepare_documents(
            texts, ids, metadatas, namespace, context
        )
        
        return [
            {
                "id": r.id,
                "values": r.embedding,
                "metadata": r.metadata
            }
            for r in records
        ]
    
    def query_index(
        self,
        index: Any,
        query: str,
        top_k: int = 10,
        namespace: Optional[str] = None,
        context: Optional[List[str]] = None,
        **kwargs
    ) -> Any:
        """
        Query a Pinecone index with context-enriched embedding.
        
        Args:
            index: Pinecone index object
            query: Query text
            top_k: Number of results
            namespace: Namespace to query
            context: Query context
            **kwargs: Additional Pinecone query arguments
        
        Returns:
            Pinecone query results
        """
        query_emb = self.prepare_query(query, namespace, context)
        
        return index.query(
            vector=query_emb,
            top_k=top_k,
            namespace=namespace,
            **kwargs
        )


class WeaviatePreprocessor(VectorDBPreprocessor):
    """
    Weaviate preprocessor for context-enriched embeddings.
    
    Example:
        preprocessor = WeaviatePreprocessor(
            encoder=encoder,
            class_context={
                "Article": ["news", "journalism", "current events"],
                "Product": ["e-commerce", "catalog", "retail"]
            }
        )
        
        # Prepare object for insertion
        obj = preprocessor.prepare_object(
            text="Breaking news about technology",
            class_name="Article",
            properties={"title": "Tech News", "category": "Technology"}
        )
    """
    
    def __init__(
        self,
        encoder: BaseEncoder,
        alpha: float = 0.7,
        strategy: Union[str, BlendStrategy] = 'linear',
        default_context: Optional[List[str]] = None,
        class_context: Optional[Dict[str, List[str]]] = None,
        **strategy_kwargs
    ):
        super().__init__(
            encoder=encoder,
            alpha=alpha,
            strategy=strategy,
            default_context=default_context,
            collection_context=class_context,
            **strategy_kwargs
        )
    
    def prepare_documents(
        self,
        texts: List[str],
        ids: Optional[List[str]] = None,
        metadatas: Optional[List[Dict[str, Any]]] = None,
        collection_name: Optional[str] = None,
        context: Optional[List[str]] = None
    ) -> List[VectorRecord]:
        """Prepare documents as VectorRecord objects."""
        if ids is None:
            import uuid
            ids = [str(uuid.uuid4()) for _ in texts]
        
        if metadatas is None:
            metadatas = [{} for _ in texts]
        
        embeddings = self.embed_texts(texts, context, collection_name)
        
        return [
            VectorRecord(
                id=ids[i],
                embedding=embeddings[i].tolist(),
                metadata=metadatas[i],
                text=texts[i]
            )
            for i in range(len(texts))
        ]
    
    def prepare_query(
        self,
        query: str,
        collection_name: Optional[str] = None,
        context: Optional[List[str]] = None
    ) -> List[float]:
        """Prepare a query embedding."""
        emb = self.embed_text(query, context, collection_name)
        return emb.tolist()
    
    def prepare_object(
        self,
        text: str,
        class_name: str,
        properties: Dict[str, Any],
        uuid: Optional[str] = None,
        context: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Prepare a single object for Weaviate insertion.
        
        Args:
            text: Text content for embedding
            class_name: Weaviate class name
            properties: Object properties
            uuid: Optional UUID (auto-generated if not provided)
            context: Explicit context
        
        Returns:
            Dict ready for Weaviate insertion
        """
        import uuid as uuid_lib
        
        emb = self.embed_text(text, context, class_name)
        
        return {
            "class": class_name,
            "id": uuid or str(uuid_lib.uuid4()),
            "properties": properties,
            "vector": emb.tolist()
        }
    
    def batch_prepare_objects(
        self,
        texts: List[str],
        class_name: str,
        properties_list: List[Dict[str, Any]],
        uuids: Optional[List[str]] = None,
        context: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Prepare multiple objects for batch insertion.
        
        Args:
            texts: Text contents
            class_name: Weaviate class name
            properties_list: List of property dicts
            uuids: Optional UUIDs
            context: Explicit context
        
        Returns:
            List of dicts ready for batch insertion
        """
        import uuid as uuid_lib
        
        if uuids is None:
            uuids = [str(uuid_lib.uuid4()) for _ in texts]
        
        embeddings = self.embed_texts(texts, context, class_name)
        
        return [
            {
                "class": class_name,
                "id": uuids[i],
                "properties": properties_list[i],
                "vector": embeddings[i].tolist()
            }
            for i in range(len(texts))
        ]
