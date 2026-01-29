"""
Tool Service - Phase 4
Framework for agent tool use with built-in tools and plugin architecture
"""

import asyncio
import json
from typing import List, Dict, Any, Callable, Optional
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from datetime import datetime
import re


class ToolParameter(BaseModel):
    """Parameter definition for a tool"""
    name: str
    type: str  # "string", "number", "boolean", "object", "array"
    description: str
    required: bool = True
    default: Any = None
    enum: Optional[List[Any]] = None


class ToolDefinition(BaseModel):
    """Definition of a tool that agents can use"""
    name: str
    description: str
    parameters: List[ToolParameter]
    category: str = "general"  # "computation", "search", "data", "utility"
    requires_approval: bool = False  # If True, requires user approval before execution
    dangerous: bool = False  # Mark potentially dangerous tools


class ToolResult(BaseModel):
    """Result from tool execution"""
    tool_name: str
    success: bool
    result: Any = None
    error: Optional[str] = None
    execution_time_ms: float = 0
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BaseTool(ABC):
    """Base class for all tools"""

    @abstractmethod
    def get_definition(self) -> ToolDefinition:
        """Return tool definition"""
        pass

    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """Execute the tool with given parameters"""
        pass

    def validate_parameters(self, params: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate parameters against tool definition"""
        definition = self.get_definition()

        # Check required parameters
        for param in definition.parameters:
            if param.required and param.name not in params:
                return False, f"Missing required parameter: {param.name}"

        # Check parameter types (basic validation)
        for param_name, param_value in params.items():
            param_def = next((p for p in definition.parameters if p.name == param_name), None)
            if not param_def:
                return False, f"Unknown parameter: {param_name}"

            # Type validation
            expected_type = param_def.type
            if expected_type == "string" and not isinstance(param_value, str):
                return False, f"Parameter {param_name} must be a string"
            elif expected_type == "number" and not isinstance(param_value, (int, float)):
                return False, f"Parameter {param_name} must be a number"
            elif expected_type == "boolean" and not isinstance(param_value, bool):
                return False, f"Parameter {param_name} must be a boolean"

            # Enum validation
            if param_def.enum and param_value not in param_def.enum:
                return False, f"Parameter {param_name} must be one of: {param_def.enum}"

        return True, None


# Built-in Tools

class CalculatorTool(BaseTool):
    """Safe mathematical calculator tool"""

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="calculator",
            description="Evaluate mathematical expressions safely. Supports +, -, *, /, **, %, parentheses, and common functions like sqrt, sin, cos, abs.",
            parameters=[
                ToolParameter(
                    name="expression",
                    type="string",
                    description="Mathematical expression to evaluate (e.g., '2 + 2', 'sqrt(16)', '(3 * 4) + 5')"
                )
            ],
            category="computation",
            requires_approval=False,
            dangerous=False
        )

    async def execute(self, expression: str) -> ToolResult:
        """Execute calculator with sandboxed evaluation"""
        start_time = datetime.now()

        try:
            # Validate expression (only allow safe characters)
            if not re.match(r'^[0-9+\-*/().\s%**sqrtincoabslog]+$', expression.lower()):
                raise ValueError("Expression contains invalid characters")

            # Safe evaluation using limited namespace
            import math
            safe_dict = {
                "sqrt": math.sqrt,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "abs": abs,
                "log": math.log,
                "log10": math.log10,
                "exp": math.exp,
                "pi": math.pi,
                "e": math.e,
            }

            result = eval(expression, {"__builtins__": {}}, safe_dict)

            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            return ToolResult(
                tool_name="calculator",
                success=True,
                result=result,
                execution_time_ms=execution_time,
                metadata={"expression": expression}
            )

        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            return ToolResult(
                tool_name="calculator",
                success=False,
                error=str(e),
                execution_time_ms=execution_time
            )


class ToolService:
    """
    Service for managing and executing agent tools

    Features:
    - Tool registration and discovery
    - Parameter validation
    - Sandboxed execution
    - Plugin architecture
    - Usage tracking
    """

    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
        self.usage_history: List[Dict[str, Any]] = []

        # Register built-in tools
        self._register_builtin_tools()

    def _register_builtin_tools(self):
        """Register all built-in tools"""
        builtin_tools = [
            CalculatorTool(),
        ]

        for tool in builtin_tools:
            self.register_tool(tool)

    def register_tool(self, tool: BaseTool):
        """Register a tool for use by agents"""
        definition = tool.get_definition()
        self.tools[definition.name] = tool
        print(f"Registered tool: {definition.name}")

    def unregister_tool(self, tool_name: str) -> bool:
        """Unregister a tool"""
        if tool_name in self.tools:
            del self.tools[tool_name]
            return True
        return False

    def get_tool(self, tool_name: str) -> Optional[BaseTool]:
        """Get tool by name"""
        return self.tools.get(tool_name)

    def list_tools(self, category: Optional[str] = None) -> List[ToolDefinition]:
        """List all available tools, optionally filtered by category"""
        definitions = [tool.get_definition() for tool in self.tools.values()]

        if category:
            definitions = [d for d in definitions if d.category == category]

        return definitions

    def get_tools_for_llm(self, enabled_tools: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Get tool definitions in LLM-compatible format (OpenAI function calling format)

        Args:
            enabled_tools: List of tool IDs to include (e.g., ['calculator'])
                          If None, returns all tools

        Returns list of tool schemas for LLM function calling
        """
        tools = []

        # Map tool IDs to tool names in the registry
        tool_id_mapping = {
            'calculator': 'calculator',
            'rag': None,  # RAG is handled separately, not a function call tool
        }

        for tool in self.tools.values():
            definition = tool.get_definition()

            # Filter by enabled tools if specified
            if enabled_tools is not None:
                # Check if this tool is in the enabled list
                tool_enabled = False
                for tool_id, tool_name in tool_id_mapping.items():
                    if tool_id in enabled_tools and (
                        definition.name == tool_name or
                        (tool_name and definition.name.startswith(tool_name))
                    ):
                        tool_enabled = True
                        break

                if not tool_enabled:
                    continue

            # Convert to OpenAI function calling format
            properties = {}
            required = []

            for param in definition.parameters:
                properties[param.name] = {
                    "type": param.type,
                    "description": param.description,
                }

                if param.enum:
                    properties[param.name]["enum"] = param.enum

                if param.required:
                    required.append(param.name)

            tools.append({
                "type": "function",
                "function": {
                    "name": definition.name,
                    "description": definition.description,
                    "parameters": {
                        "type": "object",
                        "properties": properties,
                        "required": required,
                    }
                }
            })

        return tools

    async def execute_tool(
        self,
        tool_name: str,
        parameters: Dict[str, Any],
        agent_id: Optional[str] = None
    ) -> ToolResult:
        """
        Execute a tool with given parameters

        Args:
            tool_name: Name of tool to execute
            parameters: Tool parameters
            agent_id: ID of agent executing tool (for tracking)

        Returns:
            ToolResult with execution outcome
        """
        tool = self.get_tool(tool_name)

        if not tool:
            return ToolResult(
                tool_name=tool_name,
                success=False,
                error=f"Tool '{tool_name}' not found"
            )

        # Validate parameters
        valid, error = tool.validate_parameters(parameters)
        if not valid:
            return ToolResult(
                tool_name=tool_name,
                success=False,
                error=f"Invalid parameters: {error}"
            )

        # Execute tool
        try:
            result = await tool.execute(**parameters)

            # Track usage
            self.usage_history.append({
                "tool_name": tool_name,
                "agent_id": agent_id,
                "parameters": parameters,
                "success": result.success,
                "timestamp": datetime.now().isoformat(),
                "execution_time_ms": result.execution_time_ms
            })

            return result

        except Exception as e:
            return ToolResult(
                tool_name=tool_name,
                success=False,
                error=f"Execution error: {str(e)}"
            )

    def get_usage_stats(self, tool_name: Optional[str] = None) -> Dict[str, Any]:
        """Get usage statistics for tools"""
        history = self.usage_history

        if tool_name:
            history = [h for h in history if h["tool_name"] == tool_name]

        if not history:
            return {"total_calls": 0, "success_rate": 0, "average_time_ms": 0}

        total = len(history)
        successes = sum(1 for h in history if h["success"])
        avg_time = sum(h["execution_time_ms"] for h in history) / total

        return {
            "total_calls": total,
            "success_rate": successes / total,
            "average_time_ms": avg_time,
            "by_tool": self._group_by_tool(history) if not tool_name else None
        }

    def _group_by_tool(self, history: List[Dict]) -> Dict[str, Dict]:
        """Group usage stats by tool"""
        by_tool = {}

        for entry in history:
            tool_name = entry["tool_name"]
            if tool_name not in by_tool:
                by_tool[tool_name] = []
            by_tool[tool_name].append(entry)

        return {
            tool_name: {
                "calls": len(entries),
                "success_rate": sum(1 for e in entries if e["success"]) / len(entries),
                "avg_time_ms": sum(e["execution_time_ms"] for e in entries) / len(entries)
            }
            for tool_name, entries in by_tool.items()
        }


# Singleton instance
tool_service = ToolService()
