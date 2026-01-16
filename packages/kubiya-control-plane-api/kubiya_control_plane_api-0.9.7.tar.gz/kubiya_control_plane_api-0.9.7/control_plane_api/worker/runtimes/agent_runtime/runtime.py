"""
Agent Runtime - Rust-based high-performance runtime integration.

This runtime communicates with the agent-runtime GRPC service (Rust) for
execution, providing high performance and multiple provisioning strategies.
"""

import grpc
import structlog
from typing import AsyncIterator, Dict, Any, Optional, Callable
import os
import json

from ..base import (
    BaseRuntime,
    RuntimeExecutionContext,
    RuntimeExecutionResult,
    RuntimeType,
    RuntimeCapabilities,
    RuntimeRegistry,
)

logger = structlog.get_logger(__name__)


@RuntimeRegistry.register(RuntimeType.AGENT_RUNTIME)
class AgentRuntimeRuntime(BaseRuntime):
    """
    Agent Runtime integration - connects to Rust-based agent-runtime via GRPC.

    Features:
    - High-performance Rust backend
    - Multiple provisioners (Local, Docker, Kubernetes)
    - Built-in state persistence
    - Session management
    - Hot-reload configuration
    """

    def __init__(self, control_plane_client, cancellation_manager, **kwargs):
        """
        Initialize Agent Runtime client.

        Args:
            control_plane_client: Control Plane API client
            cancellation_manager: Cancellation manager instance
            **kwargs: Additional configuration
        """
        super().__init__(control_plane_client, cancellation_manager, **kwargs)

        # Get agent-runtime GRPC address from environment
        self.agent_runtime_address = os.getenv(
            "AGENT_RUNTIME_ADDRESS",
            "localhost:50052"
        )

        # GRPC channel and stub (lazy initialized)
        self._channel = None
        self._stub = None

        logger.info(
            "initialized_agent_runtime",
            address=self.agent_runtime_address,
        )

    def get_runtime_type(self) -> RuntimeType:
        """Return RuntimeType.AGENT_RUNTIME."""
        return RuntimeType.AGENT_RUNTIME

    def get_capabilities(self) -> RuntimeCapabilities:
        """Return Agent Runtime capabilities."""
        return RuntimeCapabilities(
            streaming=True,
            tools=True,
            mcp=True,
            hooks=True,
            cancellation=True,
            conversation_history=True,
            custom_tools=False,  # Custom tools handled by agent-runtime itself
        )

    def _get_stub(self):
        """Get or create GRPC stub (lazy initialization)."""
        if self._stub is None:
            self._channel = grpc.insecure_channel(self.agent_runtime_address)

            # Import generated proto files
            try:
                from generated.runtime.v1 import runtime_pb2, runtime_pb2_grpc
                self._stub = runtime_pb2_grpc.RuntimeServiceStub(self._channel)
                self._pb2 = runtime_pb2
                logger.info("grpc_stub_created", address=self.agent_runtime_address)
            except ImportError as e:
                logger.error(
                    "failed_to_import_grpc_stubs",
                    error=str(e),
                    hint="Run: python -m grpc_tools.protoc to generate stubs"
                )
                raise

        return self._stub

    def _build_execution_context(self, context: RuntimeExecutionContext):
        """Build GRPC ExecutionContext from RuntimeExecutionContext."""
        # Ensure stub is initialized first to get pb2
        self._get_stub()
        pb2 = self._pb2

        # Build base context
        grpc_context = pb2.ExecutionContext(
            agent_id=context.agent_id,
            organization_id=context.organization_id or "",
            prompt=context.prompt,
            system_prompt=context.system_prompt or "",
            model_id=context.model_id or "claude-sonnet-4",
            user_metadata=context.user_metadata or {},
        )

        # Add model_config if present
        if context.model_config:
            for key, value in context.model_config.items():
                grpc_context.model_config[key] = str(value)

        # Add conversation history if present
        if context.conversation_history:
            for msg in context.conversation_history:
                grpc_msg = pb2.ConversationMessage(
                    role=msg.get("role", "user"),
                    content=msg.get("content", ""),
                    timestamp=msg.get("timestamp", 0),
                )
                grpc_context.conversation_history.append(grpc_msg)

        # Add MCP servers if present
        if context.mcp_servers:
            for name, config in context.mcp_servers.items():
                mcp_server = pb2.MCPServer(
                    name=name,
                    command=config.get("command", ""),
                    args=config.get("args", []),
                    env=config.get("env", {}),
                )
                grpc_context.mcp_servers.append(mcp_server)

        # Add skills/tools if present
        if context.skills:
            for tool in context.skills:
                skill = pb2.Skill(
                    id=tool.get("id", ""),
                    name=tool.get("name", ""),
                    type=tool.get("type", ""),
                    config=tool.get("config", {}),
                )
                grpc_context.skills.append(skill)

        # ==================== NEW: Session Persistence Support ====================

        # Map session_id if present
        if context.session_id:
            grpc_context.session_id = context.session_id

        # Map full session messages (not just conversation_history)
        if context.session_messages:
            for msg in context.session_messages:
                session_msg = pb2.SessionMessage(
                    role=msg.get("role", "user"),
                    content=msg.get("content", ""),
                    timestamp=msg.get("timestamp", ""),
                    message_id=msg.get("message_id", ""),
                    user_id=msg.get("user_id", ""),
                    user_name=msg.get("user_name", ""),
                    user_email=msg.get("user_email", ""),
                    user_avatar=msg.get("user_avatar", ""),
                )
                # Map metadata if present
                if msg.get("metadata"):
                    for k, v in msg["metadata"].items():
                        session_msg.metadata[k] = str(v)
                grpc_context.session_messages.append(session_msg)

        # ==================== NEW: Native Sub-Agent Execution Support ====================

        # Map agents configuration for sub-agent execution
        if context.agents and context.enable_native_subagents:
            for agent_id, agent_def in context.agents.items():
                grpc_agent = grpc_context.agents[agent_id]  # Get the entry directly
                grpc_agent.agent_id = agent_id
                grpc_agent.description = agent_def.get("description", "")
                grpc_agent.prompt = agent_def.get("prompt", "")
                grpc_agent.tools.extend(agent_def.get("tools", []))
                grpc_agent.model = agent_def.get("model", "inherit")
                # Map optional config
                if agent_def.get("config"):
                    for k, v in agent_def["config"].items():
                        grpc_agent.config[k] = str(v)

        # ==================== NEW: Feature Flags ====================

        # Set feature flags
        grpc_context.enable_session_persistence = context.enable_session_persistence
        grpc_context.enable_native_subagents = context.enable_native_subagents

        return grpc_context

    async def _execute_impl(
        self, context: RuntimeExecutionContext
    ) -> RuntimeExecutionResult:
        """
        Core execution logic (non-streaming).

        For Agent Runtime, we collect all streaming chunks and return final result.
        """
        execution_id = context.execution_id

        logger.info(
            "executing_via_agent_runtime",
            execution_id=execution_id,
            agent_id=context.agent_id,
            address=self.agent_runtime_address,
        )

        try:
            stub = self._get_stub()
            pb2 = self._pb2

            # Build request
            grpc_context = self._build_execution_context(context)
            request = pb2.ExecuteRequest(
                execution_id=execution_id,
                runtime_name=context.runtime_type.value if context.runtime_type else "claude-code",
                context=grpc_context,
                timeout_seconds=context.runtime_config.get("timeout", 300) if context.runtime_config else 300,
            )

            # Execute with streaming and collect all responses
            response_stream = stub.Execute(request)

            final_response = ""
            final_usage = {}
            finish_reason = None
            tool_executions = []

            for response in response_stream:
                # Check for cancellation
                if self.cancellation_manager.is_cancelled(execution_id):
                    logger.info("execution_cancelled_by_manager", execution_id=execution_id)

                    # Send cancel request to agent-runtime
                    cancel_request = pb2.CancelExecutionRequest(execution_id=execution_id)
                    stub.CancelExecution(cancel_request)

                    return RuntimeExecutionResult(
                        response="",
                        usage={},
                        success=False,
                        error="Execution cancelled",
                        finish_reason="cancelled",
                    )

                # Handle different response types
                if response.HasField("chunk"):
                    final_response += response.chunk.content

                elif response.HasField("complete"):
                    final_response = response.complete.response
                    final_usage = {
                        "input_tokens": response.complete.usage.input_tokens,
                        "output_tokens": response.complete.usage.output_tokens,
                        "total_tokens": response.complete.usage.total_tokens,
                    }
                    finish_reason = response.complete.finish_reason
                    tool_executions = [
                        {
                            "tool": te.tool_name,
                            "input": dict(te.input),
                            "output": te.output,
                            "success": te.success,
                            "duration_ms": te.duration_ms,
                        }
                        for te in response.complete.tool_executions
                    ]

                elif response.HasField("error"):
                    return RuntimeExecutionResult(
                        response="",
                        usage={},
                        success=False,
                        error=response.error.error_message,
                        finish_reason="error",
                    )

            logger.info("execution_completed", execution_id=execution_id)

            return RuntimeExecutionResult(
                response=final_response,
                usage=final_usage,
                success=True,
                finish_reason=finish_reason,
                tool_execution_messages=tool_executions,
            )

        except grpc.RpcError as e:
            logger.error(
                "grpc_error",
                execution_id=execution_id,
                code=e.code(),
                details=e.details(),
            )
            return RuntimeExecutionResult(
                response="",
                usage={},
                success=False,
                error=f"GRPC error: {e.details()}",
                finish_reason="error",
            )

        except Exception as e:
            logger.error(
                "execution_failed",
                execution_id=execution_id,
                error=str(e),
            )
            return RuntimeExecutionResult(
                response="",
                usage={},
                success=False,
                error=str(e),
                finish_reason="error",
            )

    async def _stream_execute_impl(
        self,
        context: RuntimeExecutionContext,
        event_callback: Optional[Callable[[Dict], None]] = None,
    ) -> AsyncIterator[RuntimeExecutionResult]:
        """
        Core streaming execution logic.

        Yields RuntimeExecutionResult chunks as they arrive from agent-runtime.
        """
        execution_id = context.execution_id

        logger.info(
            "streaming_via_agent_runtime",
            execution_id=execution_id,
            agent_id=context.agent_id,
            address=self.agent_runtime_address,
        )

        try:
            stub = self._get_stub()
            pb2 = self._pb2

            # Build request
            grpc_context = self._build_execution_context(context)
            request = pb2.ExecuteRequest(
                execution_id=execution_id,
                runtime_name=context.runtime_type.value if context.runtime_type else "claude-code",
                context=grpc_context,
                timeout_seconds=context.runtime_config.get("timeout", 300) if context.runtime_config else 300,
            )

            # Execute with streaming
            response_stream = stub.Execute(request)

            # Process stream
            for response in response_stream:
                # Check for cancellation
                if self.cancellation_manager.is_cancelled(execution_id):
                    logger.info("execution_cancelled_by_manager", execution_id=execution_id)

                    # Send cancel request to agent-runtime
                    cancel_request = pb2.CancelExecutionRequest(execution_id=execution_id)
                    stub.CancelExecution(cancel_request)

                    yield RuntimeExecutionResult(
                        response="",
                        usage={},
                        success=False,
                        error="Execution cancelled",
                        finish_reason="cancelled",
                    )
                    break

                # Handle different response types
                if response.HasField("chunk"):
                    # Yield intermediate chunk
                    yield RuntimeExecutionResult(
                        response=response.chunk.content,
                        usage={},
                        success=True,
                        finish_reason=None,
                        metadata={"chunk_type": response.chunk.type},
                    )

                elif response.HasField("complete"):
                    # Yield final result
                    yield RuntimeExecutionResult(
                        response=response.complete.response,
                        usage={
                            "input_tokens": response.complete.usage.input_tokens,
                            "output_tokens": response.complete.usage.output_tokens,
                            "total_tokens": response.complete.usage.total_tokens,
                        },
                        success=True,
                        finish_reason=response.complete.finish_reason,
                        tool_execution_messages=[
                            {
                                "tool": te.tool_name,
                                "input": dict(te.input),
                                "output": te.output,
                                "success": te.success,
                                "duration_ms": te.duration_ms,
                            }
                            for te in response.complete.tool_executions
                        ],
                        metadata=dict(response.complete.metadata),
                    )

                elif response.HasField("error"):
                    yield RuntimeExecutionResult(
                        response="",
                        usage={},
                        success=False,
                        error=response.error.error_message,
                        finish_reason="error",
                        metadata={"error_code": response.error.error_code},
                    )

            logger.info("streaming_completed", execution_id=execution_id)

        except grpc.RpcError as e:
            logger.error(
                "grpc_error",
                execution_id=execution_id,
                code=e.code(),
                details=e.details(),
            )
            yield RuntimeExecutionResult(
                response="",
                usage={},
                success=False,
                error=f"GRPC error: {e.details()}",
                finish_reason="error",
            )

        except Exception as e:
            logger.error(
                "execution_failed",
                execution_id=execution_id,
                error=str(e),
            )
            yield RuntimeExecutionResult(
                response="",
                usage={},
                success=False,
                error=str(e),
                finish_reason="error",
            )

    async def _cancel_impl(self, execution_id: str) -> bool:
        """Cancel execution via agent-runtime GRPC."""
        try:
            stub = self._get_stub()
            pb2 = self._pb2

            cancel_request = pb2.CancelExecutionRequest(execution_id=execution_id)
            response = stub.CancelExecution(cancel_request)

            logger.info("execution_cancelled", execution_id=execution_id)
            return response.success if hasattr(response, 'success') else True
        except Exception as e:
            logger.error("cancel_failed", execution_id=execution_id, error=str(e))
            return False

    def close(self):
        """Close GRPC channel."""
        if self._channel:
            logger.info("closing_grpc_channel")
            self._channel.close()
            self._channel = None
            self._stub = None

    def __del__(self):
        """Cleanup on deletion."""
        self.close()
