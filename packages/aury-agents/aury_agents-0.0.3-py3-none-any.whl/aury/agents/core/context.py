"""Invocation context for agent execution.

InvocationContext is a runtime object that provides access to
the current execution context. It is NOT persisted - it is built
from the persisted Invocation when execution starts.

All services (llm, tools, middleware, etc.) are accessed through
this context, enabling unified agent construction.
"""
from __future__ import annotations

import asyncio
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING, AsyncIterator

from .logging import context_logger as logger
from .types.session import generate_id

# ContextVar for emit queue - shared across entire async call chain
_emit_queue_var: ContextVar[asyncio.Queue] = ContextVar('emit_queue')

# ContextVar for current parent_id - used by middleware to group blocks
# Stores tuple of (parent_id, apply_to_kinds) where apply_to_kinds is None (all) or set of kinds
_current_parent_id: ContextVar[tuple[str | None, set[str] | None]] = ContextVar(
    'current_parent_id', default=(None, None)
)


def set_parent_id(
    parent_id: str,
    apply_to_kinds: set[str] | None = None,
) -> object:
    """Set current parent_id for block grouping.
    
    Args:
        parent_id: The parent block ID to set
        apply_to_kinds: If provided, only blocks with these kinds will inherit
                       the parent_id. If None, all blocks inherit it.
    
    Returns:
        Token for reset. Use with middleware on_request/on_response.
    
    Example:
        # All blocks inherit parent_id
        token = set_parent_id("blk_xxx")
        
        # Only thinking and text blocks inherit parent_id
        token = set_parent_id("blk_xxx", apply_to_kinds={"thinking", "text"})
        
        # ... emit blocks
        reset_parent_id(token)
    """
    return _current_parent_id.set((parent_id, apply_to_kinds))


def reset_parent_id(token: object) -> None:
    """Reset parent_id to previous value using token from set_parent_id."""
    _current_parent_id.reset(token)


def get_parent_id() -> str | None:
    """Get current parent_id (for debugging/inspection)."""
    parent_id, _ = _current_parent_id.get()
    return parent_id


def resolve_parent_id(kind: str) -> str | None:
    """Resolve parent_id for a given block kind.
    
    Checks if the kind matches the apply_to_kinds filter.
    
    Args:
        kind: The block kind (e.g., "thinking", "text", "tool_use")
        
    Returns:
        parent_id if kind matches filter, None otherwise
    """
    parent_id, apply_to_kinds = _current_parent_id.get()
    if parent_id is None:
        return None
    if apply_to_kinds is None:
        return parent_id  # No filter, apply to all
    if kind in apply_to_kinds:
        return parent_id
    return None


async def emit(event: "BlockEvent | ActionEvent") -> None:
    """Global emit function - emits to current run's queue via ContextVar.
    
    Use this when you don't have access to InvocationContext,
    e.g., in tool execute() methods.
    
    For BlockEvent: automatically fills parent_id from ContextVar if not set.
    ActionEvent does not have parent_id.
    
    Args:
        event: BlockEvent or ActionEvent to emit
    """
    try:
        # Auto-fill parent_id from ContextVar if not explicitly set (BlockEvent only)
        if hasattr(event, 'parent_id') and event.parent_id is None:
            from .types.block import BlockKind
            kind = event.kind.value if isinstance(event.kind, BlockKind) else event.kind
            event.parent_id = resolve_parent_id(kind)
        
        queue = _emit_queue_var.get()
        await queue.put(event)
        # Yield control to event loop to allow consumer to process the queue
        # This ensures streaming output is truly streaming, not buffered
        await asyncio.sleep(0)
    except LookupError:
        # Log warning if called outside of agent.run() context
        pass

if TYPE_CHECKING:
    from .types.session import Session, Invocation
    from .types.message import Message
    from .types.block import BlockEvent
    from .types.action import ActionEvent
    from .bus import Bus, Events
    from ..backends.state import StateBackend
    from ..backends.snapshot import SnapshotBackend
    from ..llm import LLMProvider
    from ..tool import ToolSet, BaseTool, ToolResult
    from ..middleware import MiddlewareChain, HookAction
    from ..memory import MemoryManager
    from ..usage import UsageTracker
    from .state import State


