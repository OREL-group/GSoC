import logging
from typing import List
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

logger = logging.getLogger("LLAMOSC")


class RAGRetriever:
    """
    Retrieval-Augmented Generation (RAG) retriever for LLAMOSC.
    Embeds and indexes text documents using OllamaEmbeddings + FAISS,
    enabling semantic retrieval of relevant context for LLM prompts.
    """

    def __init__(self, model: str = "llama3", k: int = 3):
        """
        Args:
            model: Ollama model to use for embeddings
            k: number of top relevant documents to retrieve
        """
        self.k = k
        self.embeddings = OllamaEmbeddings(model=model)
        self.vectorstore = None
        logger.info(f"[RAGRetriever] Initialized with model={model}, k={k}")

    def index_documents(self, texts: List[str]):
        if not texts:
            return
        docs = [Document(page_content=t) for t in texts if t.strip()]
        if not docs:
            return
        try:
            if self.vectorstore is None:
                self.vectorstore = FAISS.from_documents(docs, self.embeddings)
            else:
                self.vectorstore.add_documents(docs)
            logger.info(f"[RAGRetriever] Indexed {len(docs)} documents.")
        except Exception as e:
            logger.error(f"[RAGRetriever] Failed to index documents: {e}")
            self.vectorstore = None

    def retrieve(self, query: str) -> List[str]:
        """
        Retrieve top-k relevant documents for a given query.
        Args:
            query: search query string
        Returns:
            list of relevant document strings
        """
        if self.vectorstore is None:
            logger.warning("[RAGRetriever] Vectorstore not initialized. Returning empty.")
            return []

        try:
            results = self.vectorstore.similarity_search(query, k=self.k)
            retrieved = [doc.page_content for doc in results]
            logger.info(f"[RAGRetriever] Retrieved {len(retrieved)} documents for query.")
            return retrieved
        except Exception as e:
            logger.error(f"[RAGRetriever] Retrieval failed: {e}")
            return []

    def retrieve_as_string(self, query: str) -> str:
        """
        Retrieve top-k relevant documents and return as a formatted string.
        Args:
            query: search query string
        Returns:
            formatted string of relevant context
        """
        docs = self.retrieve(query)
        if not docs:
            return ""
        return "\n---\n".join(docs)
