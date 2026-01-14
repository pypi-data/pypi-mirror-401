"""EditTool - Edit file contents."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

from ...core.types.tool import BaseTool, ToolContext, ToolResult


class EditTool(BaseTool):
    """Edit file contents with multiple modes."""
    
    _name = "edit"
    _description = "Edit file contents (overwrite, append, or insert at line)"
    _parameters = {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Path to the file to edit",
            },
            "content": {
                "type": "string",
                "description": "Content to write",
            },
            "mode": {
                "type": "string",
                "enum": ["overwrite", "append", "insert"],
                "description": "Edit mode: overwrite (replace), append (add to end), insert (at line)",
                "default": "overwrite",
            },
            "line": {
                "type": "integer",
                "description": "Line number for insert mode (1-indexed)",
            },
            "encoding": {
                "type": "string",
                "description": "File encoding (default: utf-8)",
                "default": "utf-8",
            },
            "create_dirs": {
                "type": "boolean",
                "description": "Create parent directories if needed",
                "default": True,
            },
        },
        "required": ["path", "content"],
    }
    
    def __init__(self, allowed_paths: list[str] | None = None):
        """Initialize EditTool.
        
        Args:
            allowed_paths: List of allowed path prefixes (None = allow all)
        """
        self._allowed_paths = allowed_paths
    
    async def execute(self, params: dict[str, Any], ctx: ToolContext) -> ToolResult:
        file_path = params.get("path", "")
        content = params.get("content", "")
        mode = params.get("mode", "overwrite")
        line = params.get("line")
        encoding = params.get("encoding", "utf-8")
        create_dirs = params.get("create_dirs", True)
        
        if not file_path:
            return ToolResult.error("Path is required")
        
        path = Path(file_path).expanduser().resolve()
        
        # Security check
        if self._allowed_paths:
            if not any(str(path).startswith(p) for p in self._allowed_paths):
                return ToolResult.error(f"Path not allowed: {path}")
        
        try:
            # Create parent directories
            if create_dirs and not path.parent.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
            
            if mode == "overwrite":
                path.write_text(content, encoding=encoding)
                return ToolResult(output=f"File written ({len(content)} chars)")
            
            elif mode == "append":
                existing = path.read_text(encoding=encoding) if path.exists() else ""
                path.write_text(existing + content, encoding=encoding)
                return ToolResult(output=f"Content appended ({len(content)} chars)")
            
            elif mode == "insert":
                if line is None:
                    return ToolResult.error("Line number required for insert mode")
                
                if path.exists():
                    lines = path.read_text(encoding=encoding).splitlines(keepends=True)
                else:
                    lines = []
                
                # Pad with empty lines if needed
                while len(lines) < line - 1:
                    lines.append("\n")
                
                # Insert at position
                insert_idx = max(0, line - 1)
                content_lines = content.splitlines(keepends=True)
                if content_lines and not content_lines[-1].endswith("\n"):
                    content_lines[-1] += "\n"
                
                new_lines = lines[:insert_idx] + content_lines + lines[insert_idx:]
                path.write_text("".join(new_lines), encoding=encoding)
                
                return ToolResult(output=f"Content inserted at line {line} ({len(content_lines)} lines)")
            
            else:
                return ToolResult.error(f"Unknown mode: {mode}")
            
        except Exception as e:
            return ToolResult.error(str(e))


__all__ = ["EditTool"]
