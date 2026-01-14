"""ReactAgent - Autonomous agent with think-act-observe loop.

ReactAgent uses the unified BaseAgent constructor:
    __init__(self, ctx: InvocationContext, config: AgentConfig | None = None)

All services (llm, tools, storage, etc.) are accessed through ctx.
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import asdict
from datetime import datetime
from typing import Any, AsyncIterator, ClassVar, Literal, TYPE_CHECKING

from ..core.base import AgentConfig, BaseAgent, ToolInjectionMode
from ..core.context import InvocationContext
from ..core.logging import react_logger as logger
from ..core.bus import Events
from ..context_providers import ContextProvider, AgentContext
from ..core.types.block import BlockEvent, BlockKind, BlockOp
from ..llm import LLMMessage, ToolDefinition
from ..middleware import HookAction
from ..core.types import (
    Invocation,
    InvocationState,
    PromptInput,
    ToolContext,
    ToolResult,
    ToolInvocation,
    ToolInvocationState,
    generate_id,
)
from ..core.state import State
from ..hitl.exceptions import HITLSuspendError

if TYPE_CHECKING:
    from ..llm import LLMProvider
    from ..tool import ToolSet
    from ..core.types.tool import BaseTool
    from ..core.types.session import Session
    from ..backends.state import StateBackend
    from ..backends.snapshot import SnapshotBackend
    from ..backends.subagent import AgentConfig as SubAgentConfig
    from ..core.bus import Bus
    from ..middleware import MiddlewareChain, Middleware
    from ..memory import MemoryManager


class SessionNotFoundError(Exception):
    """Raised when session is not found in storage."""
    pass


class ReactAgent(BaseAgent):
    """ReAct Agent - Autonomous agent with tool calling loop.

    Implements the think-act-observe pattern:
    1. Think: LLM generates reasoning and decides on actions
    2. Act: Execute tool calls
    3. Observe: Process tool results
    4. Repeat until done or max steps reached

    Two ways to create:
    
    1. Simple (recommended for most cases):
        agent = ReactAgent.create(llm=llm, tools=tools, config=config)
    
    2. Advanced (for custom Session/Storage/Bus):
        ctx = InvocationContext(session=session, storage=storage, bus=bus, llm=llm, tools=tools)
        agent = ReactAgent(ctx, config)
    """

    # Class-level config
    agent_type: ClassVar[Literal["react", "workflow"]] = "react"
    
    @classmethod
    def create(
        cls,
        llm: "LLMProvider",
        tools: "ToolSet | list[BaseTool] | None" = None,
        config: AgentConfig | None = None,
        *,
        session: "Session | None" = None,
        storage: "StateBackend | None" = None,
        bus: "Bus | None" = None,
        middlewares: "list[Middleware] | None" = None,
        subagents: "list[SubAgentConfig] | None" = None,
        memory: "MemoryManager | None" = None,
        snapshot: "SnapshotBackend | None" = None,
        # ContextProvider system
        context_providers: "list[ContextProvider] | None" = None,
        enable_history: bool = True,
        history_limit: int = 50,
        # Tool customization
        delegate_tool_class: "type[BaseTool] | None" = None,
    ) -> "ReactAgent":
        """Create ReactAgent with minimal boilerplate.
        
        This is the recommended way to create a ReactAgent for simple use cases.
        Session, Storage, and Bus are auto-created if not provided.
        
        Args:
            llm: LLM provider (required)
            tools: Tool registry or list of tools (optional)
            config: Agent configuration (optional)
            session: Session object (auto-created if None)
            storage: State backend (auto-created as SQLiteStateBackend if None)
            bus: Event bus (auto-created if None)
            middlewares: List of middlewares (auto-creates chain)
            subagents: List of sub-agent configs (auto-creates SubAgentManager)
            memory: Memory manager (optional)
            snapshot: Snapshot backend (optional)
            context_providers: Additional custom context providers (optional)
            enable_history: Enable message history (default True)
            history_limit: Max conversation turns to keep (default 50)
            delegate_tool_class: Custom DelegateTool class (optional)
            
        Returns:
            Configured ReactAgent ready to run
            
        Example:
            # Minimal
            agent = ReactAgent.create(llm=my_llm)
            
            # With tools and middlewares
            agent = ReactAgent.create(
                llm=my_llm,
                tools=[tool1, tool2],
                middlewares=[MessageContainerMiddleware()],
            )
            
            # With sub-agents
            agent = ReactAgent.create(
                llm=my_llm,
                subagents=[
                    AgentConfig(key="researcher", agent=researcher_agent),
                ],
            )
            
            # With custom context providers
            agent = ReactAgent.create(
                llm=my_llm,
                tools=[tool1],
                context_providers=[MyRAGProvider(), MyProjectProvider()],
            )
        """
        from ..core.bus import Bus
        from ..core.types.session import Session, generate_id
        from ..backends import SQLiteStateBackend
        from ..backends.subagent import ListSubAgentBackend
        from ..tool import ToolSet
        from ..tool.builtin import DelegateTool
        from ..middleware import MiddlewareChain, MessagePersistenceMiddleware
        from ..context_providers import MessageContextProvider
        from ..messages import MessageManager, StateBackendMessageStore
        
        # Auto-create missing components
        if session is None:
            session = Session(id=generate_id("sess"))
        if storage is None:
            storage = SQLiteStateBackend()  # Default: local SQLite persistence
        if bus is None:
            bus = Bus()
        
        # Create MessageManager for history
        message_manager: MessageManager | None = None
        if enable_history:
            message_store = StateBackendMessageStore(storage)
            message_manager = MessageManager(message_store, max_turns=history_limit)
        
        # Create middleware chain from list (add MessagePersistenceMiddleware if history enabled)
        middleware_chain: MiddlewareChain | None = None
        if middlewares or message_manager:
            middleware_chain = MiddlewareChain()
            # Add message persistence middleware first
            if message_manager:
                middleware_chain.use(MessagePersistenceMiddleware(message_manager))
            # Add user middlewares
            if middlewares:
                for mw in middlewares:
                    middleware_chain.use(mw)
        
        # === Build tools list (direct, no provider) ===
        tool_list: list["BaseTool"] = []
        if tools is not None:
            if isinstance(tools, ToolSet):
                tool_list = list(tools.all())
            else:
                tool_list = list(tools)
        
        # Handle subagents - create DelegateTool directly
        if subagents:
            backend = ListSubAgentBackend(subagents)
            tool_cls = delegate_tool_class or DelegateTool
            delegate_tool = tool_cls(backend, middleware=middleware_chain)
            tool_list.append(delegate_tool)
        
        # === Build providers ===
        default_providers: list["ContextProvider"] = []
        
        # MessageContextProvider - for fetching history
        if message_manager:
            message_provider = MessageContextProvider(message_manager)
            default_providers.append(message_provider)
        
        # Combine default + custom context_providers
        all_providers = default_providers + (context_providers or [])
        
        # Build context
        ctx = InvocationContext(
            session=session,
            invocation_id=generate_id("inv"),
            agent_id=config.name if config else "react_agent",
            storage=storage,
            bus=bus,
            llm=llm,
            middleware=middleware_chain,
            memory=memory,
            snapshot=snapshot,
        )
        
        agent = cls(ctx, config)
        agent._tools = tool_list  # Direct tools (not from context_provider)
        agent._context_providers = all_providers
        agent._delegate_tool_class = delegate_tool_class or DelegateTool
        agent._middleware_chain = middleware_chain
        return agent
    
    @classmethod
    async def restore(
        cls,
        session_id: str,
        storage: "StateBackend",
        llm: "LLMProvider",
        *,
        tools: "ToolSet | list[BaseTool] | None" = None,
        config: AgentConfig | None = None,
        bus: "Bus | None" = None,
        middleware: "MiddlewareChain | None" = None,
        memory: "MemoryManager | None" = None,
        snapshot: "SnapshotBackend | None" = None,
    ) -> "ReactAgent":
        """Restore agent from persisted state.
        
        Use this to resume an agent after:
        - Page refresh
        - Process restart
        - Cross-process recovery
        
        Args:
            session_id: Session ID to restore
            storage: State backend containing persisted state
            llm: LLM provider
            tools: Tool registry or list of tools
            config: Agent configuration
            bus: Event bus (auto-created if None)
            middleware: Middleware chain
            memory: Memory manager
            snapshot: Snapshot backend
            
        Returns:
            Restored ReactAgent ready to continue
            
        Raises:
            SessionNotFoundError: If session not found
            
        Example:
            agent = await ReactAgent.restore(
                session_id="sess_xxx",
                storage=my_backend,
                llm=my_llm,
            )
            
            # Check if waiting for HITL response
            if agent.is_suspended:
                print(f"Waiting for: {agent.pending_request}")
            else:
                # Continue conversation
                await agent.run("Continue...")
        """
        from ..core.bus import Bus
        from ..core.types.session import Session, Invocation, InvocationState, generate_id
        from ..core.state import State
        from ..tool import ToolSet
        
        # 1. Load session
        session_data = await storage.get("sessions", session_id)
        if not session_data:
            raise SessionNotFoundError(f"Session not found: {session_id}")
        session = Session.from_dict(session_data)
        
        # 2. Load current invocation
        invocation: Invocation | None = None
        if session_data.get("current_invocation_id"):
            inv_data = await storage.get("invocations", session_data["current_invocation_id"])
            if inv_data:
                invocation = Invocation.from_dict(inv_data)
        
        # 3. Load state
        state = State(storage, session_id)
        await state.restore()
        
        # 4. Handle tools
        tool_set: ToolSet | None = None
        if tools is not None:
            if isinstance(tools, ToolSet):
                tool_set = tools
            else:
                tool_set = ToolSet()
                for tool in tools:
                    tool_set.add(tool)
        else:
            tool_set = ToolSet()
        
        # 5. Create bus if needed
        if bus is None:
            bus = Bus()
        
        # 6. Build context
        ctx = InvocationContext(
            session=session,
            invocation_id=invocation.id if invocation else generate_id("inv"),
            agent_id=config.name if config else "react_agent",
            storage=storage,
            bus=bus,
            llm=llm,
            tools=tool_set,
            middleware=middleware,
            memory=memory,
            snapshot=snapshot,
        )
        
        # 7. Create agent
        agent = cls(ctx, config)
        agent._restored_invocation = invocation
        agent._state = state
        
        return agent

    def __init__(
        self,
        ctx: InvocationContext,
        config: AgentConfig | None = None,
    ):
        """Initialize ReactAgent.

        Args:
            ctx: InvocationContext with llm, tools, storage, bus, session
            config: Agent configuration

        Raises:
            ValueError: If ctx.llm or ctx.tools is None
        """
        super().__init__(ctx, config)

        # Validate required services
        if ctx.llm is None:
            raise ValueError("ReactAgent requires ctx.llm (LLMProvider)")

        # Current execution state
        self._current_invocation: Invocation | None = None
        self._current_step: int = 0
        self._message_history: list[LLMMessage] = []
        self._text_buffer: str = ""
        self._thinking_buffer: str = ""
        self._tool_invocations: list[ToolInvocation] = []
        
        # Block ID tracking for streaming (ensures consecutive deltas use same block_id)
        self._current_text_block_id: str | None = None
        self._current_thinking_block_id: str | None = None
        
        # Tool call tracking for streaming arguments
        self._call_id_to_tool: dict[str, str] = {}  # call_id -> tool_name
        self._tool_call_blocks: dict[str, str] = {}  # call_id -> block_id

        # Pause/resume support
        self._paused = False
        
        # Restore support
        self._restored_invocation: "Invocation | None" = None
        self._state: "State | None" = None
        
        # Direct tools (passed to create())
        self._tools: list["BaseTool"] = []
        
        # ContextProviders for context engineering
        self._context_providers: list[ContextProvider] = []
        
        # DelegateTool class and middleware for dynamic subagent handling
        self._delegate_tool_class: type | None = None
        self._middleware_chain: "MiddlewareChain | None" = None
        
        # Current AgentContext from providers (set by _fetch_agent_context)
        self._agent_context: AgentContext | None = None
    
    # ========== Suspension properties ==========
    
    @property
    def is_suspended(self) -> bool:
        """Check if agent is suspended (waiting for HITL input)."""
        if self._restored_invocation:
            return self._restored_invocation.state == InvocationState.SUSPENDED
        return False
    
    @property
    def state(self) -> "State | None":
        """Get session state (for checkpoint/restore)."""
        return self._state
    
    # ========== Service accessors ==========

    @property
    def llm(self) -> "LLMProvider":
        """Get LLM provider from context."""
        return self._ctx.llm  # type: ignore (validated in __init__)

    @property
    def snapshot(self):
        """Get snapshot backend from context."""
        return self._ctx.snapshot

    async def _execute(self, input: PromptInput | str) -> None:
        """Execute the React loop.

        Args:
            input: User prompt input (PromptInput or str)
        """
        # Normalize input
        if isinstance(input, str):
            input = PromptInput(text=input)
        
        # NOTE: 如果需要 HITL 恢复到同一个 invocation（而不是创建新的），
        # 可以检查 self._restored_invocation.state == SUSPENDED 并恢复精确状态。
        # 当前设计：每次 run() 都创建新 invocation，HITL 回复也是新 invocation。
        
        self.reset()
        self._running = True

        logger.info(
            "Starting ReactAgent run",
            extra={
                "session_id": self.session.id,
                "agent": self.name,
            }
        )

        # Build middleware context
        from ..core.context import emit as global_emit
        mw_context = {
            "session_id": self.session.id,
            "agent_id": self.name,
            "agent_type": self.agent_type,
            "emit": global_emit,  # For middleware to emit ActionEvent
            "storage": self.storage,
        }

        try:
            # Create new invocation
            self._current_invocation = Invocation(
                id=generate_id("inv"),
                session_id=self.session.id,
                state=InvocationState.RUNNING,
                started_at=datetime.now(),
            )
            mw_context["invocation_id"] = self._current_invocation.id

            logger.debug("Created invocation", extra={"invocation_id": self._current_invocation.id})

            # === Middleware: on_agent_start ===
            if self.middleware:
                hook_result = await self.middleware.process_agent_start(
                    self.name, input, mw_context
                )
                if hook_result.action == HookAction.STOP:
                    logger.info("Agent stopped by middleware on_agent_start")
                    await self.ctx.emit(BlockEvent(
                        kind=BlockKind.ERROR,
                        op=BlockOp.APPLY,
                        data={"message": hook_result.message or "Stopped by middleware"},
                    ))
                    return
                elif hook_result.action == HookAction.SKIP:
                    logger.info("Agent skipped by middleware on_agent_start")
                    return

            await self.bus.publish(
                Events.INVOCATION_START,
                {
                    "invocation_id": self._current_invocation.id,
                    "session_id": self.session.id,
                },
            )

            # Build initial messages (loads history from storage)
            self._message_history = await self._build_messages(input)
            self._current_step = 0
            
            # Save user message (real-time persistence)
            await self._save_user_message(input)

            # 3. Main loop
            finish_reason = None

            while not await self._check_abort():
                self._current_step += 1

                # Check step limit
                if self._current_step > self.config.max_steps:
                    logger.warning(
                        "Max steps exceeded",
                        extra={
                            "max_steps": self.config.max_steps,
                            "invocation_id": self._current_invocation.id,
                        },
                    )
                    await self.ctx.emit(BlockEvent(
                        kind=BlockKind.ERROR,
                        op=BlockOp.APPLY,
                        data={"message": f"Max steps ({self.config.max_steps}) exceeded"},
                    ))
                    break

                # Take snapshot before step
                snapshot_id = None
                if self.snapshot:
                    snapshot_id = await self.snapshot.track()

                # Execute step
                finish_reason = await self._execute_step()
                
                # Save assistant message (real-time persistence)
                await self._save_assistant_message()
                
                # Save message_history to state and checkpoint
                if self._state:
                    self._save_messages_to_state()
                    await self._state.checkpoint()

                # Check if we should exit
                if finish_reason == "end_turn" and not self._tool_invocations:
                    break

                # Process tool results and continue
                if self._tool_invocations:
                    await self._process_tool_results()
                    
                    # Save tool messages (real-time persistence)
                    await self._save_tool_messages()
                    
                    self._tool_invocations.clear()
                    
                    # Save message_history to state and checkpoint
                    if self._state:
                        self._save_messages_to_state()
                        await self._state.checkpoint()

            # 4. Check if aborted
            is_aborted = self.is_cancelled
            
            # 5. Complete invocation
            if is_aborted:
                self._current_invocation.state = InvocationState.ABORTED
            else:
                self._current_invocation.state = InvocationState.COMPLETED
            self._current_invocation.finished_at = datetime.now()
            
            # Save to storage
            await self.storage.set(
                "invocations",
                self._current_invocation.id,
                self._current_invocation.to_dict(),
            )

            duration_ms = self._current_invocation.duration_ms or 0
            logger.info(
                f"ReactAgent run {'aborted' if is_aborted else 'completed'}",
                extra={
                    "invocation_id": self._current_invocation.id,
                    "steps": self._current_step,
                    "duration_ms": duration_ms,
                    "finish_reason": "aborted" if is_aborted else finish_reason,
                },
            )

            # === Middleware: on_agent_end ===
            if self.middleware:
                await self.middleware.process_agent_end(
                    self.name,
                    {"steps": self._current_step, "finish_reason": finish_reason},
                    mw_context,
                )

            await self.bus.publish(
                Events.INVOCATION_END,
                {
                    "invocation_id": self._current_invocation.id,
                    "steps": self._current_step,
                    "state": self._current_invocation.state.value,
                },
            )
            
            # Clear message_history from State after successful completion
            # Historical messages are already persisted (truncated) via MessageStore
            self._clear_messages_from_state()
            if self._state:
                await self._state.checkpoint()

        except HITLSuspendError as e:
            # HITL suspension - invocation waits for user input
            logger.info(
                "Agent suspended for HITL",
                extra={
                    "invocation_id": self._current_invocation.id
                    if self._current_invocation
                    else None,
                },
            )
            
            if self._current_invocation:
                self._current_invocation.state = InvocationState.SUSPENDED
                
                # Save invocation state
                await self.storage.set(
                    "invocations",
                    self._current_invocation.id,
                    self._current_invocation.to_dict(),
                )
            
            # Save message_history and checkpoint before suspend
            if self._state:
                self._save_messages_to_state()
                await self._state.checkpoint()
            
            # Don't raise - just return to exit cleanly
            return
        
        except Exception as e:
            logger.error(
                "ReactAgent run failed",
                extra={
                    "error": str(e),
                    "invocation_id": self._current_invocation.id
                    if self._current_invocation
                    else None,
                },
                exc_info=True,
            )

            # === Middleware: on_error ===
            if self.middleware:
                processed_error = await self.middleware.process_error(e, mw_context)
                if processed_error is None:
                    # Error suppressed by middleware
                    logger.info("Error suppressed by middleware")
                    return

            if self._current_invocation:
                self._current_invocation.state = InvocationState.FAILED
                self._current_invocation.finished_at = datetime.now()

            await self.ctx.emit(BlockEvent(
                kind=BlockKind.ERROR,
                op=BlockOp.APPLY,
                data={"message": str(e)},
            ))
            raise

        finally:
            self._running = False
            self._restored_invocation = None

    async def pause(self) -> str:
        """Pause execution and return invocation ID for later resume.

        Saves current state to the invocation for later resumption.

        Returns:
            Invocation ID for resuming
        """
        if not self._current_invocation:
            raise RuntimeError("No active invocation to pause")

        # Mark as paused
        self._paused = True
        self._current_invocation.mark_paused()

        # Save state for resumption
        self._current_invocation.agent_state = {
            "step": self._current_step,
            "message_history": [
                {"role": m.role, "content": m.content} for m in self._message_history
            ],
            "text_buffer": self._text_buffer,
        }
        self._current_invocation.step_count = self._current_step

        # Save pending tool calls
        self._current_invocation.pending_tool_ids = [
            inv.tool_call_id
            for inv in self._tool_invocations
            if inv.state == ToolInvocationState.CALL
        ]

        # Persist invocation
        await self.storage.write(
            f"invocation:{self._current_invocation.id}",
            self._current_invocation.to_dict(),
        )

        await self.bus.publish(
            Events.INVOCATION_PAUSE,
            {
                "invocation_id": self._current_invocation.id,
                "step": self._current_step,
            },
        )

        return self._current_invocation.id

    async def _resume_internal(self, invocation_id: str) -> None:
        """Internal resume logic using emit."""
        # Load invocation
        inv_data = await self.storage.read(f"invocation:{invocation_id}")
        if not inv_data:
            raise ValueError(f"Invocation not found: {invocation_id}")

        invocation = Invocation.from_dict(inv_data)

        if invocation.state != InvocationState.PAUSED:
            raise ValueError(f"Invocation is not paused: {invocation.state}")

        # Restore state
        self._current_invocation = invocation
        self._paused = False
        self._running = True

        agent_state = invocation.agent_state or {}
        self._current_step = agent_state.get("step", 0)
        self._text_buffer = agent_state.get("text_buffer", "")

        # Restore message history
        self._message_history = [
            LLMMessage(role=m["role"], content=m["content"])
            for m in agent_state.get("message_history", [])
        ]

        # Mark as running
        invocation.state = InvocationState.RUNNING

        await self.bus.publish(
            Events.INVOCATION_RESUME,
            {
                "invocation_id": invocation_id,
                "step": self._current_step,
            },
        )

        # Continue execution loop
        try:
            finish_reason = None

            while not await self._check_abort() and not self._paused:
                self._current_step += 1

                if self._current_step > self.config.max_steps:
                    await self.ctx.emit(BlockEvent(
                        kind=BlockKind.ERROR,
                        op=BlockOp.APPLY,
                        data={"message": f"Max steps ({self.config.max_steps}) exceeded"},
                    ))
                    break

                finish_reason = await self._execute_step()
                
                # Save assistant message (real-time persistence)
                await self._save_assistant_message()

                if finish_reason == "end_turn" and not self._tool_invocations:
                    break

                if self._tool_invocations:
                    await self._process_tool_results()
                    
                    # Save tool messages (real-time persistence)
                    await self._save_tool_messages()
                    
                    self._tool_invocations.clear()

            if not self._paused:
                self._current_invocation.state = InvocationState.COMPLETED
                self._current_invocation.finished_at = datetime.now()

        except Exception as e:
            self._current_invocation.state = InvocationState.FAILED
            await self.ctx.emit(BlockEvent(
                kind=BlockKind.ERROR,
                op=BlockOp.APPLY,
                data={"message": str(e)},
            ))
            raise

        finally:
            self._running = False

    async def resume(self, invocation_id: str) -> AsyncIterator[BlockEvent]:
        """Resume paused execution.

        Args:
            invocation_id: ID from pause()

        Yields:
            BlockEvent streaming events
        """
        from ..core.context import _emit_queue_var
        
        queue: asyncio.Queue[BlockEvent] = asyncio.Queue()
        token = _emit_queue_var.set(queue)
        
        try:
            exec_task = asyncio.create_task(self._resume_internal(invocation_id))
            get_task: asyncio.Task | None = None
            
            # Event-driven processing - no timeout delays
            while True:
                # First drain any pending items from queue (non-blocking)
                while True:
                    try:
                        block = queue.get_nowait()
                        yield block
                    except asyncio.QueueEmpty:
                        break
                
                # Exit if task is done and queue is empty
                if exec_task.done() and queue.empty():
                    break
                
                # Create get_task if needed
                if get_task is None or get_task.done():
                    get_task = asyncio.create_task(queue.get())
                
                # Wait for EITHER: queue item OR exec_task completion
                done, _ = await asyncio.wait(
                    {get_task, exec_task},
                    return_when=asyncio.FIRST_COMPLETED,
                )
                
                if get_task in done:
                    try:
                        block = get_task.result()
                        yield block
                        get_task = None
                    except asyncio.CancelledError:
                        pass
            
            # Cancel pending get_task if any
            if get_task and not get_task.done():
                get_task.cancel()
                try:
                    await get_task
                except asyncio.CancelledError:
                    pass
            
            # Final drain after task completion
            while not queue.empty():
                try:
                    block = queue.get_nowait()
                    yield block
                except asyncio.QueueEmpty:
                    break
            
            await exec_task
            
        finally:
            _emit_queue_var.reset(token)

    async def _fetch_agent_context(self, input: PromptInput) -> AgentContext:
        """Fetch context from all providers and merge with direct tools.
        
        Process:
        1. Fetch from all providers and merge
        2. Add direct tools (from create())
        3. If providers returned subagents, create DelegateTool
        
        Also sets ctx.input for providers to access.
        """
        from ..tool.builtin import DelegateTool
        from ..backends.subagent import ListSubAgentBackend
        
        # Set input on context for providers to access
        self._ctx.input = input
        
        # Fetch from all context_providers
        outputs: list[AgentContext] = []
        for provider in self._context_providers:
            try:
                output = await provider.fetch(self._ctx)
                outputs.append(output)
            except Exception as e:
                logger.warning(f"Provider {provider.name} fetch failed: {e}")
        
        # Merge all provider outputs
        merged = AgentContext.merge(outputs)
        
        # Add direct tools (from create())
        all_tools = list(self._tools)  # Copy direct tools
        seen_names = {t.name for t in all_tools}
        
        # Add tools from providers (deduplicate)
        for tool in merged.tools:
            if tool.name not in seen_names:
                seen_names.add(tool.name)
                all_tools.append(tool)
        
        # If providers returned subagents, create DelegateTool
        if merged.subagents:
            # Check if we already have a delegate tool
            has_delegate = any(t.name == "delegate" for t in all_tools)
            if not has_delegate:
                backend = ListSubAgentBackend(merged.subagents)
                tool_cls = self._delegate_tool_class or DelegateTool
                delegate_tool = tool_cls(backend, middleware=self._middleware_chain)
                all_tools.append(delegate_tool)
        
        # Return merged context with combined tools
        return AgentContext(
            system_content=merged.system_content,
            user_content=merged.user_content,
            tools=all_tools,
            messages=merged.messages,
            subagents=merged.subagents,
            skills=merged.skills,
        )
    
    async def _build_messages(self, input: PromptInput) -> list[LLMMessage]:
        """Build message history for LLM.
        
        Uses AgentContext from providers for system content, messages, etc.
        """
        messages = []
        
        # Fetch context from providers
        self._agent_context = await self._fetch_agent_context(input)

        # System message: config.system_prompt + agent_context.system_content
        system_prompt = self.config.system_prompt or self._default_system_prompt()
        if self._agent_context.system_content:
            system_prompt = system_prompt + "\n\n" + self._agent_context.system_content
        messages.append(LLMMessage(role="system", content=system_prompt))
        
        # Historical messages from AgentContext (provided by MessageContextProvider)
        for msg in self._agent_context.messages:
            messages.append(LLMMessage(
                role=msg.get("role", "user"),
                content=msg.get("content", ""),
            ))

        # User content prefix (from providers) + current user message
        content = input.text
        if self._agent_context.user_content:
            content = self._agent_context.user_content + "\n\n" + content
        
        if input.attachments:
            # Build multimodal content
            content_parts = [{"type": "text", "text": content}]
            for attachment in input.attachments:
                content_parts.append(attachment)
            content = content_parts

        messages.append(LLMMessage(role="user", content=content))

        return messages

    def _default_system_prompt(self) -> str:
        """Generate default system prompt with tool descriptions."""
        # Get tools from AgentContext (from providers)
        all_tools = self._agent_context.tools if self._agent_context else []
        
        tool_list = []
        for tool in all_tools:
            info = tool.get_info()
            tool_list.append(f"- {info.name}: {info.description}")

        tools_desc = "\n".join(tool_list) if tool_list else "No tools available."

        return f"""You are a helpful AI assistant with access to tools.

