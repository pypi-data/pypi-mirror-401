"""
Health Monitor for Agent Runtime Server

Monitors the agent-runtime server health and handles automatic restart on failure.
"""

import asyncio
import structlog
from typing import Optional

logger = structlog.get_logger(__name__)


class HealthMonitor:
    """Monitors agent-runtime health and handles auto-restart."""

    def __init__(
        self,
        agent_runtime_server,
        check_interval: int = 30,
        max_failures: int = 3,
        restart_enabled: bool = True,
    ):
        """
        Initialize health monitor.

        Args:
            agent_runtime_server: AgentRuntimeServer instance to monitor
            check_interval: Seconds between health checks (default: 30)
            max_failures: Consecutive failures before restart (default: 3)
            restart_enabled: Enable automatic restart (default: True)
        """
        self.server = agent_runtime_server
        self.check_interval = check_interval
        self.max_failures = max_failures
        self.restart_enabled = restart_enabled

        self.failure_count = 0
        self.total_checks = 0
        self.total_failures = 0
        self.total_restarts = 0
        self._running = False
        self._task: Optional[asyncio.Task] = None

    async def start(self):
        """Start health monitoring loop in background."""
        if self._running:
            logger.warning("health_monitor_already_running")
            return

        self._running = True
        self._task = asyncio.create_task(self._monitor_loop())
        logger.info(
            "health_monitor_started",
            check_interval=self.check_interval,
            max_failures=self.max_failures,
            restart_enabled=self.restart_enabled,
        )

    async def stop(self):
        """Stop health monitoring loop."""
        if not self._running:
            return

        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

        logger.info(
            "health_monitor_stopped",
            total_checks=self.total_checks,
            total_failures=self.total_failures,
            total_restarts=self.total_restarts,
        )

    async def _monitor_loop(self):
        """Continuous health monitoring with auto-restart."""
        while self._running:
            try:
                await asyncio.sleep(self.check_interval)

                self.total_checks += 1
                is_healthy = await self.server.health_check()

                if not is_healthy:
                    self.failure_count += 1
                    self.total_failures += 1

                    logger.warning(
                        "health_check_failed",
                        consecutive_failures=self.failure_count,
                        max_failures=self.max_failures,
                        total_checks=self.total_checks,
                    )

                    if self.failure_count >= self.max_failures:
                        if self.restart_enabled:
                            logger.error(
                                "agent_runtime_unhealthy_restarting",
                                consecutive_failures=self.failure_count,
                            )
                            await self._restart_server()
                            self.failure_count = 0
                            self.total_restarts += 1
                        else:
                            logger.error(
                                "agent_runtime_unhealthy_restart_disabled",
                                consecutive_failures=self.failure_count,
                            )
                else:
                    # Reset failure count on successful check
                    if self.failure_count > 0:
                        logger.info(
                            "health_check_recovered",
                            after_failures=self.failure_count,
                        )
                    self.failure_count = 0

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("health_monitor_error", error=str(e))
                # Don't let monitoring errors stop the loop
                await asyncio.sleep(5)

    async def _restart_server(self):
        """Restart agent-runtime server."""
        try:
            logger.info("stopping_agent_runtime_for_restart")
            self.server.stop(timeout=10)
            await asyncio.sleep(2)

            logger.info("starting_agent_runtime_after_restart")
            await self.server.start(wait_for_health=True, timeout=30)

            logger.info(
                "agent_runtime_restarted_successfully",
                grpc_address=self.server.grpc_address,
            )

        except Exception as e:
            logger.error("agent_runtime_restart_failed", error=str(e))
            # Don't re-raise - let the monitor continue trying

    def get_stats(self) -> dict:
        """Get health monitoring statistics."""
        return {
            "total_checks": self.total_checks,
            "total_failures": self.total_failures,
            "total_restarts": self.total_restarts,
            "consecutive_failures": self.failure_count,
            "is_running": self._running,
            "health_threshold": self.max_failures,
            "check_interval": self.check_interval,
        }
