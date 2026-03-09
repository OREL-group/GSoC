import logging
from typing import List
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from .base import VectorStoreBackend

logger = logging.getLogger("LLAMOSC")

class FAISSBackend(VectorStoreBackend):
    def __init__(self, embedding_model: str = "llama3"):
        self.embeddings = OllamaEmbeddings(model=embedding_model)
        self.vectorstore = None
    
    def add_documents(self, documents: List[Document]) -> None:
        if not documents:
            return
        if self.vectorstore is None:
            self.vectorstore = FAISS.from_documents(documents, self.embeddings)
        else:
            self.vectorstore.add_documents(documents)
    
    def similarity_search(self, query: str, k: int) -> List[Document]:
        if self.vectorstore is None:
            return []
        return self.vectorstore.similarity_search(query, k=k)
    
    def clear(self) -> None:
        self.vectorstore = None
