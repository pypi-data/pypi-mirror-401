"""State backend types and protocols."""
from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class StateBackend(Protocol):
    """Protocol for framework state storage.
    
    Provides key-value storage with namespace isolation.
    
    Example namespaces:
    - "session" - Session data
    - "invocation" - Invocation records
    - "plan" - Plan state
    - "memory" - Memory/recall data
    """
    
    async def get(self, namespace: str, key: str) -> Any | None:
        """Get value by key."""
        ...
    
    async def set(self, namespace: str, key: str, value: Any) -> None:
        """Set value by key."""
        ...
    
    async def delete(self, namespace: str, key: str) -> bool:
        """Delete value by key. Returns True if deleted."""
        ...
    
    async def list(self, namespace: str, prefix: str = "") -> list[str]:
        """List keys with optional prefix filter."""
        ...
    
    async def exists(self, namespace: str, key: str) -> bool:
        """Check if key exists."""
        ...
    
    # Message methods for MessageManager
    async def add_message(self, session_id: str, message: dict[str, Any]) -> None:
        """Add a message to session history.
        
        Args:
            session_id: Session ID (may include namespace suffix like "sess_xxx:agent:call_id")
            message: Message dict with role, content, invocation_id
        """
        ...
    
    async def get_messages(self, session_id: str) -> list[dict[str, Any]]:
        """Get all messages for a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            List of message dicts
        """
        ...


__all__ = ["StateBackend"]
