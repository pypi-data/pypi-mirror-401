"""Centralized logging for aury-agents.

Uses standard logging. In applications using foundation-kit,
loguru will intercept these logs and add trace_id automatically.

Usage:
    from aury.agents.core.logging import get_logger
    
    logger = get_logger("react")  # -> "aury.agents.react"
    logger.info("Starting agent", extra={"session_id": "..."})

Pre-defined loggers:
    - root: aury.agents (framework root)
    - react: aury.agents.react
    - workflow: aury.agents.workflow
    - memory: aury.agents.memory
    - tool: aury.agents.tool
    - middleware: aury.agents.middleware
    - bus: aury.agents.bus
    - storage: aury.agents.storage
    - session: aury.agents.session
"""
import logging
from typing import Literal

# Root namespace
ROOT_NAMESPACE = "aury.agents"

# Pre-defined sub-loggers
_LOGGERS: dict[str, logging.Logger] = {}


def get_logger(name: str | None = None) -> logging.Logger:
    """Get a logger for the given component.
    
    Args:
        name: Component name (e.g., "react", "workflow").
              If None, returns root logger.
              
    Returns:
        Logger instance for aury.agents.{name}
    """
    if name is None:
        full_name = ROOT_NAMESPACE
    else:
        full_name = f"{ROOT_NAMESPACE}.{name}"
    
    if full_name not in _LOGGERS:
        _LOGGERS[full_name] = logging.getLogger(full_name)
    
    return _LOGGERS[full_name]


# Pre-instantiated loggers for common components
logger = get_logger()  # Root logger
react_logger = get_logger("react")
workflow_logger = get_logger("workflow")
memory_logger = get_logger("memory")
tool_logger = get_logger("tool")
middleware_logger = get_logger("middleware")
bus_logger = get_logger("bus")
storage_logger = get_logger("storage")
session_logger = get_logger("session")
context_logger = get_logger("context")


# Convenience type for IDE completion
LoggerName = Literal[
    "react",
    "workflow", 
    "memory",
    "tool",
    "middleware",
    "bus",
    "storage",
    "session",
    "context",
]


__all__ = [
    "get_logger",
    "logger",
    "react_logger",
    "workflow_logger",
    "memory_logger",
    "tool_logger",
    "middleware_logger",
    "bus_logger",
    "storage_logger",
    "session_logger",
    "context_logger",
    "LoggerName",
    "ROOT_NAMESPACE",
]
