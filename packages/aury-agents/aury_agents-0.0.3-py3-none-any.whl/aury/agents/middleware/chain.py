"""Middleware chain for sequential processing."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, TYPE_CHECKING

from ..core.logging import middleware_logger as logger
from .types import TriggerMode, HookAction, HookResult
from .base import Middleware

if TYPE_CHECKING:
    from ..core.types.tool import BaseTool, ToolResult


@dataclass
class MiddlewareEntry:
    """Entry in middleware chain with inherit override."""
    middleware: Middleware
    inherit: bool  # Effective inherit value (config default or overridden)


class MiddlewareChain:
    """Chain of middlewares for sequential processing."""
    
    def __init__(self, middlewares: list[Middleware] | None = None) -> None:
        self._entries: list[MiddlewareEntry] = []
        self._token_buffer: str = ""
        self._token_count: int = 0
        
        # Add initial middlewares if provided
        if middlewares:
            for mw in middlewares:
                self.use(mw)
    
    @property
    def _middlewares(self) -> list[Middleware]:
        """Get middleware list."""
        return [e.middleware for e in self._entries]
    
    def use(
        self,
        middleware: Middleware,
        *,
        inherit: bool | None = None,
    ) -> "MiddlewareChain":
        """Add middleware to chain.
        
        Args:
            middleware: The middleware to add
            inherit: Override inherit setting (None = use middleware's config default)
        
        Maintains sorted order by priority.
        """
        effective_inherit = inherit if inherit is not None else middleware.config.inherit
        entry = MiddlewareEntry(middleware=middleware, inherit=effective_inherit)
        self._entries.append(entry)
        self._entries.sort(key=lambda e: e.middleware.config.priority)
        return self
    
    def remove(self, middleware: Middleware) -> "MiddlewareChain":
        """Remove middleware from chain."""
        self._entries = [e for e in self._entries if e.middleware != middleware]
        return self
    
    def clear(self) -> "MiddlewareChain":
        """Clear all middlewares."""
        self._entries.clear()
        return self
    
    def get_inheritable(self) -> list[MiddlewareEntry]:
        """Get entries that should be inherited by sub-agents."""
        return [e for e in self._entries if e.inherit]
    
    def merge(self, other: "MiddlewareChain | None") -> "MiddlewareChain":
        """Merge this chain's inheritable middlewares with another chain.
        
        Creates a new chain with:
        - This chain's inheritable middlewares
        - All of other chain's middlewares
        
        Args:
            other: Chain to merge with (sub-agent's own middlewares)
            
        Returns:
            New merged MiddlewareChain
        """
        merged = MiddlewareChain()
        
        # Add inheritable from this chain
        for entry in self.get_inheritable():
            merged._entries.append(MiddlewareEntry(
                middleware=entry.middleware,
                inherit=entry.inherit,
            ))
        
        # Add all from other chain
        if other:
            for entry in other._entries:
                # Avoid duplicates (same middleware instance)
                if entry.middleware not in [e.middleware for e in merged._entries]:
                    merged._entries.append(MiddlewareEntry(
                        middleware=entry.middleware,
                        inherit=entry.inherit,
                    ))
        
        # Re-sort by priority
        merged._entries.sort(key=lambda e: e.middleware.config.priority)
        return merged
    
    async def process_request(
        self,
        request: dict[str, Any],
        context: dict[str, Any],
    ) -> dict[str, Any] | None:
        """Process request through all middlewares."""
        current = request
        
        for mw in self._middlewares:
            result = await mw.on_request(current, context)
            if result is None:
                return None
            current = result
        
        return current
    
    async def process_response(
        self,
        response: dict[str, Any],
        context: dict[str, Any],
    ) -> dict[str, Any] | None:
        """Process response through all middlewares (reverse order)."""
        current = response
        
        for mw in reversed(self._middlewares):
            result = await mw.on_response(current, context)
            if result is None:
                return None
            current = result
        
        return current
    
    async def process_error(
        self,
        error: Exception,
        context: dict[str, Any],
    ) -> Exception | None:
        """Process error through all middlewares."""
        current = error
        
        for mw in self._middlewares:
            result = await mw.on_error(current, context)
            if result is None:
                return None
            current = result
        
        return current
    
    async def process_stream_chunk(
        self,
        chunk: dict[str, Any],
        context: dict[str, Any],
    ) -> dict[str, Any] | None:
        """Process streaming chunk through middlewares based on trigger mode."""
        text = chunk.get("text", chunk.get("delta", ""))
        self._token_buffer += text
        self._token_count += 1
        
        current = chunk
        
        for mw in self._middlewares:
            should_trigger = self._should_trigger(mw, text)
            
            if should_trigger:
                result = await mw.on_model_stream(current, context)
                if result is None:
                    return None
                current = result
        
        return current
    
    def _should_trigger(self, middleware: Middleware, text: str) -> bool:
        """Check if middleware should be triggered."""
        mode = middleware.config.trigger_mode
        
        if mode == TriggerMode.EVERY_TOKEN:
            return True
        elif mode == TriggerMode.EVERY_N_TOKENS:
            return self._token_count % middleware.config.trigger_n == 0
        elif mode == TriggerMode.ON_BOUNDARY:
            return self._is_boundary(text)
        
        return True
    
    def _is_boundary(self, text: str) -> bool:
        """Check if text ends with a sentence/paragraph boundary."""
        boundaries = (".", "。", "\n", "!", "?", "！", "？", ";", "；")
        return text.rstrip().endswith(boundaries)
    
    def reset_stream_state(self) -> None:
        """Reset streaming state (call at start of new stream)."""
        self._token_buffer = ""
        self._token_count = 0
    
    @property
    def middlewares(self) -> list[Middleware]:
        """Get list of middlewares (read-only)."""
        return list(self._middlewares)
    
    # ========== Lifecycle Hook Processing ==========
    
    async def process_agent_start(
        self,
        agent_id: str,
        input_data: Any,
        context: dict[str, Any],
    ) -> HookResult:
        """Process agent start through all middlewares.
        
        Returns:
            First non-CONTINUE result, or CONTINUE if all pass
        """
        for mw in self._middlewares:
            if hasattr(mw, 'on_agent_start'):
                result = await mw.on_agent_start(agent_id, input_data, context)
                if result.action != HookAction.CONTINUE:
                    logger.debug(f"Middleware returned {result.action} on agent_start")
                    return result
        return HookResult.proceed()
    
    async def process_agent_end(
        self,
        agent_id: str,
        result: Any,
        context: dict[str, Any],
    ) -> HookResult:
        """Process agent end through all middlewares (reverse order)."""
        for mw in reversed(self._middlewares):
            if hasattr(mw, 'on_agent_end'):
                hook_result = await mw.on_agent_end(agent_id, result, context)
                if hook_result.action != HookAction.CONTINUE:
                    logger.debug(f"Middleware returned {hook_result.action} on agent_end")
                    return hook_result
        return HookResult.proceed()
    
    async def process_tool_call(
        self,
        tool: "BaseTool",
        params: dict[str, Any],
        context: dict[str, Any],
    ) -> HookResult:
        """Process tool call through all middlewares.
        
        Returns:
            SKIP to skip tool, RETRY with modified_data to change params
        """
        for mw in self._middlewares:
            if hasattr(mw, 'on_tool_call'):
                result = await mw.on_tool_call(tool, params, context)
                if result.action != HookAction.CONTINUE:
                    logger.debug(f"Middleware returned {result.action} on tool_call")
                    return result
        return HookResult.proceed()
    
    async def process_tool_end(
        self,
        tool: "BaseTool",
        result: "ToolResult",
        context: dict[str, Any],
    ) -> HookResult:
        """Process tool end through all middlewares (reverse order)."""
        for mw in reversed(self._middlewares):
            if hasattr(mw, 'on_tool_end'):
                hook_result = await mw.on_tool_end(tool, result, context)
                if hook_result.action != HookAction.CONTINUE:
                    logger.debug(f"Middleware returned {hook_result.action} on tool_end")
                    return hook_result
        return HookResult.proceed()
    
    async def process_subagent_start(
        self,
        parent_agent_id: str,
        child_agent_id: str,
        mode: str,
        context: dict[str, Any],
    ) -> HookResult:
        """Process sub-agent start through all middlewares."""
        for mw in self._middlewares:
            if hasattr(mw, 'on_subagent_start'):
                result = await mw.on_subagent_start(
                    parent_agent_id, child_agent_id, mode, context
                )
                if result.action != HookAction.CONTINUE:
                    logger.debug(f"Middleware returned {result.action} on subagent_start")
                    return result
        return HookResult.proceed()
    
    async def process_subagent_end(
        self,
        parent_agent_id: str,
        child_agent_id: str,
        result: Any,
        context: dict[str, Any],
    ) -> HookResult:
        """Process sub-agent end through all middlewares (reverse order)."""
        for mw in reversed(self._middlewares):
            if hasattr(mw, 'on_subagent_end'):
                hook_result = await mw.on_subagent_end(
                    parent_agent_id, child_agent_id, result, context
                )
                if hook_result.action != HookAction.CONTINUE:
                    logger.debug(f"Middleware returned {hook_result.action} on subagent_end")
                    return hook_result
        return HookResult.proceed()
    
    async def process_message_save(
        self,
        message: dict[str, Any],
        context: dict[str, Any],
    ) -> dict[str, Any] | None:
        """Process message save through all middlewares.
        
        Args:
            message: Message to be saved
            context: Execution context
            
        Returns:
            Modified message, or None to skip saving
        """
        current = message
        
        for mw in self._middlewares:
            if hasattr(mw, 'on_message_save'):
                result = await mw.on_message_save(current, context)
                if result is None:
                    logger.debug("Middleware blocked message save")
                    return None
                current = result
        
        return current


__all__ = ["MiddlewareChain"]
