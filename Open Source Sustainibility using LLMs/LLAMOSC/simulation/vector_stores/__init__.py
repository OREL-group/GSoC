"""
Vector store backends for RAG retriever.
Provides pluggable storage options for embeddings.
"""

from .base import VectorStoreBackend
from .faiss_backend import FAISSBackend
from .chroma_backend import ChromaBackend

__all__ = [
    'VectorStoreBackend',
    'FAISSBackend', 
    'ChromaBackend',
]