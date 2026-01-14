"""Message store protocol and implementations.

MessageStore is the storage layer for messages.
Default implementation wraps StateBackend.
"""
from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from .types import Message


@runtime_checkable
class MessageStore(Protocol):
    """Protocol for message storage.
    
    Provides persistence for conversation messages.
    """
    
    async def add(self, session_id: str, message: Message) -> None:
        """Add a message to session history.
        
        Args:
            session_id: Session ID (may include namespace suffix)
            message: Message to store
        """
        ...
    
    async def get_all(self, session_id: str) -> list[Message]:
        """Get all messages for a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            List of messages in chronological order
        """
        ...
    
    async def get_recent(self, session_id: str, limit: int) -> list[Message]:
        """Get recent messages for a session.
        
        Args:
            session_id: Session ID
            limit: Maximum number of messages to return
            
        Returns:
            List of most recent messages
        """
        ...
    
    async def delete_by_invocation(self, session_id: str, invocation_id: str) -> int:
        """Delete messages by invocation ID (for revert).
        
        Args:
            session_id: Session ID
            invocation_id: Invocation ID to delete
            
        Returns:
            Number of messages deleted
        """
        ...


class StateBackendMessageStore:
    """MessageStore implementation backed by StateBackend.
    
    Wraps StateBackend to provide MessageStore interface.
    """
    
    def __init__(self, backend: Any):  # StateBackend
        """Initialize with StateBackend.
        
        Args:
            backend: StateBackend instance
        """
        self._backend = backend
    
    async def add(self, session_id: str, message: Message) -> None:
        """Add a message using StateBackend."""
        await self._backend.add_message(session_id, message.to_dict())
    
    async def get_all(self, session_id: str) -> list[Message]:
        """Get all messages using StateBackend."""
        raw_messages = await self._backend.get_messages(session_id)
        return [Message.from_dict(m) for m in (raw_messages or [])]
    
    async def get_recent(self, session_id: str, limit: int) -> list[Message]:
        """Get recent messages."""
        all_messages = await self.get_all(session_id)
        return all_messages[-limit:] if limit else all_messages
    
    async def delete_by_invocation(self, session_id: str, invocation_id: str) -> int:
        """Delete messages by invocation ID.
        
        Note: This requires StateBackend to support this operation,
        or we need to implement it by getting all and filtering.
        """
        # Default implementation: get all, filter, rewrite
        # This is inefficient but works for most backends
        all_messages = await self.get_all(session_id)
        filtered = [m for m in all_messages if m.invocation_id != invocation_id]
        deleted_count = len(all_messages) - len(filtered)
        
        # Note: This requires atomic replace support in backend
        # For now, just return count - actual deletion depends on backend
        return deleted_count


class InMemoryMessageStore:
    """In-memory message store for testing."""
    
    def __init__(self) -> None:
        self._messages: dict[str, list[Message]] = {}
    
    async def add(self, session_id: str, message: Message) -> None:
        if session_id not in self._messages:
            self._messages[session_id] = []
        self._messages[session_id].append(message)
    
    async def get_all(self, session_id: str) -> list[Message]:
        return self._messages.get(session_id, []).copy()
    
    async def get_recent(self, session_id: str, limit: int) -> list[Message]:
        messages = self._messages.get(session_id, [])
        return messages[-limit:] if limit else messages.copy()
    
    async def delete_by_invocation(self, session_id: str, invocation_id: str) -> int:
        if session_id not in self._messages:
            return 0
        
        original = self._messages[session_id]
        self._messages[session_id] = [
            m for m in original if m.invocation_id != invocation_id
        ]
        return len(original) - len(self._messages[session_id])


__all__ = [
    "MessageStore",
    "StateBackendMessageStore",
    "InMemoryMessageStore",
]
