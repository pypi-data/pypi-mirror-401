# neuroembed/integrations/__init__.py
"""
Integration modules for popular frameworks and vector databases.

Available integrations:
- langchain: LangChain Embeddings interface
- llamaindex: LlamaIndex embedding wrapper
- vectordb: Vector database pre-processors (Chroma, Pinecone, Weaviate)
"""

from .langchain import NeuroEmbedLangChain
from .llamaindex import NeuroEmbedLlamaIndex
from .vectordb import (
    ChromaPreprocessor,
    PineconePreprocessor,
    WeaviatePreprocessor,
    VectorDBPreprocessor,
)

__all__ = [
    "NeuroEmbedLangChain",
    "NeuroEmbedLlamaIndex",
    "ChromaPreprocessor",
    "PineconePreprocessor",
    "WeaviatePreprocessor",
    "VectorDBPreprocessor",
]
