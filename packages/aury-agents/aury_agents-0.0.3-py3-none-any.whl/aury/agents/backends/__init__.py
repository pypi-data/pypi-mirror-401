"""Backend protocols and implementations.

Backends provide abstracted interfaces for various capabilities:
- StateBackend: Framework internal state storage
- SnapshotBackend: File state tracking and revert
- ShellBackend: Shell command execution
- FileBackend: File system operations
- CodeBackend: Code execution
- SubAgentBackend: Sub-agent registry and retrieval
"""
from .state import StateBackend, SQLiteStateBackend, MemoryStateBackend, FileStateBackend, CompositeStateBackend
from .snapshot import SnapshotBackend, Patch, InMemorySnapshotBackend, GitSnapshotBackend, GitS3HybridBackend
from .shell import ShellBackend, ShellResult, LocalShellBackend
from .file import FileBackend, LocalFileBackend
from .code import CodeBackend, CodeResult
from .subagent import SubAgentBackend, AgentConfig, ListSubAgentBackend
from .sandbox import SandboxShellBackend, SandboxCodeBackend

__all__ = [
    # State
    "StateBackend",
    "SQLiteStateBackend",  # Default
    "MemoryStateBackend",
    "FileStateBackend",
    "CompositeStateBackend",
    # Snapshot
    "SnapshotBackend",
    "Patch",
    "InMemorySnapshotBackend",
    "GitSnapshotBackend",
    "GitS3HybridBackend",
    # Shell
    "ShellBackend",
    "ShellResult",
    "LocalShellBackend",
    # File
    "FileBackend",
    "LocalFileBackend",
    # Code
    "CodeBackend",
    "CodeResult",
    # SubAgent
    "SubAgentBackend",
    "AgentConfig",
    "ListSubAgentBackend",
    # Sandbox backends
    "SandboxShellBackend",
    "SandboxCodeBackend",
]
