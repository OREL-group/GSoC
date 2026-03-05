from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from LLAMOSC.utils import log_and_print


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
    around issues.
    """

    def __init__(self, channel_name: str):
        self.channel_name = channel_name
        self.messages: List[Message] = []

    def post_message(self, sender: str, content: str):
        """Post a message to the conversation space."""
        message = Message(sender=sender, content=content)
        self.messages.append(message)
        log_and_print(
            f"[#{self.channel_name}] {message.timestamp} | {sender}: {content}"
        )

    def get_history(self) -> List[Message]:
        """Return full message history."""
        return self.messages

    def get_history_as_string(self) -> str:
        """Return message history as a formatted string for LLM context."""
        return "\n".join(
            [f"{m.timestamp} | {m.sender}: {m.content}" for m in self.messages]
        )

    def clear(self):
        """Clear the conversation history."""
        self.messages = []
