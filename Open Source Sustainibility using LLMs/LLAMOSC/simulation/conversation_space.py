from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional
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
    channel: str = "#general"
    event_type: str = "manual"  # "blocked", "merged", "idle", "manual"



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
    def post_message(self, sender: str, content: str, channel: str = "#general", event_type: str = "manual"):
        """Post a message to the conversation space."""
        message = Message(sender=sender, content=content, channel=channel, event_type=event_type)
        self.messages.append(message)
        log_and_print(f"[{channel}] {message.timestamp} | {sender}: {content}")

    def notify_blocked(self, agent_name: str, issue_title: str):
        """Agent posts to #help when blocked on an issue."""
        content = (
            f"Hey team, I'm blocked on issue: '{issue_title}'. "
            f"Has anyone worked on something similar? Any pointers appreciated!"
        )
        self.post_message(sender=agent_name, content=content, channel="#help", event_type="blocked")

    def notify_pr_merged(self, agent_name: str, issue_title: str):
        """Agent posts to #general when their PR is merged."""
        content = (
            f"Just got my PR merged for issue: '{issue_title}' 🎉 "
            f"Thanks for the reviews everyone!"
        )
        self.post_message(sender=agent_name, content=content, channel="#general", event_type="merged")

    def notify_idle(self, agent_name: str, idle_turns: int):
        """Agent posts to #random when idle for more than 2 turns."""
        content = (
            f"I've been idle for {idle_turns} turns. "
            f"Looking for a new issue to work on — any suggestions?"
        )
        self.post_message(sender=agent_name, content=content, channel="#random", event_type="idle")

    def get_messages_by_channel(self, channel: str) -> List[Message]:
        """Filter messages by channel name."""
        return [m for m in self.messages if m.channel == channel]

    def get_messages_by_event(self, event_type: str) -> List[Message]:
        """Filter messages by event type."""
        return [m for m in self.messages if m.event_type == event_type]

    def get_history(self) -> List[Message]:
        """Return full message history."""
        return self.messages

    def get_history_as_string(self, query: Optional[str] = None) -> str:
        if self.use_rag and self.rag and query and self.messages:
            self.rag.vectorstore = None
            texts = [f"{m.timestamp} | {m.sender}: {m.content}" for m in self.messages]
            self.rag.index_documents(texts)
            retrieved = self.rag.retrieve_as_string(query)
            if retrieved:
                return retrieved
        return "\n".join([f"{m.timestamp} | {m.sender}: {m.content}" for m in self.messages])

    def get_engagement_metrics(self) -> Dict:
        """Returns basic engagement metrics for the conversation space."""
        if not self.messages:
            return {
                "total_messages": 0,
                "unique_participants": 0,
                "messages_per_sender": {},
                "most_active_sender": None,
                "first_message_time": None,
                "last_message_time": None,
                "conversation_duration_seconds": 0,
            }
        messages_per_sender = {}
        for message in self.messages:
            messages_per_sender[message.sender] = messages_per_sender.get(message.sender, 0) + 1
        most_active_sender = max(messages_per_sender, key=messages_per_sender.get)
        first_time = datetime.strptime(self.messages[0].timestamp, "%Y-%m-%d %H:%M:%S")
        last_time = datetime.strptime(self.messages[-1].timestamp, "%Y-%m-%d %H:%M:%S")
        duration = (last_time - first_time).seconds
        return {
            "total_messages": len(self.messages),
            "unique_participants": len(messages_per_sender),
            "messages_per_sender": messages_per_sender,
            "most_active_sender": most_active_sender,
            "first_message_time": self.messages[0].timestamp,
            "last_message_time": self.messages[-1].timestamp,
            "conversation_duration_seconds": duration,
        }

    def clear(self):
        """Clear the conversation history and reset RAG index."""
        self.messages = []
        if self.rag:
            self.rag.vectorstore = None

