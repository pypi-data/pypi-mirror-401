"""MessageManager - unified message operations.

MessageManager is the service layer for message operations:
- Save messages (called by Middleware)
- Get history (called by Provider)
- Truncation strategies
- Namespace isolation
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .types import Message
from .store import MessageStore

if TYPE_CHECKING:
    pass


class MessageManager:
    """Unified message manager.
    
    Handles:
    - Message persistence (save)
    - History retrieval (get)
    - Turn/token limits
    - Namespace isolation for sub-agents
    
    Usage:
        # Create manager
        store = StateBackendMessageStore(backend)
        manager = MessageManager(store, max_turns=50)
        
        # Save (typically called in Middleware)
        await manager.save(session_id, "user", "Hello!")
        
        # Get history (typically called by Provider)
        messages = await manager.get_history(session_id, limit=20)
    """
    
    def __init__(
        self,
        store: MessageStore,
        max_turns: int = 50,
        max_tokens: int | None = None,
    ):
        """Initialize MessageManager.
        
        Args:
            store: Message store for persistence
            max_turns: Maximum conversation turns to keep
            max_tokens: Maximum tokens (for future token-based truncation)
        """
        self.store = store
        self.max_turns = max_turns
        self.max_tokens = max_tokens
    
    async def save(
        self,
        session_id: str,
        role: str,
        content: str | list[dict[str, Any]],
        *,
        invocation_id: str = "",
        tool_call_id: str | None = None,
        namespace: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Message:
        """Save a message.
        
        Args:
            session_id: Session ID
            role: Message role (user/assistant/tool)
            content: Message content
            invocation_id: Current invocation ID
            tool_call_id: Tool call ID (for tool messages)
            namespace: Optional namespace for isolation
            metadata: Additional metadata
            
        Returns:
            The saved Message
        """
        # Build effective session_id with namespace
        effective_session_id = session_id
        if namespace:
            effective_session_id = f"{session_id}:{namespace}"
        
        # Create message
        message = Message(
            role=role,
            content=content,
            invocation_id=invocation_id,
            tool_call_id=tool_call_id,
            metadata=metadata or {},
        )
        
        # Save to store
        await self.store.add(effective_session_id, message)
        
        return message
    
    async def get_history(
        self,
        session_id: str,
        *,
        limit: int | None = None,
        namespace: str | None = None,
    ) -> list[Message]:
        """Get message history.
        
        Args:
            session_id: Session ID
            limit: Maximum messages to return (defaults to max_turns * 2)
            namespace: Optional namespace
            
        Returns:
            List of messages
        """
        # Build effective session_id with namespace
        effective_session_id = session_id
        if namespace:
            effective_session_id = f"{session_id}:{namespace}"
        
        # Determine limit
        if limit is None:
            limit = self.max_turns * 2 if self.max_turns else 0
        
        # Get messages
        if limit:
            messages = await self.store.get_recent(effective_session_id, limit)
        else:
            messages = await self.store.get_all(effective_session_id)
        
        # TODO: Apply token limit if configured
        # if self.max_tokens:
        #     messages = self._truncate_to_token_limit(messages)
        
        return messages
    
    async def get_history_as_dicts(
        self,
        session_id: str,
        *,
        limit: int | None = None,
        namespace: str | None = None,
    ) -> list[dict[str, Any]]:
        """Get message history as LLM-compatible dicts.
        
        Args:
            session_id: Session ID
            limit: Maximum messages to return
            namespace: Optional namespace
            
        Returns:
            List of message dicts for LLM
        """
        messages = await self.get_history(
            session_id,
            limit=limit,
            namespace=namespace,
        )
        return [m.to_llm_format() for m in messages]
    
    async def delete_invocation(
        self,
        session_id: str,
        invocation_id: str,
        *,
        namespace: str | None = None,
    ) -> int:
        """Delete messages from a specific invocation (for revert).
        
        Args:
            session_id: Session ID
            invocation_id: Invocation ID to delete
            namespace: Optional namespace
            
        Returns:
            Number of messages deleted
        """
        effective_session_id = session_id
        if namespace:
            effective_session_id = f"{session_id}:{namespace}"
        
        return await self.store.delete_by_invocation(
            effective_session_id,
            invocation_id,
        )


__all__ = ["MessageManager"]
