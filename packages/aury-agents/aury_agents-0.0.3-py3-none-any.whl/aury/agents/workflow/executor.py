"""Workflow executor with middleware support and lifecycle hooks."""
from __future__ import annotations

import asyncio
import time
from typing import Any, AsyncIterator, TYPE_CHECKING

from ..core.logging import workflow_logger as logger
from ..core.context import InvocationContext
from ..core.bus import Events
from ..core.types.block import BlockEvent, BlockKind, BlockOp
from ..middleware import HookAction
from .types import NodeType, NodeSpec, Workflow
from .expression import ExpressionEvaluator
from .state import WorkflowState, get_merge_strategy
from .dag import DAGExecutor
from ..core.factory import AgentFactory

if TYPE_CHECKING:
    from ..middleware import MiddlewareChain


class WorkflowExecutor:
    """Workflow executor with middleware hooks.
    
    Middleware priority:
    1. Node-level middleware (from NodeSpec.middleware)
    2. Workflow-level middleware (from WorkflowSpec.middleware)
    3. Context middleware (from InvocationContext.middleware)
    
    Calls middleware hooks:
    - on_subagent_start/end: when executing agent nodes
    """
    
    def __init__(
        self,
        workflow: Workflow,
        agent_factory: AgentFactory,
        ctx: InvocationContext,
        middleware: "MiddlewareChain | None" = None,
    ):
        self.workflow = workflow
        self.agent_factory = agent_factory
        self.ctx = ctx
        # Priority: explicit > workflow spec > context
        self.middleware = middleware or workflow.spec.middleware or ctx.middleware
        self.evaluator = ExpressionEvaluator()
        
        self._state = WorkflowState()
        self._paused = False
        self._waiting_for_input = False
        self._start_time: float | None = None
        self._node_usage: dict[str, dict] = {}  # Track per-node usage
    
    async def execute(
        self,
        inputs: dict[str, Any],
        resume_state: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Execute workflow.
        
        Args:
            inputs: Workflow inputs
            resume_state: State to resume from (for pause/resume)
            
        Returns:
            Final workflow state/result
        """
        self._start_time = time.time()
        
        # Publish start event via Bus
        await self.ctx.bus.publish(Events.INVOCATION_START, {
            "invocation_id": self.ctx.invocation_id,
            "session_id": self.ctx.session_id,
            "workflow": self.workflow.spec.name,
        })
        
        # Resume from saved state if provided
        if resume_state:
            self._state = WorkflowState.from_dict(resume_state.get("workflow_state", {}))
            completed_nodes = set(resume_state.get("completed_nodes", []))
        else:
            completed_nodes = set()
        
        logger.info(
            "Starting workflow execution",
            extra={
                "workflow": self.workflow.spec.name,
                "session_id": self.ctx.session_id,
                "invocation_id": self.ctx.invocation_id,
            }
        )
        
        eval_context = {
            "inputs": inputs,
            "state": self._state,
        }
        
        dag = DAGExecutor(
            tasks=self.workflow.spec.nodes,
            get_task_id=lambda n: n.id,
            get_dependencies=lambda n: self.workflow.incoming_edges[n.id],
        )
        
        # Mark already completed nodes (for resume)
        for node_id in completed_nodes:
            dag.mark_completed(node_id)
        
        while not dag.is_finished() and not self.ctx.is_aborted and not self._paused and not self._waiting_for_input:
            ready_nodes = dag.get_ready_tasks()
            
            if not ready_nodes:
                await asyncio.sleep(0.05)
                continue
            
            tasks = []
            for node in ready_nodes:
                # Check condition
                if node.when:
                    if not self.evaluator.evaluate_condition(node.when, eval_context):
                        dag.mark_skipped(node.id)
                        continue
                
                dag.mark_running(node.id)
                task = asyncio.create_task(
                    self._execute_node(node, eval_context, dag)
                )
                tasks.append(task)
            
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
            
            # Persist state periodically
            await self._persist_state(dag, inputs)
        
        # Publish end event
        status = dag.get_status()
        
        # Calculate workflow duration
        duration_ms = int((time.time() - self._start_time) * 1000) if self._start_time else 0
        
        # Summarize usage
        usage_summary = None
        if self.ctx.usage:
            usage_summary = self.ctx.usage.summarize(
                session_id=self.ctx.session_id,
                invocation_id=self.ctx.invocation_id,
            )
        
        final_data = {
            "state": self._state.to_dict(),
            "status": status,
            "duration_ms": duration_ms,
            "usage": usage_summary,
            "node_usage": self._node_usage,
        }
        
        # Publish end event via Bus (includes usage summary)
        await self.ctx.bus.publish(Events.INVOCATION_END, {
            "invocation_id": self.ctx.invocation_id,
            "session_id": self.ctx.session_id,
            "status": "paused" if self._waiting_for_input else "completed",
            "usage": usage_summary,
        })
        
        logger.info(
            "Workflow execution completed",
            extra={
                "workflow": self.workflow.spec.name,
                "completed": status["completed"],
                "failed": status["failed"],
                "duration_ms": duration_ms,
                "total_tokens": usage_summary.get("total_tokens") if usage_summary else 0,
            }
        )
        
        return final_data
    
    async def _persist_state(self, dag: DAGExecutor, inputs: dict[str, Any] | None = None) -> None:
        """Persist workflow state for recovery."""
        state_key = f"workflow_state:{self.ctx.invocation_id}"
        await self.ctx.storage.write(state_key, {
            "workflow_state": self._state.to_dict(),
            "completed_nodes": list(dag.get_status().get("completed_ids", [])),
            "inputs": inputs or {},
            "waiting_for_input": self._waiting_for_input,
        })
    
    def pause(self) -> None:
        """Pause execution."""
        self._paused = True
    
    async def _execute_node(
        self,
        node: NodeSpec,
        eval_context: dict[str, Any],
        dag: DAGExecutor,
    ) -> None:
        """Execute single node with lifecycle hooks."""
        node_start_time = time.time()
        
        try:
            match node.type:
                case NodeType.TRIGGER | NodeType.TERMINAL:
                    dag.mark_completed(node.id)
                
                case NodeType.AGENT:
                    # Resolve inputs
                    inputs = self.evaluator.resolve_inputs(node.inputs, eval_context)
                    
                    # Publish NODE_START via Bus
                    await self.ctx.bus.publish(Events.NODE_START, {
                        "node_id": node.id,
                        "agent": node.agent,
                        "inputs": inputs,
                        "session_id": self.ctx.session_id,
                        "invocation_id": self.ctx.invocation_id,
                    })
                    
                    result = await self._execute_agent_node(node, eval_context)
                    
                    # Record node duration
                    duration_ms = int((time.time() - node_start_time) * 1000)
                    self._node_usage[node.id] = {
                        "duration_ms": duration_ms,
                        "agent": node.agent,
                    }
                    
                    # Publish NODE_END via Bus
                    await self.ctx.bus.publish(Events.NODE_END, {
                        "node_id": node.id,
                        "agent": node.agent,
                        "duration_ms": duration_ms,
                        "session_id": self.ctx.session_id,
                        "invocation_id": self.ctx.invocation_id,
                    })
                    
                    dag.mark_completed(node.id)
                
                case NodeType.CONDITION:
                    await self._execute_condition_node(node, eval_context, dag)
                
                case _:
                    dag.mark_completed(node.id)
        
        except Exception as e:
            logger.error(
                "Node execution failed",
                extra={"node_id": node.id, "error": str(e)}
            )
            
            # Publish NODE_ERROR via Bus
            await self.ctx.bus.publish(Events.NODE_ERROR, {
                "node_id": node.id,
                "error": str(e),
                "session_id": self.ctx.session_id,
                "invocation_id": self.ctx.invocation_id,
            })
            
            dag.mark_failed(node.id)
            await self.ctx.emit(BlockEvent(
                kind=BlockKind.ERROR,
                op=BlockOp.APPLY,
                data={"node_id": node.id, "error": str(e)},
            ))
    
    async def _execute_agent_node(
        self,
        node: NodeSpec,
        eval_context: dict[str, Any],
    ) -> Any:
        """Execute agent node and return result."""
        if "foreach" in node.config:
            items = self.evaluator.evaluate(node.config["foreach"], eval_context)
            item_var = node.config.get("as", "item")
            merge_strategy = node.config.get("merge", "collect_list")
            
            results = []
            for item in items:
                branch_state = self._state.create_branch()
                branch_context = {
                    **eval_context,
                    item_var: item,
                    "state": branch_state,
                }
                
                result = await self._run_single_agent(node, branch_context)
                results.append(result)
            
            strategy = get_merge_strategy(merge_strategy)
            merged = strategy.merge(results)
            if node.output:
                self._state[node.output] = merged
            return merged
        else:
            result = await self._run_single_agent(node, eval_context)
            if node.output:
                self._state[node.output] = result
            return result
    
    def _get_effective_middleware(
        self,
        node: NodeSpec,
    ) -> "MiddlewareChain | None":
        """Get effective middleware for a node.
        
        Merges node-level middleware with workflow/context middleware.
        Node middleware takes precedence (runs first).
        """
        from ..middleware import MiddlewareChain
        
        # Start with workflow/context middleware
        base_middleware = self.middleware
        
        # If node has its own middleware, create merged chain
        if node.middleware:
            merged = MiddlewareChain()
            
            # Add node middleware first (higher priority)
            for mw in node.middleware:
                merged.use(mw)
            
            # Add base middleware (lower priority)
            if base_middleware:
                for mw in base_middleware.middlewares:
                    merged.use(mw)
            
            return merged
        
        return base_middleware
    
    async def _run_single_agent(
        self,
        node: NodeSpec,
        eval_context: dict[str, Any],
    ) -> Any:
        """Execute single agent with middleware hooks.
        
        Sub-agent's emit calls go to the same ContextVar queue,
        so they automatically flow to the parent's run() yield.
        """
        inputs = self.evaluator.resolve_inputs(node.inputs, eval_context)
        
        # Get effective middleware for this node
        effective_middleware = self._get_effective_middleware(node)
        
        # Build middleware context
        mw_context = {
            "session_id": self.ctx.session_id,
            "invocation_id": self.ctx.invocation_id,
            "parent_agent_id": self.workflow.spec.name,
            "child_agent_id": node.agent,
            "node_id": node.id,
            "has_node_middleware": bool(node.middleware),
        }
        
        # === Middleware: on_subagent_start ===
        if effective_middleware:
            hook_result = await effective_middleware.process_subagent_start(
                self.workflow.spec.name,
                node.agent,
                "embedded",  # Workflow nodes are embedded execution
                mw_context,
            )
            if hook_result.action == HookAction.SKIP:
                logger.info(f"SubAgent {node.agent} skipped by middleware")
                return {"skipped": True, "message": hook_result.message}
        
        # Create child context for sub-agent with effective middleware
        child_ctx = self.ctx.create_child(
            agent_id=node.agent,
            middleware=effective_middleware,
        )
        
        agent = self.agent_factory.create(
            agent_type=node.agent,
            ctx=child_ctx,
        )
        
        # Run agent - its emit calls go to the same ContextVar queue
        # So output flows automatically to parent's run() yield
        result = None
        async for response in agent.run(inputs):
            # Check for result in response
            if response.type == "session_end" and response.data:
                result = response.data.get("result")
        
        # === Middleware: on_subagent_end ===
        if effective_middleware:
            await effective_middleware.process_subagent_end(
                self.workflow.spec.name,
                node.agent,
                result,
                mw_context,
            )
        
        return result
    
    async def _execute_condition_node(
        self,
        node: NodeSpec,
        eval_context: dict[str, Any],
        dag: DAGExecutor,
    ) -> None:
        """Execute condition node."""
        condition_result = self.evaluator.evaluate_condition(
            node.expression, eval_context
        )
        
        if condition_result:
            # then branch - mark else branch as skipped
            if node.else_node:
                dag.mark_skipped(node.else_node)
        else:
            # else branch - mark then branch as skipped
            if node.then_node:
                dag.mark_skipped(node.then_node)
        
        dag.mark_completed(node.id)
    
    def stop(self) -> None:
        """Stop execution."""
        self.ctx.abort_self.set()
    
    @property
    def state(self) -> WorkflowState:
        """Get current state."""
        return self._state
