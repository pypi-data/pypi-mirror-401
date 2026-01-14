"""MessageContextProvider - provides conversation history messages.

This provider ONLY fetches message history for context.
Message saving is handled by Middleware (on_message_save hook).

Recovery Strategy:
- Check State for complete messages (from pending/crashed invocation)
- If found, use State messages (complete, not truncated)
- Otherwise, load from MessageStore (truncated historical messages)
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from .base import BaseContextProvider, AgentContext

if TYPE_CHECKING:
    from ..core.context import InvocationContext
    from ..messages import MessageManager

logger = logging.getLogger(__name__)


class MessageContextProvider(BaseContextProvider):
    """Message history context provider.
    
    Provides conversation history messages for LLM context.
    
    Features:
    - Load messages via MessageManager
    - Priority: State (complete) > MessageStore (truncated)
    - Turn limits handled by MessageManager
    
    Note: Message SAVING is not done here.
    Use MessagePersistenceMiddleware for saving messages.
    """
    
    _name = "messages"
    
    def __init__(self, manager: "MessageManager"):
        """Initialize MessageContextProvider.
        
        Args:
            manager: MessageManager for loading messages
        """
        self.manager = manager
    
    async def fetch(self, ctx: "InvocationContext") -> AgentContext:
        """Fetch conversation history.
        
        Priority:
        1. Check State for complete messages (from pending/crashed inv)
        2. Fall back to MessageStore (truncated historical messages)
        
        Returns:
            AgentContext with messages list
        """
        # Try to get complete messages from State (pending/crashed recovery)
        state_messages = await self._get_messages_from_state(ctx)
        if state_messages:
            logger.debug(
                f"Loaded {len(state_messages)} messages from State (complete)",
                extra={"session_id": ctx.session.id},
            )
            return AgentContext(messages=state_messages)
        
        # Fall back to MessageStore (truncated historical messages)
        messages = await self.manager.get_history_as_dicts(ctx.session.id)
        logger.debug(
            f"Loaded {len(messages)} messages from MessageStore (may be truncated)",
            extra={"session_id": ctx.session.id},
        )
        return AgentContext(messages=messages)
    
    async def _get_messages_from_state(self, ctx: "InvocationContext") -> list[dict[str, Any]] | None:
        """Try to get complete messages from State.
        
        State stores complete (not truncated) messages during execution.
        This allows recovery from:
        - HITL suspend
        - Process crash
        - Abnormal termination
        
        Returns:
            List of message dicts if found, None otherwise
        """
        if not ctx.state:
            return None
        
        # Check if State has message_history
        messages_data = ctx.state.get("agent.message_history")
        if not messages_data:
            return None
        
        if not isinstance(messages_data, list):
            return None
        
        # Validate and convert to expected format
        messages: list[dict[str, Any]] = []
        for msg in messages_data:
            if isinstance(msg, dict) and "role" in msg:
                messages.append(msg)
        
        return messages if messages else None


__all__ = ["MessageContextProvider"]
