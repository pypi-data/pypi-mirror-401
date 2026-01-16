"""
Plan Orchestrator Worker - Temporal worker for plan execution

This worker runs plan orchestration workflows for ALL organizations.
Single worker instance handles plan generation and execution for all orgs.

Usage:
    python -m worker_internal.planner.worker

Environment Variables Required:
    TEMPORAL_NAMESPACE: Temporal namespace (default: agent-control-plane.lpagu)
    TEMPORAL_API_KEY or TEMPORAL_CLOUD_ADMIN_TOKEN: Temporal API key for authentication
    TEMPORAL_HOST or TEMPORAL_URL: Temporal host URL (default: us-east-1.aws.api.temporal.io:7233)
    CONTROL_PLANE_URL: Control Plane API URL (default: https://control-plane.kubiya.ai)
    KUBIYA_API_KEY: Kubiya API key for activities (optional, extracted from requests)
"""

import asyncio
import os
import sys
import argparse
import signal
import structlog
from typing import Optional
from temporalio import workflow
from temporalio.client import Client as TemporalClient, TLSConfig
from temporalio.worker import Worker
from temporalio.worker.workflow_sandbox import SandboxedWorkflowRunner, SandboxRestrictions

# Import workflows and activities
with workflow.unsafe.imports_passed_through():
    from worker_internal.planner.workflows import PlanOrchestratorWorkflow
    from worker_internal.planner.activities import (
        create_plan_execution,
        update_plan_state,
        execute_task_activity,
        validate_task_completion,
        get_task_status_activity,
        call_llm_activity,
        continue_task_activity,
        analyze_task_completion_status,
        publish_event_activity,
    )
    # Import plan generation workflow and activities
    from control_plane_api.app.workflows.plan_generation import PlanGenerationWorkflow
    from control_plane_api.app.activities.plan_generation_activities import (
        generate_plan_activity,
        store_plan_activity,
        update_plan_generation_status,
    )

logger = structlog.get_logger()


class PlanWorker:
    """Plan Orchestrator Worker for Temporal - handles all organizations"""

    def __init__(
        self,
        temporal_url: str,
        temporal_namespace: str,
        temporal_api_key: str,
        control_plane_url: Optional[str] = None,
        task_queue: str = "agent-control-plane.internal",
    ):
        self.temporal_url = temporal_url
        self.temporal_namespace = temporal_namespace
        self.temporal_api_key = temporal_api_key
        self.control_plane_url = control_plane_url or os.getenv("CONTROL_PLANE_URL", "https://control-plane.kubiya.ai")
        self.task_queue = task_queue
        self.client: Optional[TemporalClient] = None
        self.worker: Optional[Worker] = None
        self._shutdown = False

    async def start(self):
        """Start the Temporal worker."""
        logger.info(
            "starting_plan_worker",
            task_queue=self.task_queue,
            temporal_url=self.temporal_url,
            namespace=self.temporal_namespace,
        )

        # Set environment variables for activities
        os.environ["CONTROL_PLANE_URL"] = self.control_plane_url

        # Connect to Temporal
        try:
            # Check if using Temporal Cloud (has API key)
            is_cloud = "tmprl.cloud" in self.temporal_url or "api.temporal.io" in self.temporal_url

            if is_cloud and self.temporal_api_key:
                # Temporal Cloud with API key authentication
                api_key_preview = f"{self.temporal_api_key[:20]}...{self.temporal_api_key[-20:]}" if len(self.temporal_api_key) > 40 else self.temporal_api_key
                logger.info(
                    "connecting_to_temporal_cloud",
                    namespace=self.temporal_namespace,
                    has_api_key=bool(self.temporal_api_key),
                    api_key_preview=api_key_preview,
                    host=self.temporal_url,
                )

                # Connect using rpc_metadata with Bearer token (same as control plane)
                self.client = await TemporalClient.connect(
                    self.temporal_url,
                    namespace=self.temporal_namespace,
                    tls=TLSConfig(),  # TLS without client cert
                    rpc_metadata={"authorization": f"Bearer {self.temporal_api_key}"},
                )
            else:
                # Local Temporal or non-cloud
                logger.info("connecting_to_local_temporal", namespace=self.temporal_namespace)
                self.client = await TemporalClient.connect(
                    self.temporal_url,
                    namespace=self.temporal_namespace,
                )

            logger.info(
                "temporal_client_connected",
                url=self.temporal_url,
                namespace=self.temporal_namespace
            )
        except Exception as e:
            logger.error("failed_to_connect_to_temporal", error=str(e))
            raise

        # Configure workflow sandbox with passthrough modules
        # These modules use non-deterministic operations at import time but are safe
        # because they're only used in activities, not workflow logic
        sandbox_restrictions = SandboxRestrictions.default.with_passthrough_modules(
            "structlog",
            "structlog.dev",
            "structlog.processors",
            "structlog.tracebacks",
            "rich",
            "rich.traceback",
            "httpx",
            "worker_internal",
            "worker_internal.planner",
        )

        # Create worker
        self.worker = Worker(
            self.client,
            task_queue=self.task_queue,
            workflows=[
                PlanOrchestratorWorkflow,  # Plan execution
                PlanGenerationWorkflow,     # Plan generation (async)
            ],
            activities=[
                # Plan orchestrator activities
                create_plan_execution,
                update_plan_state,
                execute_task_activity,
                validate_task_completion,
                get_task_status_activity,
                call_llm_activity,
                continue_task_activity,
                analyze_task_completion_status,
                publish_event_activity,
                # Plan generation activities
                generate_plan_activity,
                store_plan_activity,
                update_plan_generation_status,
            ],
            max_concurrent_workflow_tasks=10,
            max_concurrent_activities=20,
            workflow_runner=SandboxedWorkflowRunner(restrictions=sandbox_restrictions),
            # Temporarily disabled build_id to avoid versioning mismatch issues
            # build_id=f"plan-orchestrator-{self.organization_id}-v1",
        )

        logger.info(
            "plan_worker_started",
            task_queue=self.task_queue,
            namespace=self.temporal_namespace,
        )

        # Run worker
        await self.worker.run()

    async def stop(self):
        """Stop the worker gracefully."""
        logger.info("stopping_plan_worker")
        self._shutdown = True
        # Worker.run() will exit when workflows/activities complete


