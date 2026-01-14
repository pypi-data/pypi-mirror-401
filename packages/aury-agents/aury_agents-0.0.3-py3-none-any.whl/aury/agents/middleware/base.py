"""Middleware protocol and base implementation."""
from __future__ import annotations

from typing import Any, Protocol, runtime_checkable, TYPE_CHECKING

from .types import HookResult, MiddlewareConfig

if TYPE_CHECKING:
    from ..core.types.tool import BaseTool, ToolResult


@runtime_checkable
class Middleware(Protocol):
    """Middleware protocol for request/response processing.
    
    Includes both LLM request/response hooks and agent lifecycle hooks.
    """
    
    @property
    def config(self) -> MiddlewareConfig:
        """Get middleware configuration."""
        ...
    
    # ========== LLM Request/Response Hooks ==========
    
    async def on_request(
        self,
        request: dict[str, Any],
        context: dict[str, Any],
    ) -> dict[str, Any] | None:
        """Process request before LLM call.
        
        Args:
            request: The request to process
            context: Execution context
            
        Returns:
            Modified request, or None to skip further processing
        """
        ...
    
    async def on_response(
        self,
        response: dict[str, Any],
        context: dict[str, Any],
    ) -> dict[str, Any] | None:
        """Process response after LLM call.
        
        Args:
            response: The response to process
            context: Execution context
            
        Returns:
            Modified response, or None to skip further processing
        """
        ...
    
    async def on_error(
        self,
        error: Exception,
        context: dict[str, Any],
    ) -> Exception | None:
        """Handle errors.
        
        Args:
            error: The exception that occurred
            context: Execution context
            
        Returns:
            Modified exception, or None to suppress
        """
        ...
    
    async def on_model_stream(
        self,
        chunk: dict[str, Any],
        context: dict[str, Any],
    ) -> dict[str, Any] | None:
        """Process streaming chunk (triggered by trigger_mode).
        
        Args:
            chunk: The streaming chunk
            context: Execution context
            
        Returns:
            Modified chunk, or None to skip further processing
        """
        ...
    
    # ========== Agent Lifecycle Hooks ==========
    
    async def on_agent_start(
        self,
        agent_id: str,
        input_data: Any,
        context: dict[str, Any],
    ) -> HookResult:
        """Called when agent starts processing.
        
        Args:
            agent_id: The agent identifier
            input_data: Input to the agent
            context: Execution context
            
        Returns:
            HookResult controlling execution flow
        """
        ...
    
    async def on_agent_end(
        self,
        agent_id: str,
        result: Any,
        context: dict[str, Any],
    ) -> HookResult:
        """Called when agent completes processing.
        
        Args:
            agent_id: The agent identifier
            result: Agent's result
            context: Execution context
            
        Returns:
            HookResult (only CONTINUE/STOP meaningful here)
        """
        ...
    
    async def on_tool_call(
        self,
        tool: "BaseTool",
        params: dict[str, Any],
        context: dict[str, Any],
    ) -> HookResult:
        """Called before tool execution.
        
        Args:
            tool: The tool to be called
            params: Tool parameters
            context: Execution context
            
        Returns:
            HookResult - SKIP to skip tool, RETRY to modify params
        """
        ...
    
    async def on_tool_end(
        self,
        tool: "BaseTool",
        result: "ToolResult",
        context: dict[str, Any],
    ) -> HookResult:
        """Called after tool execution.
        
        Args:
            tool: The tool that was called
            result: Tool execution result
            context: Execution context
            
        Returns:
            HookResult - RETRY to re-execute tool
        """
        ...
    
    async def on_subagent_start(
        self,
        parent_agent_id: str,
        child_agent_id: str,
        mode: str,  # "embedded" or "delegated"
        context: dict[str, Any],
    ) -> HookResult:
        """Called when delegating to a sub-agent.
        
        Args:
            parent_agent_id: Parent agent identifier
            child_agent_id: Child agent identifier
            mode: Delegation mode
            context: Execution context
            
        Returns:
            HookResult - SKIP to skip delegation
        """
        ...
    
    async def on_subagent_end(
        self,
        parent_agent_id: str,
        child_agent_id: str,
        result: Any,
        context: dict[str, Any],
    ) -> HookResult:
        """Called when sub-agent completes.
        
        Args:
            parent_agent_id: Parent agent identifier
            child_agent_id: Child agent identifier
            result: Sub-agent's result
            context: Execution context
            
        Returns:
            HookResult (for post-processing)
        """
        ...
    
    async def on_message_save(
        self,
        message: dict[str, Any],
        context: dict[str, Any],
    ) -> dict[str, Any] | None:
        """Called before saving a message to history.
        
        Allows middlewares to transform, filter, or block messages
        before they are persisted.
        
        Args:
            message: Message dict with 'role', 'content', etc.
            context: Execution context
            
        Returns:
            Modified message, or None to skip saving
        """
        ...


class BaseMiddleware:
    """Base middleware implementation with sensible defaults.
    
    Subclass and override specific hooks as needed.
    All hooks have sensible pass-through defaults.
    """
    
    _config: MiddlewareConfig = MiddlewareConfig()
    
    @property
    def config(self) -> MiddlewareConfig:
        return self._config
    
    # ========== LLM Request/Response Hooks ==========
    
    async def on_request(
        self,
        request: dict[str, Any],
        context: dict[str, Any],
    ) -> dict[str, Any] | None:
        """Default: pass through."""
        return request
    
    async def on_response(
        self,
        response: dict[str, Any],
        context: dict[str, Any],
    ) -> dict[str, Any] | None:
        """Default: pass through."""
        return response
    
    async def on_error(
        self,
        error: Exception,
        context: dict[str, Any],
    ) -> Exception | None:
        """Default: re-raise error."""
        return error
    
    async def on_model_stream(
        self,
        chunk: dict[str, Any],
        context: dict[str, Any],
    ) -> dict[str, Any] | None:
        """Default: pass through."""
        return chunk
    
    # ========== Agent Lifecycle Hooks ==========
    
    async def on_agent_start(
        self,
        agent_id: str,
        input_data: Any,
        context: dict[str, Any],
    ) -> HookResult:
        """Default: continue."""
        return HookResult.proceed()
    
    async def on_agent_end(
        self,
        agent_id: str,
        result: Any,
        context: dict[str, Any],
    ) -> HookResult:
        """Default: continue."""
        return HookResult.proceed()
    
    async def on_tool_call(
        self,
        tool: "BaseTool",
        params: dict[str, Any],
        context: dict[str, Any],
    ) -> HookResult:
        """Default: continue."""
        return HookResult.proceed()
    
    async def on_tool_end(
        self,
        tool: "BaseTool",
        result: "ToolResult",
        context: dict[str, Any],
    ) -> HookResult:
        """Default: continue."""
        return HookResult.proceed()
    
    async def on_subagent_start(
        self,
        parent_agent_id: str,
        child_agent_id: str,
        mode: str,
        context: dict[str, Any],
    ) -> HookResult:
        """Default: continue."""
        return HookResult.proceed()
    
    async def on_subagent_end(
        self,
        parent_agent_id: str,
        child_agent_id: str,
        result: Any,
        context: dict[str, Any],
    ) -> HookResult:
        """Default: continue."""
        return HookResult.proceed()
    
    async def on_message_save(
        self,
        message: dict[str, Any],
        context: dict[str, Any],
    ) -> dict[str, Any] | None:
        """Default: pass through."""
        return message


__all__ = [
    "Middleware",
    "BaseMiddleware",
]
