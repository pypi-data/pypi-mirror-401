"""LLM Provider adapter using aury-ai-model ModelClient."""
from __future__ import annotations

import json
from typing import Any, AsyncIterator

from .provider import (
    LLMProvider,
    LLMEvent,
    LLMMessage,
    ToolCall,
    ToolDefinition,
    Usage,
)

# Import from aury-ai-model
try:
    from aury.ai.model import (
        ModelClient,
        Message,
        StreamEvent,
        msg,
        Text,
        Evt,
        ToolCall as ModelToolCall,
        ToolSpec,
        FunctionToolSpec,
        ToolKind,
        StreamCollector,
    )
    HAS_MODEL_CLIENT = True
except ImportError:
    HAS_MODEL_CLIENT = False
    ModelClient = None  # type: ignore


class ModelClientProvider:
    """LLM Provider using aury-ai-model ModelClient.
    
    This adapter bridges the framework's LLMProvider protocol with
    the aury-ai-model ModelClient.
    
    Example:
        >>> provider = ModelClientProvider(
        ...     provider="openai",
        ...     model="gpt-4o",
        ... )
        >>> async for event in provider.complete(messages):
        ...     print(event)
    """
    
    def __init__(
        self,
        provider: str,
        model: str,
        api_key: str | None = None,
        base_url: str | None = None,
        **kwargs: Any,
    ):
        """Initialize ModelClient provider.
        
        Args:
            provider: Provider name (openai, anthropic, doubao, etc.)
            model: Model name
            api_key: API key (optional, uses env if not provided)
            base_url: Base URL override
            **kwargs: Additional ModelClient options
        """
        if not HAS_MODEL_CLIENT:
            raise ImportError(
                "aury-ai-model is not installed. "
                "Please install it: pip install aury-ai-model[all]"
            )
        
        self._provider_name = provider
        self._model_name = model
        
        # Build ModelClient
        client_kwargs = {
            "provider": provider,
            "model": model,
        }
        if api_key:
            client_kwargs["api_key"] = api_key
        if base_url:
            client_kwargs["base_url"] = base_url
        
        # Pass through additional options
        for key in ("default_max_tokens", "default_temperature", "default_top_p"):
            if key in kwargs:
                client_kwargs[key] = kwargs[key]
        
        self._client = ModelClient(**client_kwargs)
        self._extra_kwargs = {
            k: v for k, v in kwargs.items()
            if k not in client_kwargs
        }
        self._call_count = 0
    
    @property
    def provider(self) -> str:
        return self._provider_name
    
    @property
    def model(self) -> str:
        return self._model_name
    
    @property
    def call_count(self) -> int:
        """Get number of LLM calls made."""
        return self._call_count
    
    def _convert_messages(self, messages: list[LLMMessage]) -> list[Message]:
        """Convert LLMMessage to aury-ai-model Message.
        
        Supports all message types from aury.ai.model:
        - system: msg.system(text)
        - user: msg.user(text, images=[])
        - assistant: msg.assistant(text, tool_calls=[])
        - tool: msg.tool(result, tool_call_id)
        """
        result = []
        
        for m in messages:
            if m.role == "system":
                result.append(msg.system(
                    m.content if isinstance(m.content, str) else str(m.content)
                ))
            
            elif m.role == "user":
                if isinstance(m.content, str):
                    result.append(msg.user(m.content))
                else:
                    # Handle multipart content (text + images)
                    text_parts = []
                    images = []
                    for part in m.content:
                        if isinstance(part, dict):
                            if part.get("type") == "text":
                                text_parts.append(part.get("text", ""))
                            elif part.get("type") == "image_url":
                                url = part.get("image_url", {}).get("url", "")
                                if url:
                                    images.append(url)
                    result.append(msg.user(
                        text=" ".join(text_parts) if text_parts else None,
                        images=images if images else None,
                    ))
            
            elif m.role == "assistant":
                if isinstance(m.content, str):
                    result.append(msg.assistant(m.content))
                else:
                    # Handle tool calls in assistant message
                    text_parts = []
                    tool_calls = []
                    for part in m.content:
                        if isinstance(part, dict):
                            if part.get("type") == "text":
                                text_parts.append(part.get("text", ""))
                            elif part.get("type") == "tool_use":
                                tool_calls.append(ModelToolCall(
                                    id=part.get("id", ""),
                                    name=part.get("name", ""),
                                    arguments_json=json.dumps(part.get("input", {})),
                                ))
                    result.append(msg.assistant(
                        text=" ".join(text_parts) if text_parts else None,
                        tool_calls=tool_calls if tool_calls else None,
                    ))
            
            elif m.role == "tool":
                # Tool result message - two formats supported:
                # 1. Simple: LLMMessage(role="tool", content="result", tool_call_id="xxx")
                # 2. List format: content=[{"type": "tool_result", "content": "...", "tool_use_id": "..."}]
                if m.tool_call_id and isinstance(m.content, str):
                    # Simple format
                    result.append(msg.tool(
                        result=m.content,
                        tool_call_id=m.tool_call_id,
                    ))
                elif isinstance(m.content, list):
                    # List format (for compatibility)
                    for part in m.content:
                        if isinstance(part, dict) and part.get("type") == "tool_result":
                            result.append(msg.tool(
                                result=str(part.get("content", "")),
                                tool_call_id=part.get("tool_use_id", ""),
                            ))
        
        return result
    
    def _convert_tools(
        self,
        tools: list[ToolDefinition] | None,
    ) -> list[ToolSpec] | None:
        """Convert ToolDefinition to aury-ai-model ToolSpec."""
        if not tools:
            return None
        
        return [
            ToolSpec(
                kind=ToolKind.function,
                function=FunctionToolSpec(
                    name=tool.name,
                    description=tool.description,
                    parameters=tool.input_schema,
                ),
            )
            for tool in tools
        ]
    
    def _convert_stream_event(self, event: StreamEvent) -> LLMEvent | None:
        """Convert aury-ai-model StreamEvent to LLMEvent."""
        match event.type:
            case Evt.content:
                return LLMEvent(type="content", delta=event.delta)
            
            case Evt.thinking:
                return LLMEvent(type="thinking", delta=event.delta)
            
            case Evt.tool_call_start:
                if event.tool_call:
                    return LLMEvent(
                        type="tool_call_start",
                        tool_call=ToolCall(
                            id=event.tool_call.id,
                            name=event.tool_call.name,
                            arguments="",  # Empty at start
                        ),
                    )
            
            case Evt.tool_call_delta:
                if event.tool_call_delta:
                    return LLMEvent(
                        type="tool_call_delta",
                        tool_call_delta=event.tool_call_delta,
                    )
            
            case Evt.tool_call_progress:
                if event.tool_call_progress:
                    return LLMEvent(
                        type="tool_call_progress",
                        tool_call_progress=event.tool_call_progress,
                    )
            
            case Evt.tool_call:
                if event.tool_call:
                    return LLMEvent(
                        type="tool_call",
                        tool_call=ToolCall(
                            id=event.tool_call.id,
                            name=event.tool_call.name,
                            arguments=event.tool_call.arguments_json,
                        ),
                    )
            
            case Evt.usage:
                if event.usage:
                    return LLMEvent(
                        type="usage",
                        usage=Usage(
                            input_tokens=event.usage.input_tokens,
                            output_tokens=event.usage.output_tokens,
                            cache_read_tokens=getattr(event.usage, 'cache_read_tokens', 0),
                            cache_write_tokens=getattr(event.usage, 'cache_write_tokens', 0),
                            reasoning_tokens=getattr(event.usage, 'reasoning_tokens', 0),
                        ),
                    )
            
            case Evt.completed:
                return LLMEvent(type="completed", finish_reason="end_turn")
            
            case Evt.error:
                return LLMEvent(type="error", error=event.error)
        
        return None
    
    async def complete(
        self,
        messages: list[LLMMessage],
        tools: list[ToolDefinition] | None = None,
        enable_thinking: bool = False,
        reasoning_effort: str | None = None,
        **kwargs: Any,
    ) -> AsyncIterator[LLMEvent]:
        """Generate completion with streaming.
        
        Streaming is enabled by default - this method uses ModelClient.astream()
        which always streams responses incrementally.
        
        Args:
            messages: Conversation messages
            tools: Available tools
            enable_thinking: Whether to request thinking output
            reasoning_effort: Reasoning effort level ("low", "medium", "high", "max", "auto")
            **kwargs: Additional parameters (temperature, max_tokens, etc.)
        
        Yields:
            LLMEvent: Streaming events (content, thinking, tool_call, usage, completed, error)
        """
        # Convert messages and tools
        model_messages = self._convert_messages(messages)
        model_tools = self._convert_tools(tools)
        
        # Merge kwargs
        call_kwargs = {**self._extra_kwargs, **kwargs}
        if model_tools:
            call_kwargs["tools"] = model_tools
        
        # Add thinking configuration (for models that support it)
        if enable_thinking:
            call_kwargs["return_thinking"] = True
            if reasoning_effort:
                call_kwargs["reasoning_effort"] = reasoning_effort
        
        # Increment call count
        self._call_count += 1
        
        # Remove stream from kwargs if present (astream always streams, doesn't accept stream param)
        call_kwargs.pop('stream', None)
        
        # Ensure usage events are yielded (for statistics tracking)
        # This ensures usage events are included in the stream
        yield_usage_event = call_kwargs.pop('yield_usage_event', True)
        
        # Stream from ModelClient with retry support
        # astream() always streams incrementally - events arrive as they're generated
        async for event in self._client.with_retry(
            max_attempts=3,
            base_delay=1.0,
            max_delay=10.0,
        ).astream(
            model_messages,
            yield_usage_event=yield_usage_event,
            **call_kwargs
        ):
            converted = self._convert_stream_event(event)
            if converted:
                yield converted


def create_provider(
    provider: str,
    model: str,
    **kwargs: Any,
) -> LLMProvider:
    """Create an LLM provider.
    
    Args:
        provider: Provider name (openai, anthropic, doubao, etc.)
        model: Model name
        **kwargs: Additional options
    
    Returns:
        LLMProvider instance
    """
    return ModelClientProvider(provider=provider, model=model, **kwargs)
