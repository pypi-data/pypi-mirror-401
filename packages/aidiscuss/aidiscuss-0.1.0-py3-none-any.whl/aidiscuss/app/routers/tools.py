"""
Tools router - API endpoints for tool management and execution
Phase 4: Tool Use
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from aidiscuss.app.services.tool_service import tool_service, ToolDefinition, ToolResult

router = APIRouter()


# Request/Response Models

class ToolExecuteRequest(BaseModel):
    """Request model for tool execution"""
    tool_name: str
    parameters: Dict[str, Any]
    agent_id: Optional[str] = None


class ToolDefinitionResponse(BaseModel):
    """Response model for tool definition"""
    name: str
    description: str
    parameters: List[Dict[str, Any]]
    category: str
    requires_approval: bool
    dangerous: bool


class ToolResultResponse(BaseModel):
    """Response model for tool execution result"""
    tool_name: str
    success: bool
    result: Any = None
    error: Optional[str] = None
    execution_time_ms: float
    metadata: Dict[str, Any]


class ToolUsageStatsResponse(BaseModel):
    """Response model for usage statistics"""
    total_calls: int
    success_rate: float
    average_time_ms: float
    by_tool: Optional[Dict[str, Dict]] = None


# Endpoints

@router.get("/tools", response_model=List[ToolDefinitionResponse])
async def list_tools(category: Optional[str] = None):
    """
    List all available tools

    Args:
        category: Optional category filter ("computation", "search", "data", "utility")

    Returns:
        List of tool definitions
    """
    try:
        tools = tool_service.list_tools(category=category)

        return [
            ToolDefinitionResponse(
                name=tool.name,
                description=tool.description,
                parameters=[
                    {
                        "name": param.name,
                        "type": param.type,
                        "description": param.description,
                        "required": param.required,
                        "default": param.default,
                        "enum": param.enum
                    }
                    for param in tool.parameters
                ],
                category=tool.category,
                requires_approval=tool.requires_approval,
                dangerous=tool.dangerous
            )
            for tool in tools
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing tools: {str(e)}")


@router.get("/tools/{tool_name}", response_model=ToolDefinitionResponse)
async def get_tool(tool_name: str):
    """
    Get specific tool definition

    Args:
        tool_name: Name of the tool

    Returns:
        Tool definition
    """
    try:
        tool = tool_service.get_tool(tool_name)

        if not tool:
            raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")

        definition = tool.get_definition()

        return ToolDefinitionResponse(
            name=definition.name,
            description=definition.description,
            parameters=[
                {
                    "name": param.name,
                    "type": param.type,
                    "description": param.description,
                    "required": param.required,
                    "default": param.default,
                    "enum": param.enum
                }
                for param in definition.parameters
            ],
            category=definition.category,
            requires_approval=definition.requires_approval,
            dangerous=definition.dangerous
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving tool: {str(e)}")


@router.post("/tools/execute", response_model=ToolResultResponse)
async def execute_tool(request: ToolExecuteRequest):
    """
    Execute a tool with given parameters

    Args:
        request: Tool execution request with tool_name, parameters, and optional agent_id

    Returns:
        Tool execution result
    """
    try:
        result = await tool_service.execute_tool(
            tool_name=request.tool_name,
            parameters=request.parameters,
            agent_id=request.agent_id
        )

        return ToolResultResponse(
            tool_name=result.tool_name,
            success=result.success,
            result=result.result,
            error=result.error,
            execution_time_ms=result.execution_time_ms,
            metadata=result.metadata
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing tool: {str(e)}")


@router.get("/tools/stats/usage", response_model=ToolUsageStatsResponse)
async def get_usage_stats(tool_name: Optional[str] = None):
    """
    Get tool usage statistics

    Args:
        tool_name: Optional tool name to filter stats

    Returns:
        Usage statistics
    """
    try:
        stats = tool_service.get_usage_stats(tool_name=tool_name)

        return ToolUsageStatsResponse(**stats)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving stats: {str(e)}")


@router.get("/tools/llm-format")
async def get_tools_for_llm():
    """
    Get tool definitions in LLM-compatible format (OpenAI function calling)

    This endpoint returns tools in the format expected by LLMs that support
    function calling (e.g., OpenAI, Anthropic Claude)

    Returns:
        List of tool schemas in OpenAI function calling format
    """
    try:
        tools = tool_service.get_tools_for_llm()
        return tools

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error formatting tools: {str(e)}")