@dataclass
class InvocationContext:
    """Runtime context for an invocation.
    
    This is the central object passed to all agents, providing access to:
    - Core services: storage, bus, snapshot
    - AI services: llm, tools
    - Plugins: middleware
    - Memory: memory manager
    - Session info: session, invocation IDs
    
    All agents (ReactAgent, WorkflowAgent) use the same constructor:
        def __init__(self, ctx: InvocationContext, config: AgentConfig | None = None)
    
    Attributes:
        session: Current session object
        invocation_id: Current invocation ID
        agent_id: Current executing agent ID
        storage: State backend for persistence
        bus: Event bus for pub/sub
        llm: LLM provider for AI calls
        tools: Tool registry
        middleware: Middleware chain
        memory: Memory manager (optional)
        snapshot: Snapshot backend for file tracking (optional)
        parent_invocation_id: Parent invocation (for SubAgent)
        mode: ROOT or DELEGATED
        step: Current step number (mutable)
        abort_self: Event to abort only this invocation
        abort_chain: Event to abort entire invocation chain (shared)
        config: Configuration options
        metadata: Additional context data
    """
    # Core identifiers
    session: "Session"
    invocation_id: str
    agent_id: str
    
    # Core services (required)
    storage: "StateBackend"
    bus: "Bus"
    
    # AI services (required for ReactAgent, optional for WorkflowAgent)
    llm: "LLMProvider | None" = None
    tools: "ToolSet | None" = None
    
    # Plugin services
    middleware: "MiddlewareChain | None" = None
    
    # Memory
    memory: "MemoryManager | None" = None
    
    # Usage tracking
    usage: "UsageTracker | None" = None
    
    # Optional services
    snapshot: "SnapshotBackend | None" = None
    
    # State management (with checkpoint support)
    state: "State | None" = None
    
    # Current run input (set by agent.run(), accessible by Managers)
    input: Any = None  # PromptInput
    
    # Current step's context (set before each LLM call, contains merged Manager outputs)
    agent_context: Any = None  # AgentContext
    
    # Hierarchy
    parent_invocation_id: str | None = None
    mode: str = "root"  # root or delegated
    step: int = 0
    
    # Abort signals
    abort_self: asyncio.Event = field(default_factory=asyncio.Event)
    abort_chain: asyncio.Event = field(default_factory=asyncio.Event)
    
    # Config
    config: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    
    # Depth tracking (for max depth enforcement)
    _depth: int = 0
    
    @property
    def session_id(self) -> str:
        """Get session ID (convenience property)."""
        return self.session.id
    
    @property
    def depth(self) -> int:
        """Get current invocation depth (0 = root)."""
        return self._depth
    
    @property
    def is_aborted(self) -> bool:
        """Check if this invocation should stop."""
        return self.abort_self.is_set() or self.abort_chain.is_set()
    
    @classmethod
    def from_invocation(
        cls,
        inv: "Invocation",
        session: "Session",
        storage: "StateBackend",
        bus: "Bus",
        llm: "LLMProvider | None" = None,
        tools: "ToolSet | None" = None,
        middleware: "MiddlewareChain | None" = None,
        memory: "MemoryManager | None" = None,
        snapshot: "SnapshotBackend | None" = None,
    ) -> "InvocationContext":
        """Build context from persisted invocation.
        
        Args:
            inv: Persisted invocation
            session: Session object
            storage: State backend
            bus: Event bus
            llm: LLM provider (required for ReactAgent)
            tools: Tool registry (required for ReactAgent)
            middleware: Middleware chain
            memory: Memory manager
            snapshot: Snapshot backend
        """
        return cls(
            session=session,
            invocation_id=inv.id,
            agent_id=inv.agent_id,
            storage=storage,
            bus=bus,
            llm=llm,
            tools=tools,
            middleware=middleware,
            memory=memory,
            snapshot=snapshot,
            parent_invocation_id=inv.parent_invocation_id,
            mode=inv.mode.value if hasattr(inv.mode, 'value') else str(inv.mode),
        )
    
    def create_child(
        self,
        agent_id: str,
        mode: str = "delegated",
        inherit_config: bool = True,
        llm: "LLMProvider | None" = None,
        tools: "ToolSet | None" = None,
        middleware: "MiddlewareChain | None" = None,
    ) -> "InvocationContext":
        """Create child context for sub-agent execution.
        
        Child context inherits services from parent by default.
        LLM, tools, and middleware can be overridden for specialized sub-agents.
        
        Args:
            agent_id: Sub-agent ID
            mode: Execution mode (delegated)
            inherit_config: Whether to copy config
            llm: Override LLM provider (None = inherit from parent)
            tools: Override tool registry (None = inherit from parent)
            middleware: Override middleware (None = inherit from parent)
            
        Returns:
            New InvocationContext for child
            
        Raises:
            MaxDepthExceededError: If max depth exceeded
        """
        max_depth = self.config.get("max_sub_agent_depth", 5)
        if self._depth >= max_depth:
            logger.warning(
                "Max sub-agent depth exceeded",
                extra={"max_depth": max_depth, "agent_id": agent_id}
            )
            raise MaxDepthExceededError(f"Max sub-agent depth {max_depth} exceeded")
        
        logger.debug(
            "Creating child context",
            extra={
                "parent_inv": self.invocation_id,
                "child_agent": agent_id,
                "mode": mode,
                "depth": self._depth + 1,
            }
        )
        
        return InvocationContext(
            session=self.session,
            invocation_id=generate_id("inv"),
            agent_id=agent_id,
            storage=self.storage,
            bus=self.bus,
            llm=llm if llm is not None else self.llm,
            tools=tools if tools is not None else self.tools,
            middleware=middleware if middleware is not None else self.middleware,
            memory=self.memory,
            usage=self.usage,  # Share usage tracker
            snapshot=self.snapshot,
            parent_invocation_id=self.invocation_id,
            mode=mode,
            step=0,
            abort_self=asyncio.Event(),  # Child has own abort_self
            abort_chain=self.abort_chain,  # Shared abort_chain
            config=self.config.copy() if inherit_config else {},
            metadata={},
            _depth=self._depth + 1,
        )
    
    def with_step(self, step: int) -> "InvocationContext":
        """Create new context with updated step."""
        return InvocationContext(
            session=self.session,
            invocation_id=self.invocation_id,
            agent_id=self.agent_id,
            storage=self.storage,
            bus=self.bus,
            llm=self.llm,
            tools=self.tools,
            middleware=self.middleware,
            memory=self.memory,
            snapshot=self.snapshot,
            parent_invocation_id=self.parent_invocation_id,
            mode=self.mode,
            step=step,
            abort_self=self.abort_self,
            abort_chain=self.abort_chain,
            config=self.config,
            metadata=self.metadata.copy(),
            _depth=self._depth,
        )
    
    # ========== Core Helper Methods ==========
    
    async def emit(self, block: "BlockEvent") -> None:
        """Emit a block event to the current run's queue.
        
        This is the unified way to send streaming output from anywhere:
        - ReactAgent LLM responses
        - WorkflowAgent node outputs
        - Tool outputs
        - BlockHandle operations
        
        The block's session_id, invocation_id, and parent_id are automatically filled.
        Uses ContextVar to find the queue set by BaseAgent.run().
        Parent_id respects the apply_to_kinds filter set via set_parent_id().
        
        Args:
            block: BlockEvent to emit
        """
        # Fill in IDs if not set
        if not block.session_id:
            block.session_id = self.session_id
        if not block.invocation_id:
            block.invocation_id = self.invocation_id
        # Auto-fill parent_id from ContextVar if not explicitly set
        # Uses resolve_parent_id to respect apply_to_kinds filter
        if block.parent_id is None:
            from .types.block import BlockKind
            kind = block.kind.value if isinstance(block.kind, BlockKind) else block.kind
            block.parent_id = resolve_parent_id(kind)
        
        # Put into the current run's queue (via ContextVar)
        try:
            queue = _emit_queue_var.get()
            await queue.put(block)
            # Yield control to event loop to allow consumer to process the queue
            # This ensures streaming output is truly streaming, not buffered
            await asyncio.sleep(0)
        except LookupError:
            # Fallback: if no queue set, log warning (shouldn't happen in normal use)
            logger.warning("emit() called outside of agent.run() context")
    
    async def call_llm(
        self,
        messages: list["Message"],
        llm: "LLMProvider | None" = None,
        stream: bool = False,
        **kwargs: Any,
    ) -> Any | AsyncIterator[Any]:
        """Call LLM with automatic middleware support.
        
        Supports temporarily using a different LLM provider.
        Automatically triggers on_request/on_response middleware hooks.
        
        Args:
            messages: Messages to send to LLM
            llm: Override LLM provider (None = use ctx.llm)
            stream: Whether to stream the response
            **kwargs: Additional LLM parameters
            
        Returns:
            LLM response (or async iterator if streaming)
            
        Raises:
            ValueError: If no LLM available
        """
        provider = llm or self.llm
        if provider is None:
            raise ValueError("No LLM provider available")
        
        # Build request
        request = {
            "messages": messages,
            "stream": stream,
            **kwargs,
        }
        
        # Build context for middleware
        mw_context = {
            "session_id": self.session_id,
            "invocation_id": self.invocation_id,
            "agent_id": self.agent_id,
            "step": self.step,
        }
        
        # Process through middleware (on_request)
        if self.middleware:
            processed = await self.middleware.process_request(request, mw_context)
            if processed is None:
                logger.debug("Request blocked by middleware")
                return None
            request = processed
        
        try:
            # Call LLM
            if stream:
                return self._stream_llm_with_middleware(provider, request, mw_context)
            else:
                response = await provider.generate(
                    messages=request["messages"],
                    **{k: v for k, v in request.items() if k not in ("messages", "stream")}
                )
                
                # Process through middleware (on_response)
                if self.middleware:
                    response_dict = {"response": response}
                    processed = await self.middleware.process_response(response_dict, mw_context)
                    if processed is None:
                        return None
                    response = processed.get("response", response)
                
                return response
                
        except Exception as e:
            if self.middleware:
                processed_error = await self.middleware.process_error(e, mw_context)
                if processed_error is None:
                    return None
                raise processed_error
            raise
    
    async def _stream_llm_with_middleware(
        self,
        provider: "LLMProvider",
        request: dict[str, Any],
        mw_context: dict[str, Any],
    ) -> AsyncIterator[Any]:
        """Stream LLM response with middleware processing."""
        if self.middleware:
            self.middleware.reset_stream_state()
        
        try:
            async for chunk in provider.stream(
                messages=request["messages"],
                **{k: v for k, v in request.items() if k not in ("messages", "stream")}
            ):
                if self.middleware:
                    chunk_dict = {"chunk": chunk}
                    processed = await self.middleware.process_stream_chunk(chunk_dict, mw_context)
                    if processed is None:
                        continue
                    chunk = processed.get("chunk", chunk)
                yield chunk
                
        except Exception as e:
            if self.middleware:
                processed_error = await self.middleware.process_error(e, mw_context)
                if processed_error is None:
                    return
                raise processed_error
            raise
    
    async def execute_tool(
        self,
        tool: "BaseTool",
        arguments: dict[str, Any],
    ) -> "ToolResult":
        """Execute a tool with automatic middleware support.
        
        Allows manual tool execution with custom arguments.
        Automatically triggers on_tool_call/on_tool_end middleware hooks.
        
        Args:
            tool: The tool to execute
            arguments: Tool arguments (manual input)
            
        Returns:
            Tool execution result
        """
        from ..middleware import HookAction
        
        # Build context for middleware
        mw_context = {
            "session_id": self.session_id,
            "invocation_id": self.invocation_id,
            "agent_id": self.agent_id,
            "step": self.step,
        }
        
        current_args = arguments
        
        # Process through middleware (on_tool_call)
        if self.middleware:
            result = await self.middleware.process_tool_call(tool, current_args, mw_context)
            if result.action == HookAction.SKIP:
                logger.debug(f"Tool {tool.name} skipped by middleware")
                from ..tool import ToolResult
                return ToolResult(
                    output=result.message or "Skipped by middleware",
                    is_error=False,
                )
            elif result.action == HookAction.RETRY and result.modified_data:
                current_args = result.modified_data
            elif result.action == HookAction.STOP:
                logger.debug(f"Tool {tool.name} stopped by middleware")
                from ..tool import ToolResult
                return ToolResult(
                    output=result.message or "Stopped by middleware",
                    is_error=True,
                )
        
        # Execute tool
        tool_result = await tool.execute(**current_args)
        
        # Process through middleware (on_tool_end)
        if self.middleware:
            result = await self.middleware.process_tool_end(tool, tool_result, mw_context)
            if result.action == HookAction.RETRY and result.modified_data:
                # Re-execute with modified args
                tool_result = await tool.execute(**result.modified_data)
        
        return tool_result


class MaxDepthExceededError(Exception):
    """Raised when sub-agent nesting exceeds max depth."""
    pass


__all__ = [
    "InvocationContext",
    "MaxDepthExceededError",
    # Parent ID management for block grouping
    "emit",
    "set_parent_id",
    "reset_parent_id",
    "get_parent_id",
    "resolve_parent_id",
]