async def main():
    """Main entry point for worker."""
    # Load environment from .env.local
    from dotenv import load_dotenv
    env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env.local')
    if os.path.exists(env_path):
        load_dotenv(env_path)
        logger.info("loaded_env_from_file", path=env_path)

    parser = argparse.ArgumentParser(
        description="Plan Orchestrator Worker - Handles all organizations",
        epilog="""
Examples:
  # Basic usage (uses env vars)
  python -m worker_internal.planner.worker

  # Override defaults
  python -m worker_internal.planner.worker --temporal-namespace my-namespace.lpagu
        """
    )
    parser.add_argument(
        "--temporal-url",
        default=os.getenv("TEMPORAL_HOST") or os.getenv("TEMPORAL_URL", "us-east-1.aws.api.temporal.io:7233"),
        help="Temporal server URL",
    )
    parser.add_argument(
        "--temporal-namespace",
        default=os.getenv("TEMPORAL_NAMESPACE", "agent-control-plane.lpagu"),
        help="Temporal namespace",
    )
    parser.add_argument(
        "--temporal-api-key",
        default=os.getenv("TEMPORAL_API_KEY") or os.getenv("TEMPORAL_CLOUD_ADMIN_TOKEN"),
        help="Temporal API key",
    )
    parser.add_argument(
        "--task-queue",
        default=os.getenv("TASK_QUEUE", "agent-control-plane.internal"),
        help="Task queue name",
    )
    parser.add_argument(
        "--control-plane-url",
        default=os.getenv("CONTROL_PLANE_URL", "https://control-plane.kubiya.ai"),
        help="Control Plane API URL",
    )

    args = parser.parse_args()

    # Validate required parameters
    if not args.temporal_api_key:
        logger.error(
            "TEMPORAL_API_KEY required",
            message="Set TEMPORAL_API_KEY or TEMPORAL_CLOUD_ADMIN_TOKEN env var"
        )
        sys.exit(1)

    logger.info(
        "worker_configuration",
        temporal_url=args.temporal_url,
        temporal_namespace=args.temporal_namespace,
        task_queue=args.task_queue,
        control_plane_url=args.control_plane_url,
    )

    # Create worker with env-based credentials
    worker = PlanWorker(
        temporal_url=args.temporal_url,
        temporal_namespace=args.temporal_namespace,
        temporal_api_key=args.temporal_api_key,
        control_plane_url=args.control_plane_url,
        task_queue=args.task_queue,
    )

    # Handle shutdown signals
    loop = asyncio.get_event_loop()

    def handle_shutdown(sig):
        logger.info("shutdown_signal_received", signal=sig)
        asyncio.create_task(worker.stop())

    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, lambda s=sig: handle_shutdown(s))

    # Start worker
    try:
        await worker.start()
    except KeyboardInterrupt:
        logger.info("keyboard_interrupt_received")
    except Exception as e:
        import traceback
        logger.error(
            "worker_error",
            error=str(e),
            traceback=traceback.format_exc()
        )
        sys.exit(1)
    finally:
        logger.info("worker_shutdown_complete")


if __name__ == "__main__":
    # Setup logging
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.JSONRenderer(),
        ]
    )

    # Run
    asyncio.run(main())
