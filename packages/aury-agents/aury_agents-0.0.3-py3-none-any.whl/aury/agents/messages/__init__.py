"""Message system for conversation history.

Architecture:
- MessageStore: Storage layer (protocol + implementations)
- MessageManager: Service layer (save, get, truncation)
- MessageContextProvider: Provider layer (fetch context for Agent)
- Middleware: Hook layer (on_message_save triggers save)

Usage:
    # Create store and manager
    store = StateBackendMessageStore(backend)
    manager = MessageManager(store, max_turns=50)
    
    # Create provider (for context fetch)
    provider = MessageContextProvider(manager)
    
    # Create middleware (for save hook)
    middleware = MessagePersistenceMiddleware(manager)
    
    # Use in Agent
    agent = ReactAgent.create(
        llm=llm,
        context_providers=[provider],
        middleware=MiddlewareChain([middleware]),
    )
"""
from .types import (
    MessageRole,
    Message,
)
from .store import (
    MessageStore,
    StateBackendMessageStore,
    InMemoryMessageStore,
)
from .manager import (
    MessageManager,
)

__all__ = [
    # Types
    "MessageRole",
    "Message",
    # Store
    "MessageStore",
    "StateBackendMessageStore",
    "InMemoryMessageStore",
    # Manager
    "MessageManager",
]
