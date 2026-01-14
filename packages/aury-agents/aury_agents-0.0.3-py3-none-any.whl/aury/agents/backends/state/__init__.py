"""State backend for framework internal storage.

Used for storing session state, plan data, invocation records, messages, etc.
This is NOT for user file operations - use FileBackend for that.

Default: SQLiteStateBackend (local persistence)
"""
from .types import StateBackend
from .sqlite import SQLiteStateBackend
from .memory import MemoryStateBackend
from .file import FileStateBackend
from .composite import CompositeStateBackend

__all__ = [
    "StateBackend",
    "SQLiteStateBackend",  # Default
    "MemoryStateBackend",  # For testing
    "FileStateBackend",
    "CompositeStateBackend",
]
