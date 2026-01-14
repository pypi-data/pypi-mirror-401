"""Expression evaluator for workflow DSL."""
from __future__ import annotations

import re
from typing import Any


class ExpressionError(Exception):
    """Expression evaluation error."""
    pass


class ExpressionEvaluator:
    """Expression evaluator for ${{ ... }} syntax."""
    
    EXPR_PATTERN = re.compile(r'\$\{\{\s*(.+?)\s*\}\}')
    
    def evaluate(
        self,
        expression: str,
        context: dict[str, Any],
    ) -> Any:
        """Evaluate expression.
        
        Supports:
        - Full expressions: ${{ inputs.name }}
        - Template strings: "Hello ${{ inputs.name }}!"
        - Comparisons: ${{ inputs.count > 10 }}
        """
        if expression.startswith("${{") and expression.endswith("}}"):
            inner = expression[3:-2].strip()
            return self._eval_inner(inner, context)
        
        def replace(match: re.Match) -> str:
            inner = match.group(1)
            result = self._eval_inner(inner, context)
            return str(result) if result is not None else ""
        
        return self.EXPR_PATTERN.sub(replace, expression)
    
    def _eval_inner(self, expr: str, context: dict[str, Any]) -> Any:
        """Evaluate inner expression."""
        safe_context = {
            "inputs": context.get("inputs", {}),
            "state": context.get("state", {}),
            "true": True,
            "false": False,
            "null": None,
            "True": True,
            "False": False,
            "None": None,
        }
        
        # Add extra context variables
        for key, value in context.items():
            if key not in ("inputs", "state"):
                safe_context[key] = value
        
        try:
            return eval(expr, {"__builtins__": {}}, safe_context)
        except Exception as e:
            raise ExpressionError(f"Failed to evaluate: {expr}") from e
    
    def evaluate_condition(self, expr: str | None, context: dict[str, Any]) -> bool:
        """Evaluate condition expression."""
        if not expr:
            return True
        result = self.evaluate(expr, context)
        return bool(result)
    
    def has_expression(self, value: str) -> bool:
        """Check if string contains expression."""
        if not isinstance(value, str):
            return False
        return bool(self.EXPR_PATTERN.search(value))
    
    def resolve_inputs(
        self,
        inputs: dict[str, Any],
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """Resolve all expressions in inputs dict."""
        resolved = {}
        
        for key, value in inputs.items():
            if isinstance(value, str) and self.has_expression(value):
                resolved[key] = self.evaluate(value, context)
            elif isinstance(value, dict):
                resolved[key] = self.resolve_inputs(value, context)
            elif isinstance(value, list):
                resolved[key] = [
                    self.evaluate(v, context)
                    if isinstance(v, str) and self.has_expression(v)
                    else v
                    for v in value
                ]
            else:
                resolved[key] = value
        
        return resolved
