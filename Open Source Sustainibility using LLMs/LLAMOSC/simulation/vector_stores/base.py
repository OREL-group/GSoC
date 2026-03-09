from abc import ABC, abstractmethod
from typing import List
from langchain_core.documents import Document

class VectorStoreBackend(ABC):
    @abstractmethod
    def add_documents(self, documents: List[Document]) -> None:
        pass
    
    @abstractmethod
    def similarity_search(self, query: str, k: int) -> List[Document]:
        pass
    
    @abstractmethod
    def clear(self) -> None:
        pass