Available tools:
{tools_desc}

When you need to use a tool, make a tool call. After receiving the tool result, continue reasoning or provide your final response.

Think step by step and use tools when necessary to complete the user's request."""

    async def _execute_step(self) -> str | None:
        """Execute a single LLM step with middleware hooks.
        
        Returns:
            finish_reason from LLM
        """
        # Get tools from AgentContext (from providers)
        all_tools = self._agent_context.tools if self._agent_context else []
        
        # Get tool definitions
        tool_defs = [
            ToolDefinition(
                name=t.name,
                description=t.description,
                input_schema=t.parameters,
            )
            for t in all_tools
        ]

        # Reset buffers
        self._text_buffer = ""
        self._thinking_buffer = ""  # Buffer for non-streaming thinking
        self._tool_invocations = []
        current_tool_invocation: ToolInvocation | None = None
        
        # Reset block IDs for this step (each step gets fresh block IDs)
        self._current_text_block_id = None
        self._current_thinking_block_id = None
        
        # Reset tool call tracking
        self._call_id_to_tool = {}
        self._tool_call_blocks = {}

        # Build middleware context for this step
        from ..core.context import emit as global_emit
        mw_context = {
            "session_id": self.session.id,
            "invocation_id": self._current_invocation.id if self._current_invocation else "",
            "step": self._current_step,
            "agent_id": self.name,
            "emit": global_emit,  # For middleware to emit BlockEvent/ActionEvent
            "storage": self.storage,
        }

        # Build LLM call kwargs
        llm_kwargs: dict[str, Any] = {
            "messages": self._message_history,
            "tools": tool_defs if tool_defs else None,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
        }

        # Add thinking configuration
        if self.config.enable_thinking:
            llm_kwargs["enable_thinking"] = True
            if self.config.reasoning_effort:
                llm_kwargs["reasoning_effort"] = self.config.reasoning_effort
        
        # Add LLM override parameters (only if explicitly set)
        if self.config.llm_timeout is not None:
            llm_kwargs["timeout"] = self.config.llm_timeout
        if self.config.llm_max_retries is not None:
            llm_kwargs["max_retries"] = self.config.llm_max_retries
        if self.config.llm_retry_delay is not None:
            llm_kwargs["retry_delay"] = self.config.llm_retry_delay
        if self.config.llm_retry_backoff is not None:
            llm_kwargs["retry_backoff"] = self.config.llm_retry_backoff
        llm_kwargs["retry_on_timeout"] = self.config.llm_retry_on_timeout
        llm_kwargs["retry_on_rate_limit"] = self.config.llm_retry_on_rate_limit

        # === Middleware: on_request ===
        if self.middleware:
            llm_kwargs = await self.middleware.process_request(llm_kwargs, mw_context)
            if llm_kwargs is None:
                logger.info("LLM request cancelled by middleware")
                return None

        # Debug: log message history before LLM call
        logger.debug(
            f"LLM call - Step {self._current_step}, messages: {len(self._message_history)}, "
            f"tools: {len(tool_defs) if tool_defs else 0}"
        )
        # Detailed message log (for debugging model issues like repeated calls)
        for i, msg in enumerate(self._message_history):
            content_preview = str(msg.content)[:300] if msg.content else "<empty>"
            tool_call_id = getattr(msg, 'tool_call_id', None)
            logger.debug(
                f"  msg[{i}] role={msg.role}"
                f"{f', tool_call_id={tool_call_id}' if tool_call_id else ''}"
                f", content={content_preview}"
            )
        
        # Call LLM
        await self.bus.publish(
            Events.LLM_START,
            {
                "provider": self.llm.provider,
                "model": self.llm.model,
                "step": self._current_step,
                "enable_thinking": self.config.enable_thinking,
            },
        )

        finish_reason = None
        llm_response_data: dict[str, Any] = {}  # Collect response for middleware

        # Reset middleware stream state
        if self.middleware:
            self.middleware.reset_stream_state()

        async for event in self.llm.complete(**llm_kwargs):
            if await self._check_abort():
                break

            if event.type == "content":
                # Text content
                if event.delta:
                    # === Middleware: on_model_stream ===
                    stream_chunk = {"delta": event.delta, "type": "content"}
                    if self.middleware:
                        stream_chunk = await self.middleware.process_stream_chunk(
                            stream_chunk, mw_context
                        )
                        if stream_chunk is None:
                            continue  # Skip this chunk

                    delta = stream_chunk.get("delta", event.delta)
                    self._text_buffer += delta
                    
                    # Reuse or create block_id for text streaming
                    if self._current_text_block_id is None:
                        self._current_text_block_id = generate_id("blk")
                    
                    await self.ctx.emit(BlockEvent(
                        block_id=self._current_text_block_id,
                        kind=BlockKind.TEXT,
                        op=BlockOp.DELTA,
                        data={"content": delta},
                    ))

                    await self.bus.publish(
                        Events.LLM_STREAM,
                        {
                            "delta": delta,
                            "step": self._current_step,
                        },
                    )

            elif event.type == "thinking":
                # Thinking content - only emit if thinking is enabled
                if event.delta and self.config.enable_thinking:
                    if self.config.stream_thinking:
                        # Reuse or create block_id for thinking streaming
                        if self._current_thinking_block_id is None:
                            self._current_thinking_block_id = generate_id("blk")
                        
                        # Stream thinking in real-time
                        await self.ctx.emit(BlockEvent(
                            block_id=self._current_thinking_block_id,
                            kind=BlockKind.THINKING,
                            op=BlockOp.DELTA,
                            data={"content": event.delta},
                        ))
                    else:
                        # Buffer thinking for batch output
                        self._thinking_buffer += event.delta

            elif event.type == "tool_call_start":
                # Tool call started (name known, arguments pending)
                if event.tool_call:
                    tc = event.tool_call
                    self._call_id_to_tool[tc.id] = tc.name
                    
                    # Always emit start notification (privacy-safe, no arguments)
                    block_id = generate_id("blk")
                    self._tool_call_blocks[tc.id] = block_id
                    
                    await self.ctx.emit(BlockEvent(
                        block_id=block_id,
                        kind=BlockKind.TOOL_USE,
                        op=BlockOp.APPLY,
                        data={
                            "name": tc.name,
                            "call_id": tc.id,
                            "status": "streaming",  # Indicate arguments are streaming
                        },
                    ))

            elif event.type == "tool_call_delta":
                # Tool arguments delta (streaming)
                if event.tool_call_delta:
                    call_id = event.tool_call_delta.get("call_id")
                    arguments_delta = event.tool_call_delta.get("arguments_delta")
                    
                    if call_id and arguments_delta:
                        tool_name = self._call_id_to_tool.get(call_id)
                        if tool_name:
                            tool = self._get_tool(tool_name)
                            
                            # Check if tool allows streaming arguments
                            if tool and tool.config.stream_arguments:
                                block_id = self._tool_call_blocks.get(call_id)
                                if block_id:
                                    await self.ctx.emit(BlockEvent(
                                        block_id=block_id,
                                        kind=BlockKind.TOOL_USE,
                                        op=BlockOp.DELTA,
                                        data={
                                            "call_id": call_id,
                                            "arguments_delta": arguments_delta,
                                        },
                                    ))

            elif event.type == "tool_call_progress":
                # Tool arguments progress (bytes received)
                if event.tool_call_progress:
                    call_id = event.tool_call_progress.get("call_id")
                    bytes_received = event.tool_call_progress.get("bytes_received")
                    
                    if call_id and bytes_received is not None:
                        block_id = self._tool_call_blocks.get(call_id)
                        if block_id:
                            # Always emit progress (privacy-safe, no content)
                            await self.ctx.emit(BlockEvent(
                                block_id=block_id,
                                kind=BlockKind.TOOL_USE,
                                op=BlockOp.PATCH,
                                data={
                                    "call_id": call_id,
                                    "bytes_received": bytes_received,
                                    "status": "receiving",
                                },
                            ))

            elif event.type == "tool_call":
                # Tool call complete (arguments fully received)
                if event.tool_call:
                    tc = event.tool_call
                    invocation = ToolInvocation(
                        tool_call_id=tc.id,
                        tool_name=tc.name,
                        args_raw=tc.arguments,
                        state=ToolInvocationState.CALL,
                    )

                    # Parse arguments
                    try:
                        invocation.args = json.loads(tc.arguments)
                    except json.JSONDecodeError:
                        invocation.args = {}

                    self._tool_invocations.append(invocation)

                    # Strict mode: require tool_call_start to be received first
                    # TODO: Uncomment below for compatibility with providers that don't send tool_call_start
                    # block_id = self._tool_call_blocks.get(tc.id)
                    # if block_id is None:
                    #     # No streaming start event, create block now
                    #     block_id = generate_id("blk")
                    #     self._tool_call_blocks[tc.id] = block_id
                    #     self._call_id_to_tool[tc.id] = tc.name
                    #     
                    #     # Emit APPLY with full data
                    #     await self.ctx.emit(BlockEvent(
                    #         block_id=block_id,
                    #         kind=BlockKind.TOOL_USE,
                    #         op=BlockOp.APPLY,
                    #         data={
                    #             "name": tc.name,
                    #             "call_id": tc.id,
                    #             "arguments": invocation.args,
                    #             "status": "ready",
                    #         },
                    #     ))
                    # else:
                    #     # Update existing block with complete arguments
                    #     await self.ctx.emit(BlockEvent(
                    #         block_id=block_id,
                    #         kind=BlockKind.TOOL_USE,
                    #         op=BlockOp.PATCH,
                    #         data={
                    #             "call_id": tc.id,
                    #             "arguments": invocation.args,
                    #             "status": "ready",
                    #         },
                    #     ))
                    
                    # Strict mode: tool_call_start must have been received
                    block_id = self._tool_call_blocks[tc.id]  # Will raise KeyError if not found
                    await self.ctx.emit(BlockEvent(
                        block_id=block_id,
                        kind=BlockKind.TOOL_USE,
                        op=BlockOp.PATCH,
                        data={
                            "call_id": tc.id,
                            "arguments": invocation.args,
                            "status": "ready",
                        },
                    ))

                    await self.bus.publish(
                        Events.TOOL_START,
                        {
                            "call_id": tc.id,
                            "tool": tc.name,
                            "arguments": invocation.args,
                        },
                    )

            elif event.type == "completed":
                finish_reason = event.finish_reason

            elif event.type == "usage":
                if event.usage:
                    await self.bus.publish(
                        Events.USAGE_RECORDED,
                        {
                            "provider": self.llm.provider,
                            "model": self.llm.model,
                            "input_tokens": event.usage.input_tokens,
                            "output_tokens": event.usage.output_tokens,
                            "cache_read_tokens": event.usage.cache_read_tokens,
                            "cache_write_tokens": event.usage.cache_write_tokens,
                            "reasoning_tokens": event.usage.reasoning_tokens,
                        },
                    )

            elif event.type == "error":
                await self.ctx.emit(BlockEvent(
                    kind=BlockKind.ERROR,
                    op=BlockOp.APPLY,
                    data={"message": event.error or "Unknown LLM error"},
                ))

        # If thinking was buffered, emit it now
        if self._thinking_buffer and not self.config.stream_thinking:
            await self.ctx.emit(BlockEvent(
                kind=BlockKind.THINKING,
                op=BlockOp.APPLY,
                data={"content": self._thinking_buffer},
            ))

        # === Middleware: on_response ===
        llm_response_data = {
            "text": self._text_buffer,
            "thinking": self._thinking_buffer,
            "tool_calls": len(self._tool_invocations),
            "finish_reason": finish_reason,
        }
        if self.middleware:
            llm_response_data = await self.middleware.process_response(
                llm_response_data, mw_context
            )

        await self.bus.publish(
            Events.LLM_END,
            {
                "step": self._current_step,
                "finish_reason": finish_reason,
                "text_length": len(self._text_buffer),
                "thinking_length": len(self._thinking_buffer),
                "tool_calls": len(self._tool_invocations),
            },
        )

        # Add assistant message to history
        if self._text_buffer or self._tool_invocations:
            assistant_content: Any = self._text_buffer
            if self._tool_invocations:
                # Build content with tool calls
                content_parts = []
                if self._text_buffer:
                    content_parts.append({"type": "text", "text": self._text_buffer})
                for inv in self._tool_invocations:
                    content_parts.append(
                        {
                            "type": "tool_use",
                            "id": inv.tool_call_id,
                            "name": inv.tool_name,
                            "input": inv.args,
                        }
                    )
                assistant_content = content_parts

            self._message_history.append(
                LLMMessage(
                    role="assistant",
                    content=assistant_content,
                )
            )

        return finish_reason

    async def _process_tool_results(self) -> None:
        """Execute tool calls and add results to history.

        Executes tools in parallel or sequentially based on config.
        """
        if not self._tool_invocations:
            return

        # Execute tools based on configuration
        if self.config.parallel_tool_execution:
            # Parallel execution using asyncio.gather with create_task
            # create_task ensures each task gets its own ContextVar copy
            tasks = [asyncio.create_task(self._execute_tool(inv)) for inv in self._tool_invocations]
            results = await asyncio.gather(*tasks, return_exceptions=True)
        else:
            # Sequential execution
            results = []
            for inv in self._tool_invocations:
                try:
                    result = await self._execute_tool(inv)
                    results.append(result)
                except Exception as e:
                    results.append(e)

        # Check for HITLSuspendError first - must propagate
        for result in results:
            if isinstance(result, HITLSuspendError):
                raise result
        
        # Process results
        tool_results = []

        for invocation, result in zip(self._tool_invocations, results):
            # Handle exceptions from gather
            if isinstance(result, Exception):
                error_msg = f"Tool execution error: {str(result)}"
                invocation.mark_result(error_msg, is_error=True)
                result = ToolResult.error(error_msg)

            # Get parent block_id from tool_call mapping
            parent_block_id = self._tool_call_blocks.get(invocation.tool_call_id)
            
            await self.ctx.emit(BlockEvent(
                kind=BlockKind.TOOL_RESULT,
                op=BlockOp.APPLY,
                parent_id=parent_block_id,
                data={
                    "call_id": invocation.tool_call_id,
                    "content": result.output,
                    "is_error": invocation.is_error,
                },
            ))

            await self.bus.publish(
                Events.TOOL_END,
                {
                    "call_id": invocation.tool_call_id,
                    "tool": invocation.tool_name,
                    "result": result.output[:500],  # Truncate for event
                    "is_error": invocation.is_error,
                    "duration_ms": invocation.duration_ms,
                },
            )

            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": invocation.tool_call_id,
                    "content": result.output,
                    "is_error": invocation.is_error,
                }
            )

        # Add tool results as tool messages (OpenAI format)
        for tr in tool_results:
            print(f"[DEBUG _process_tool_results] Adding tool_result to history: {tr}")
            self._message_history.append(
                LLMMessage(
                    role="tool",
                    content=tr["content"],
                    tool_call_id=tr["tool_use_id"],
                )
            )

    def _save_messages_to_state(self) -> None:
        """Save current message_history to State for recovery.
        
        This saves the COMPLETE message history (not truncated) to State,
        allowing recovery from HITL suspend or crash.
        
        Truncated messages are saved separately via MessagePersistenceMiddleware.
        """
        if not self._state:
            return
        
        # Serialize message history
        messages_data = []
        for msg in self._message_history:
            msg_dict = {"role": msg.role, "content": msg.content}
            if hasattr(msg, "tool_call_id") and msg.tool_call_id:
                msg_dict["tool_call_id"] = msg.tool_call_id
            messages_data.append(msg_dict)
        
        # Save to state.agent.message_history
        self._state.set("agent.message_history", messages_data)
        
        # Also save invocation_id for recovery context
        if self._current_invocation:
            self._state.set("agent.current_invocation_id", self._current_invocation.id)
    
    def _clear_messages_from_state(self) -> None:
        """Clear message_history from State after inv completes.
        
        Called when invocation completes normally. Historical messages
        are already persisted (truncated) via MessageStore.
        """
        if not self._state:
            return
        
        self._state.delete("agent.message_history")
        self._state.delete("agent.current_invocation_id")
    
    async def _trigger_message_save(self, message: dict) -> dict | None:
        """Trigger on_message_save hook via middleware.
        
        Message persistence is handled by MessagePersistenceMiddleware.
        Agent only triggers the hook, doesn't save directly.
        
        Args:
            message: Message dict with role, content, etc.
            
        Returns:
            Modified message or None if blocked
        """
        # Check if message saving is disabled (e.g., for sub-agents with record_messages=False)
        if getattr(self, '_disable_message_save', False):
            return message
        
        if not self.middleware:
            return message
        
        namespace = getattr(self, '_message_namespace', None)
        mw_context = {
            "session_id": self.session.id,
            "agent_id": self.name,
            "namespace": namespace,
        }
        
        return await self.middleware.process_message_save(message, mw_context)
    
    async def _save_user_message(self, input: PromptInput) -> None:
        """Trigger save for user message."""
        # Build user content
        content: str | list[dict] = input.text
        if self._agent_context and self._agent_context.user_content:
            content = self._agent_context.user_content + "\n\n" + input.text
        
        if input.attachments:
            content_parts: list[dict] = [{"type": "text", "text": content}]
            for attachment in input.attachments:
                content_parts.append(attachment)
            content = content_parts
        
        # Build message and trigger hook
        message = {
            "role": "user",
            "content": content,
            "invocation_id": self._current_invocation.id if self._current_invocation else "",
        }
        
        await self._trigger_message_save(message)
    
    async def _save_assistant_message(self) -> None:
        """Trigger save for assistant message."""
        if not self._text_buffer and not self._tool_invocations:
            return
        
        # Build assistant content
        content: str | list[dict] = self._text_buffer
        if self._tool_invocations:
            content_parts: list[dict] = []
            if self._text_buffer:
                content_parts.append({"type": "text", "text": self._text_buffer})
            for inv in self._tool_invocations:
                content_parts.append({
                    "type": "tool_use",
                    "id": inv.tool_call_id,
                    "name": inv.tool_name,
                    "input": inv.args,
                })
            content = content_parts
        
        # Build message and trigger hook
        message = {
            "role": "assistant",
            "content": content,
            "invocation_id": self._current_invocation.id if self._current_invocation else "",
        }
        
        await self._trigger_message_save(message)
    
    async def _save_tool_messages(self) -> None:
        """Trigger save for tool result messages."""
        for inv in self._tool_invocations:
            if inv.result is not None:
                # Build tool result message
                content: list[dict] = [{
                    "type": "tool_result",
                    "tool_use_id": inv.tool_call_id,
                    "content": inv.result,
                    "is_error": inv.is_error,
                }]
                
                message = {
                    "role": "tool",
                    "content": content,
                    "tool_call_id": inv.tool_call_id,
                    "invocation_id": self._current_invocation.id if self._current_invocation else "",
                }
                
                await self._trigger_message_save(message)
    
    def _get_tool(self, tool_name: str) -> "BaseTool | None":
        """Get tool by name from agent context."""
        if self._agent_context:
            for tool in self._agent_context.tools:
                if tool.name == tool_name:
                    return tool
        return None
    
    async def _execute_tool(self, invocation: ToolInvocation) -> ToolResult:
        """Execute a single tool call."""
        invocation.mark_call_complete()

        # Build middleware context
        mw_context = {
            "session_id": self.session.id,
            "invocation_id": self._current_invocation.id if self._current_invocation else "",
            "tool_call_id": invocation.tool_call_id,
            "agent_id": self.name,
        }

        try:
            # Get tool from agent context
            tool = self._get_tool(invocation.tool_name)
            if tool is None:
                error_msg = f"Unknown tool: {invocation.tool_name}"
                invocation.mark_result(error_msg, is_error=True)
                return ToolResult.error(error_msg)

            # === Middleware: on_tool_call ===
            if self.middleware:
                hook_result = await self.middleware.process_tool_call(
                    tool, invocation.args, mw_context
                )
                if hook_result.action == HookAction.SKIP:
                    logger.info(f"Tool {invocation.tool_name} skipped by middleware")
                    return ToolResult(
                        output=hook_result.message or "Skipped by middleware",
                        is_error=False,
                    )
                elif hook_result.action == HookAction.RETRY and hook_result.modified_data:
                    invocation.args = hook_result.modified_data

            # Create ToolContext
            tool_ctx = ToolContext(
                session_id=self.session.id,
                invocation_id=self._current_invocation.id if self._current_invocation else "",
                block_id="",
                call_id=invocation.tool_call_id,
                agent=self.config.name,
                abort_signal=self._abort,
                update_metadata=self._noop_update_metadata,
                middleware=self.middleware,
            )

            # Execute tool directly (with timeout)
            timeout = tool.config.timeout if tool.config.timeout is not None else self.config.tool_timeout
            result = await asyncio.wait_for(
                tool.execute(invocation.args, tool_ctx),
                timeout=timeout,
            )

            # === Middleware: on_tool_end ===
            if self.middleware:
                hook_result = await self.middleware.process_tool_end(tool, result, mw_context)
                if hook_result.action == HookAction.RETRY:
                    logger.info(f"Tool {invocation.tool_name} retry requested by middleware")

            invocation.mark_result(result.output, is_error=result.is_error)
            return result

        except asyncio.TimeoutError:
            error_msg = f"Tool {invocation.tool_name} timed out after {self.config.tool_timeout}s"
            invocation.mark_result(error_msg, is_error=True)
            return ToolResult.error(error_msg)

        except HITLSuspendError:
            # HITL suspension must propagate up
            raise
        
        except Exception as e:
            error_msg = f"Tool execution error: {str(e)}"
            invocation.mark_result(error_msg, is_error=True)
            return ToolResult.error(error_msg)

    async def _noop_update_metadata(self, metadata: dict[str, Any]) -> None:
        """No-op metadata updater."""
        pass
