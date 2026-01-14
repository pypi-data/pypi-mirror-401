"""State management with checkpoint support.

State provides layered storage with three partitions:
- vars: Developer variables for prompt formatting
- workflow: Workflow node outputs
- agent: Agent internal state

Supports path-based access, pattern matching, and checkpoint/restore.
"""
from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..backends.state import StateBackend


class State:
    """Layered state management with checkpoint support.
    
    State is NOT persisted on every set() call. Instead:
    - set() writes to in-memory buffer
    - checkpoint() persists buffer to backend
    - restore() loads from backend
    
    This allows efficient batching and recovery from interrupts.
    
    Example:
        state = State(backend, session_id)
        await state.restore()  # Load existing state
        
        state.set("vars.user_name", "高鑫")
        state.set("workflow.node1_output", result)
        
        await state.checkpoint()  # Persist changes
    """
    
    def __init__(
        self,
        backend: "StateBackend",
        session_id: str,
        *,
        initial_data: dict[str, Any] | None = None,
    ):
        """Initialize state.
        
        Args:
            backend: Storage backend for persistence
            session_id: Session identifier (used as storage key)
            initial_data: Optional initial state data
        """
        self._backend = backend
        self._session_id = session_id
        self._data: dict[str, Any] = initial_data or {
            "vars": {},
            "workflow": {},
            "agent": {},
        }
        self._dirty = False
    
    # ========== Partition Access ==========
    
    @property
    def vars(self) -> dict[str, Any]:
        """Developer variables (for prompt formatting).
        
        Example:
            prompt = template.format(**state.vars)
        """
        if "vars" not in self._data:
            self._data["vars"] = {}
        return self._data["vars"]
    
    @property
    def workflow(self) -> dict[str, Any]:
        """Workflow node outputs.
        
        Example:
            result = state.workflow["node1_output"]
        """
        if "workflow" not in self._data:
            self._data["workflow"] = {}
        return self._data["workflow"]
    
    @property
    def agent(self) -> dict[str, Any]:
        """Agent internal state.
        
        Example:
            turn = state.agent.get("turn_count", 0)
        """
        if "agent" not in self._data:
            self._data["agent"] = {}
        return self._data["agent"]
    
    # ========== Path Operations ==========
    
    def get(self, path: str, default: Any = None) -> Any:
        """Get value by path.
        
        Args:
            path: Dot-separated path (e.g., "vars.user_name")
            default: Default value if path not found
            
        Returns:
            Value at path, or default
            
        Example:
            state.get("vars.user_name")     # → "高鑫"
            state.get("workflow.node1")     # → {...}
            state.get("agent.missing", 0)   # → 0
        """
        parts = path.split(".")
        current = self._data
        
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default
        
        return current
    
    def set(self, path: str, value: Any) -> None:
        """Set value by path (writes to buffer, not persisted).
        
        Args:
            path: Dot-separated path (e.g., "vars.user_name")
            value: Value to set
            
        Example:
            state.set("vars.user_name", "高鑫")
            state.set("workflow.node1_output", result)
        """
        parts = path.split(".")
        current = self._data
        
        # Navigate to parent, creating dicts as needed
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        # Set value
        current[parts[-1]] = value
        self._dirty = True
    
    def delete(self, path: str) -> bool:
        """Delete value by path.
        
        Args:
            path: Dot-separated path
            
        Returns:
            True if deleted, False if not found
        """
        parts = path.split(".")
        current = self._data
        
        # Navigate to parent
        for part in parts[:-1]:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return False
        
        # Delete
        if isinstance(current, dict) and parts[-1] in current:
            del current[parts[-1]]
            self._dirty = True
            return True
        
        return False
    
    def match(self, pattern: str) -> dict[str, Any]:
        """Get values matching prefix pattern.
        
        Args:
            pattern: Prefix pattern ending with '*' (e.g., "workflow.*")
            
        Returns:
            Dict of matching key-value pairs (keys without prefix)
            
        Example:
            state.match("workflow.*")  # → {"node1_output": ..., "node2_output": ...}
            state.match("vars.*")      # → {"user_name": ..., "project_name": ...}
        """
        if not pattern.endswith("*"):
            # Exact match, return single value wrapped
            val = self.get(pattern)
            return {pattern.split(".")[-1]: val} if val is not None else {}
        
        # Prefix match
        prefix = pattern[:-1]  # Remove '*'
        if prefix.endswith("."):
            prefix = prefix[:-1]  # Remove trailing '.'
        
        parent = self.get(prefix)
        if isinstance(parent, dict):
            return parent.copy()
        
        return {}
    
    def has(self, path: str) -> bool:
        """Check if path exists.
        
        Args:
            path: Dot-separated path
            
        Returns:
            True if path exists
        """
        return self.get(path) is not None
    
    def clear(self, partition: str | None = None) -> None:
        """Clear state.
        
        Args:
            partition: If provided, clear only that partition.
                       If None, clear all partitions.
        """
        if partition:
            if partition in self._data:
                self._data[partition] = {}
                self._dirty = True
        else:
            self._data = {
                "vars": {},
                "workflow": {},
                "agent": {},
            }
            self._dirty = True
    
    # ========== Persistence ==========
    
    @property
    def is_dirty(self) -> bool:
        """Check if state has unsaved changes."""
        return self._dirty
    
    async def checkpoint(self) -> None:
        """Persist current state to backend.
        
        Call at key points:
        - After step completion
        - After tool execution
        - Before HITL suspend
        """
        if not self._dirty:
            return
        
        await self._backend.set("state", self._session_id, self._data)
        self._dirty = False
    
    async def restore(self) -> bool:
        """Restore state from backend.
        
        Returns:
            True if state was restored, False if no saved state
        """
        data = await self._backend.get("state", self._session_id)
        if data:
            self._data = data
            # Ensure all partitions exist
            for key in ("vars", "workflow", "agent"):
                if key not in self._data:
                    self._data[key] = {}
            self._dirty = False
            return True
        return False
    
    # ========== Utility ==========
    
    def to_dict(self) -> dict[str, Any]:
        """Export state as dict."""
        return self._data.copy()
    
    def update(self, data: dict[str, Any]) -> None:
        """Bulk update state.
        
        Args:
            data: Dict with partition keys (vars, workflow, agent)
        """
        for key in ("vars", "workflow", "agent"):
            if key in data:
                self._data[key].update(data[key])
                self._dirty = True
    
    def __repr__(self) -> str:
        dirty_marker = " (dirty)" if self._dirty else ""
        return f"<State session={self._session_id}{dirty_marker}>"


# Convenience type for state isolation in SubAgents
class StateSnapshot:
    """Immutable snapshot of state for isolation."""
    
    def __init__(self, data: dict[str, Any]):
        self._data = data
    
    @property
    def vars(self) -> dict[str, Any]:
        return self._data.get("vars", {}).copy()
    
    @property
    def workflow(self) -> dict[str, Any]:
        return self._data.get("workflow", {}).copy()
    
    @property
    def agent(self) -> dict[str, Any]:
        return self._data.get("agent", {}).copy()
    
    def get(self, path: str, default: Any = None) -> Any:
        parts = path.split(".")
        current = self._data
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default
        return current
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "vars": self.vars,
            "workflow": self.workflow,
            "agent": self.agent,
        }


__all__ = ["State", "StateSnapshot"]
