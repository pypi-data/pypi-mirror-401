"""Agent tools for plan orchestration.

These tools are provided to the Claude Code agent to allow it to:
- Execute tasks (spawn child agent workflows)
- Check task status
- Validate task completion
- Update plan state
"""

from typing import Dict, Any, Optional
import structlog
from anthropic import BaseModel as AnthropicBaseModel

from worker_internal.planner.models import (
    PlanTask,
    TaskStatus,
    TaskExecutionResult,
    AgentToolContext,
)

logger = structlog.get_logger()


class ExecuteTaskTool(AnthropicBaseModel):
    """Tool for executing tasks from the plan."""

    name: str = "execute_task"
    description: str = """Execute one or more tasks from the plan.

    For independent tasks (no dependencies), you can execute multiple tasks IN PARALLEL
    by providing task_ids array instead of single task_id. This is much faster!

    This will:
    1. Create enriched prompts with task details
    2. Spawn agent execution workflows (in parallel if multiple tasks)
    3. Return execution results

    Args:
        task_id: Single task ID to execute (optional if task_ids provided)
        task_ids: Array of task IDs to execute in parallel (optional if task_id provided)

    Returns:
        Dictionary with execution results

    Examples:
        execute_task(task_id=1)  # Execute task 1
        execute_task(task_ids=[1, 2, 3])  # Execute tasks 1, 2, 3 in parallel
    """

    input_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "task_id": {
                "type": "integer",
                "description": "Single task ID to execute"
            },
            "task_ids": {
                "type": "array",
                "items": {"type": "integer"},
                "description": "Array of task IDs to execute in parallel (for independent tasks)"
            }
        }
    }


class GetTaskStatusTool(AnthropicBaseModel):
    """Tool for checking task execution status."""

    name: str = "get_task_status"
    description: str = """Check the current status of a task execution.

    Returns the execution status, output, and metadata for a task.

    Args:
        task_id: The ID of the task to check

    Returns:
        Dictionary with status, output, tokens, and other metadata
    """

    input_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "task_id": {
                "type": "integer",
                "description": "The ID of the task to check status for"
            }
        },
        "required": ["task_id"]
    }


class ValidateTaskTool(AnthropicBaseModel):
    """Tool for validating task completion."""

    name: str = "validate_task"
    description: str = """Validate that a task completed successfully using LLM analysis.

    This analyzes the task output and conversation to determine if:
    - The task completed as expected (success)
    - The task failed or produced incorrect output (failed)
    - The task needs more work (pending)

    Args:
        task_id: The ID of the task to validate

    Returns:
        Dictionary with validation status, reason, and confidence score
    """

    input_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "task_id": {
                "type": "integer",
                "description": "The ID of the task to validate"
            }
        },
        "required": ["task_id"]
    }


class UpdatePlanStatusTool(AnthropicBaseModel):
    """Tool for updating overall plan status."""

    name: str = "update_plan_status"
    description: str = """Update the overall plan execution status and progress.

    Use this to provide status updates as you progress through the plan.
    This will publish events to the UI for real-time updates.

    Args:
        status_message: Human-readable status message
        completed_tasks: Number of tasks completed so far

    Returns:
        Success confirmation
    """

    input_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "status_message": {
                "type": "string",
                "description": "Human-readable status update message"
            },
            "completed_tasks": {
                "type": "integer",
                "description": "Number of tasks completed so far"
            }
        },
        "required": ["status_message"]
    }


class ListTasksTool(AnthropicBaseModel):
    """Tool for listing all tasks in the plan."""

    name: str = "list_tasks"
    description: str = """Get a list of all tasks in the plan with their dependencies.

    Use this to understand the plan structure and task relationships.

    Returns:
        List of tasks with their IDs, titles, dependencies, and status
    """

    input_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {},
        "required": []
    }


def get_agent_tools() -> list:
    """Get all tools available to the orchestrator agent."""
    return [
        ExecuteTaskTool(),
        GetTaskStatusTool(),
        ValidateTaskTool(),
        UpdatePlanStatusTool(),
        ListTasksTool(),
    ]


def format_tool_for_anthropic(tool: AnthropicBaseModel) -> Dict[str, Any]:
    """Format a tool definition for Anthropic API."""
    return {
        "name": tool.name,
        "description": tool.description,
        "input_schema": tool.input_schema,
    }


def get_agent_tools_formatted() -> list:
    """Get all tools formatted for Anthropic API."""
    return [format_tool_for_anthropic(tool) for tool in get_agent_tools()]
