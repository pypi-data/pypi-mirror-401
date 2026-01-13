"""Chunk conversations into meaningful pieces for embedding."""

from dataclasses import dataclass

from .parser import Message
from .understanding import MemoryType, extract_understanding


@dataclass
class Chunk:
    """A chunk of conversation for embedding."""

    id: str
    content: str
    session_id: str
    timestamp: str
    metadata: dict


def chunk_by_exchange(messages: list[Message], max_chars: int = 2000) -> list[Chunk]:
    """
    Chunk messages by user-assistant exchanges.

    Groups a user message with its assistant response as a single chunk.
    This preserves the Q&A context which is important for retrieval.
    """
    chunks = []
    current_exchange = []
    current_chars = 0

    for msg in messages:
        msg_len = len(msg.content)

        # If adding this message would exceed limit, flush current exchange
        if current_chars + msg_len > max_chars and current_exchange:
            chunks.append(_create_chunk(current_exchange))
            current_exchange = []
            current_chars = 0

        current_exchange.append(msg)
        current_chars += msg_len

        # If we have a complete exchange (user + assistant), consider flushing
        if msg.role == "assistant" and len(current_exchange) >= 2:
            # Check if next message would start a new exchange
            chunks.append(_create_chunk(current_exchange))
            current_exchange = []
            current_chars = 0

    # Don't forget the last chunk
    if current_exchange:
        chunks.append(_create_chunk(current_exchange))

    return chunks


def chunk_by_topic(messages: list[Message], max_chars: int = 3000) -> list[Chunk]:
    """
    Chunk messages by topic/context switches.

    Uses simple heuristics to detect topic changes:
    - Long gaps in timestamps
    - Explicit topic markers
    - Tool usage patterns
    """
    chunks = []
    current_topic = []
    current_chars = 0

    for i, msg in enumerate(messages):
        msg_len = len(msg.content)

        # Start new chunk if this would be too big
        if current_chars + msg_len > max_chars and current_topic:
            chunks.append(_create_chunk(current_topic))
            current_topic = []
            current_chars = 0

        current_topic.append(msg)
        current_chars += msg_len

    if current_topic:
        chunks.append(_create_chunk(current_topic))

    return chunks


def _create_chunk(messages: list[Message]) -> Chunk:
    """Create a Chunk from a list of messages with understanding extraction."""
    content_parts = []
    for msg in messages:
        prefix = "User: " if msg.role == "user" else "Assistant: "
        content_parts.append(f"{prefix}{msg.content}")

    first_msg = messages[0]
    last_msg = messages[-1]
    content = "\n\n".join(content_parts)

    # Extract understanding from the combined content
    understanding = extract_understanding(content)

    # Build rich metadata
    metadata = {
        "start_uuid": first_msg.uuid,
        "end_uuid": last_msg.uuid,
        "message_count": len(messages),
        "has_tool_use": any(m.is_tool_use for m in messages),
        # Understanding layer additions
        "memory_type": understanding.memory_type.value,
        "intent": understanding.intent.intent.value,
        "intent_confidence": understanding.intent.confidence,
    }

    # Add extracted structured data if present
    if understanding.decisions:
        metadata["decisions"] = "|".join(understanding.decisions[:3])
    if understanding.blockers:
        metadata["blockers"] = "|".join(understanding.blockers[:3])
    if understanding.entities:
        metadata["entities"] = "|".join(understanding.entities[:5])
    if understanding.intent.topic:
        metadata["topic"] = understanding.intent.topic
    if understanding.intent.keywords:
        metadata["keywords"] = "|".join(understanding.intent.keywords[:5])

    return Chunk(
        id=f"{first_msg.session_id}:{first_msg.uuid}",
        content=content,
        session_id=first_msg.session_id,
        timestamp=first_msg.timestamp,
        metadata=metadata,
    )
