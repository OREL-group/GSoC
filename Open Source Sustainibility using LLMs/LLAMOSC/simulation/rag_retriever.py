import logging
from typing import List
from langchain_core.documents import Document

from LLAMOSC.simulation.vector_stores import VectorStoreBackend, FAISSBackend, ChromaBackend

logger = logging.getLogger("LLAMOSC")


class RAGRetriever:
    def __init__(self, backend: str = "faiss", model: str = "llama3", k: int = 3):
        self.k = k
        self.backend = self._create_backend(backend, model)
        logger.info(f"[RAGRetriever] Initialized with backend={backend}, model={model}, k={k}")

    def _create_backend(self, backend_type: str, model: str) -> VectorStoreBackend:
        if backend_type.lower() == "faiss":
            return FAISSBackend(embedding_model=model)
        elif backend_type.lower() == "chroma":
            return ChromaBackend(embedding_model=model)
        else:
            raise ValueError(f"Unknown backend: {backend_type}. Use 'faiss' or 'chroma'")

    def index_documents(self, texts: List[str]):
        if not texts:
            return
        docs = [Document(page_content=t) for t in texts if t.strip()]
        if not docs:
            return
        self.backend.add_documents(docs)

    def retrieve(self, query: str) -> List[str]:
        results = self.backend.similarity_search(query, k=self.k)
        retrieved = [doc.page_content for doc in results]
        logger.info(f"[RAGRetriever] Retrieved {len(retrieved)} documents")
        return retrieved

    def retrieve_as_string(self, query: str) -> str:
        docs = self.retrieve(query)
        if not docs:
            return ""
        return "\n---\n".join(docs)

    def clear(self):
        self.backend.clear()
