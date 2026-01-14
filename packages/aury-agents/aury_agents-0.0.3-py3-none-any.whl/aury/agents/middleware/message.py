"""MessagePersistenceMiddleware - saves messages via on_message_save hook.

This middleware handles message persistence. When the Agent triggers
on_message_save, this middleware saves the message via MessageManager.

Usage:
    manager = MessageManager(store)
    middleware = MessagePersistenceMiddleware(manager)
    
    agent = ReactAgent.create(
        llm=llm,
        middleware=MiddlewareChain([middleware]),
    )
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import BaseMiddleware

if TYPE_CHECKING:
    from ..messages import MessageManager


class MessagePersistenceMiddleware(BaseMiddleware):
    """Middleware that persists messages via MessageManager.
    
    Intercepts on_message_save hook and saves messages to storage.
    """
    
    def __init__(self, manager: "MessageManager"):
        """Initialize with MessageManager.
        
        Args:
            manager: MessageManager for saving messages
        """
        self.manager = manager
    
    async def on_message_save(
        self,
        message: dict[str, Any],
        context: dict[str, Any],
    ) -> dict[str, Any] | None:
        """Save message via MessageManager.
        
        Args:
            message: Message dict with 'role', 'content', etc.
            context: Execution context with 'session_id', 'agent_id'
            
        Returns:
            The message (pass through to other middlewares)
        """
        session_id = context.get("session_id", "")
        namespace = context.get("namespace")
        
        if not session_id:
            return message
        
        # Extract message fields
        role = message.get("role", "")
        content = message.get("content", "")
        invocation_id = message.get("invocation_id", "")
        tool_call_id = message.get("tool_call_id")
        
        # Save via manager
        await self.manager.save(
            session_id=session_id,
            role=role,
            content=content,
            invocation_id=invocation_id,
            tool_call_id=tool_call_id,
            namespace=namespace,
        )
        
        # Pass through to other middlewares
        return message


__all__ = ["MessagePersistenceMiddleware"]
