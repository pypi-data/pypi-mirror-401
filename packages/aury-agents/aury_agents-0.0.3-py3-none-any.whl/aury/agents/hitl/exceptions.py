"""HITL (Human-in-the-Loop) exceptions.

These exceptions control agent execution flow when human input is needed.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class HITLSuspendError(Exception):
    """Raised to suspend agent execution and wait for human input.
    
    When this exception is raised:
    1. Current state is checkpointed
    2. Invocation status becomes SUSPENDED
    3. Frontend is notified via BlockEvent
    4. Agent loop exits, waiting for user response
    
    The agent can be resumed by:
    - Calling respond(request_id, response)
    - Or calling run() with user input (auto-detects suspended state)
    """
    
    def __init__(
        self,
        request_id: str,
        request_type: str = "ask_user",
        metadata: dict[str, Any] | None = None,
    ):
        """Initialize HITL suspend error.
        
        Args:
            request_id: Unique ID for this request (used to match response)
            request_type: Type of request (ask_user, confirm, choice, etc.)
            metadata: Arbitrary data for this request (question, choices, context, etc.)
        """
        self.request_id = request_id
        self.request_type = request_type
        self.metadata = metadata or {}
        
        super().__init__(f"HITL suspend: {request_type} ({request_id})")
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for storage/transmission."""
        return {
            "request_id": self.request_id,
            "request_type": self.request_type,
            **self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "HITLSuspendError":
        """Create from dictionary."""
        request_id = data.pop("request_id")
        request_type = data.pop("request_type", "ask_user")
        return cls(
            request_id=request_id,
            request_type=request_type,
            metadata=data,
        )


class HITLTimeoutError(Exception):
    """Raised when HITL request times out."""
    
    def __init__(self, request_id: str, timeout: float):
        self.request_id = request_id
        self.timeout = timeout
        super().__init__(f"HITL request {request_id} timed out after {timeout}s")


class HITLCancelledError(Exception):
    """Raised when HITL request is cancelled."""
    
    def __init__(self, request_id: str, reason: str = "cancelled"):
        self.request_id = request_id
        self.reason = reason
        super().__init__(f"HITL request {request_id} cancelled: {reason}")


@dataclass
class HITLRequest:
    """A pending HITL request.
    
    Stored in invocation for persistence.
    """
    request_id: str
    request_type: str  # ask_user, permission, form, workflow_human
    
    # Display
    message: str | None = None
    options: list[str] | None = None
    
    # Context
    tool_name: str | None = None  # If triggered by tool
    node_id: str | None = None    # If triggered by workflow node
    
    # Metadata
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "request_id": self.request_id,
            "request_type": self.request_type,
            "message": self.message,
            "options": self.options,
            "tool_name": self.tool_name,
            "node_id": self.node_id,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "HITLRequest":
        """Create from dictionary."""
        return cls(
            request_id=data["request_id"],
            request_type=data.get("request_type", "ask_user"),
            message=data.get("message"),
            options=data.get("options"),
            tool_name=data.get("tool_name"),
            node_id=data.get("node_id"),
            metadata=data.get("metadata", {}),
        )


__all__ = [
    "HITLSuspendError",
    "HITLTimeoutError",
    "HITLCancelledError",
    "HITLRequest",
]
