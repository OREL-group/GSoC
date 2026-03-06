from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from LLAMOSC.utils import log_and_print
from LLAMOSC.simulation.rag_retriever import RAGRetriever

import logging
logger = logging.getLogger("LLAMOSC")


@dataclass
class Message:
    sender: str
    content: str
    timestamp: str = field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )


class ConversationSpace:
    """
    Simulates a Slack-like conversation space for contributors and maintainers.
    Analogous to how the simulation currently handles GitHub discussions,
    ConversationSpace provides a structured channel for team communication
    around issues. Supports RAG-based retrieval for relevant message history.
    """

    def __init__(self, channel_name: str, use_rag: bool = True):
        self.channel_name = channel_name
        self.messages: List[Message] = []
        self.use_rag = use_rag
        self.rag = RAGRetriever() if use_rag else None

    def post_message(self, sender: str, content: str):
        """Post a message to the conversation space."""
        message = Message(sender=sender, content=content)
        self.messages.append(message)
        log_and_print(
            f"[#{self.channel_name}] {message.timestamp} | {sender}: {content}"
        )
        # Re-index RAG on every new message
        if self.use_rag and self.rag:
            self._reindex_rag(message)

    def _reindex_rag(self, message: Message):
        """Index a new message into the RAG vectorstore."""
        text = f"{message.timestamp} | {message.sender}: {message.content}"
        self.rag.index_documents([text])

    def get_history(self) -> List[Message]:
        """Return full message history."""
        return self.messages

    def get_history_as_string(self, query: Optional[str] = None) -> str:
        """
        Return message history as a formatted string for LLM context.
        If RAG is enabled and a query is provided, returns only the
        most relevant messages instead of the full history.
        """
        if self.use_rag and self.rag and query:
            retrieved = self.rag.retrieve_as_string(query)
            if retrieved:
                logger.info(f"[ConversationSpace] RAG retrieved context for query: {query[:50]}")
                return retrieved
            else:
                logger.warning("[ConversationSpace] RAG returned empty, falling back to full history.")

        return "\n".join(
            [f"{m.timestamp} | {m.sender}: {m.content}" for m in self.messages]
        )

    def clear(self):
        """Clear the conversation history and reset RAG index."""
        self.messages = []
        if self.rag:
            self.rag.vectorstore = None
