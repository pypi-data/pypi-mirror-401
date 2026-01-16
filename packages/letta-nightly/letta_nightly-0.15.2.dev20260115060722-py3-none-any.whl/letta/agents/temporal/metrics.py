import os
import time
from contextlib import contextmanager
from functools import wraps
from typing import Any, Callable, Optional

from datadog import initialize, statsd
from temporalio import workflow
from temporalio.exceptions import ActivityError, ApplicationError

from letta.log import get_logger

logger = get_logger(__name__)


class TemporalMetrics:
    _initialized = False
    _enabled = False

    @classmethod
    def initialize(cls) -> None:
        if cls._initialized:
            return

        # Allow explicit disabling via environment variable
        if os.environ.get("DD_METRICS_ENABLED", "").lower() in ("false", "0", "no"):
            logger.info("Datadog metrics explicitly disabled via DD_METRICS_ENABLED")
            cls._enabled = False
            cls._initialized = True
            return

        dd_env = os.environ.get("DD_ENV") or os.environ.get("LETTA_ENVIRONMENT", "development")
        dd_service = os.environ.get("DD_SERVICE", "letta-temporal")
        dd_version = os.environ.get("DD_VERSION", "unknown")

        # Check if using Unix Domain Socket (injected by Datadog admission controller)
        dogstatsd_url = os.environ.get("DD_DOGSTATSD_URL", "")

        try:
            if dogstatsd_url.startswith("unix://"):
                # Use Unix socket (most efficient, auto-configured in K8s)
                socket_path = dogstatsd_url.replace("unix://", "")
                initialize(statsd_socket_path=socket_path)
                logger.info(f"Datadog metrics initialized for service={dd_service}, env={dd_env}, socket={socket_path}")
            else:
                # Fall back to TCP (local dev or custom setup)
                statsd_host = os.environ.get("DD_AGENT_HOST", "localhost")
                statsd_port = int(os.environ.get("DD_DOGSTATSD_PORT", "8125"))
                initialize(
                    statsd_host=statsd_host,
                    statsd_port=statsd_port,
                )
                logger.info(f"Datadog metrics initialized for service={dd_service}, env={dd_env}, statsd={statsd_host}:{statsd_port}")

            statsd.constant_tags = [
                f"env:{dd_env}",
                f"service:{dd_service}",
                f"version:{dd_version}",
            ]

            cls._enabled = True
        except Exception as e:
            logger.warning(f"Failed to initialize Datadog metrics: {e}. Metrics disabled.")
            cls._enabled = False

        cls._initialized = True

    @classmethod
    def is_enabled(cls) -> bool:
        if not cls._initialized:
            cls.initialize()
        return cls._enabled

    @staticmethod
    def increment(metric: str, value: int = 1, tags: Optional[list[str]] = None) -> None:
        if not TemporalMetrics.is_enabled():
            return
        try:
            statsd.increment(metric, value=value, tags=tags or [])
        except Exception as e:
            logger.warning(f"Failed to increment metric {metric}: {e}")

    @staticmethod
    def gauge(metric: str, value: float, tags: Optional[list[str]] = None) -> None:
        if not TemporalMetrics.is_enabled():
            return
        try:
            statsd.gauge(metric, value, tags=tags or [])
        except Exception as e:
            logger.warning(f"Failed to gauge metric {metric}: {e}")

    @staticmethod
    def histogram(metric: str, value: float, tags: Optional[list[str]] = None) -> None:
        if not TemporalMetrics.is_enabled():
            return
        try:
            statsd.distribution(metric, value, tags=tags or [])
        except Exception as e:
            logger.warning(f"Failed to distribution metric {metric}: {e}")

    @staticmethod
    def timing(metric: str, value: float, tags: Optional[list[str]] = None) -> None:
        if not TemporalMetrics.is_enabled():
            return
        try:
            statsd.timing(metric, value, tags=tags or [])
        except Exception as e:
            logger.warning(f"Failed to timing metric {metric}: {e}")

    @staticmethod
    @contextmanager
    def timed(metric: str, tags: Optional[list[str]] = None):
        start_time = time.time()
        try:
            yield
        finally:
            duration_ms = (time.time() - start_time) * 1000
            TemporalMetrics.timing(metric, duration_ms, tags=tags)


class WorkflowMetrics:
    @staticmethod
    def record_workflow_enqueued(workflow_type: str, workflow_id: str) -> None:
        tags = [f"workflow_type:{workflow_type}", f"workflow_id:{workflow_id}"]
        TemporalMetrics.increment("temporal.workflow.enqueued", tags=tags)

    @staticmethod
    def record_workflow_start(workflow_type: str, workflow_id: str) -> None:
        tags = [f"workflow_type:{workflow_type}", f"workflow_id:{workflow_id}"]
        TemporalMetrics.increment("temporal.workflow.started", tags=tags)

    @staticmethod
    def record_workflow_success(workflow_type: str, workflow_id: str, duration_ns: int) -> None:
        tags = [f"workflow_type:{workflow_type}", f"workflow_id:{workflow_id}"]
        TemporalMetrics.increment("temporal.workflow.completed", tags=tags)
        TemporalMetrics.histogram(
            "temporal.workflow.duration",
            duration_ns / 1_000_000,
            tags=tags,
        )

    @staticmethod
    def record_workflow_failure(
        workflow_type: str,
        workflow_id: str,
        error_type: str,
        duration_ns: int,
    ) -> None:
        tags = [
            f"workflow_type:{workflow_type}",
            f"workflow_id:{workflow_id}",
            f"error_type:{error_type}",
        ]
        TemporalMetrics.increment("temporal.workflow.failed", tags=tags)
        TemporalMetrics.histogram(
            "temporal.workflow.duration",
            duration_ns / 1_000_000,
            tags=tags,
        )

    @staticmethod
    def record_workflow_step(workflow_type: str, step_index: int) -> None:
        tags = [f"workflow_type:{workflow_type}"]
        TemporalMetrics.gauge("temporal.workflow.step_index", step_index, tags=tags)

    @staticmethod
    def record_workflow_usage(
        workflow_type: str,
        step_count: int,
        completion_tokens: int,
        prompt_tokens: int,
        total_tokens: int,
    ) -> None:
        tags = [f"workflow_type:{workflow_type}"]
        TemporalMetrics.gauge("temporal.workflow.steps", step_count, tags=tags)
        TemporalMetrics.histogram("temporal.workflow.completion_tokens", completion_tokens, tags=tags)
        TemporalMetrics.histogram("temporal.workflow.prompt_tokens", prompt_tokens, tags=tags)
        TemporalMetrics.histogram("temporal.workflow.total_tokens", total_tokens, tags=tags)


class ActivityMetrics:
    @staticmethod
    def record_activity_start(activity_name: str) -> None:
        tags = [f"activity_name:{activity_name}"]
        TemporalMetrics.increment("temporal.activity.started", tags=tags)

    @staticmethod
    def record_activity_success(activity_name: str, duration_ms: float) -> None:
        tags = [f"activity_name:{activity_name}"]
        TemporalMetrics.increment("temporal.activity.completed", tags=tags)
        TemporalMetrics.histogram("temporal.activity.duration", duration_ms, tags=tags)

    @staticmethod
    def record_activity_failure(activity_name: str, error_type: str, duration_ms: float) -> None:
        tags = [f"activity_name:{activity_name}", f"error_type:{error_type}"]
        TemporalMetrics.increment("temporal.activity.failed", tags=tags)
        TemporalMetrics.histogram("temporal.activity.duration", duration_ms, tags=tags)

    @staticmethod
    def record_activity_retry(activity_name: str, attempt: int) -> None:
        tags = [f"activity_name:{activity_name}", f"attempt:{attempt}"]
        TemporalMetrics.increment("temporal.activity.retry", tags=tags)


class WorkerMetrics:
    @staticmethod
    def record_worker_start(task_queue: str, deployment_name: Optional[str] = None) -> None:
        tags = [f"task_queue:{task_queue}"]
        if deployment_name:
            tags.append(f"deployment:{deployment_name}")
        TemporalMetrics.increment("temporal.worker.started", tags=tags)

    @staticmethod
    def record_worker_shutdown(task_queue: str, deployment_name: Optional[str] = None) -> None:
        tags = [f"task_queue:{task_queue}"]
        if deployment_name:
            tags.append(f"deployment:{deployment_name}")
        TemporalMetrics.increment("temporal.worker.shutdown", tags=tags)

    @staticmethod
    def record_worker_error(task_queue: str, error_type: str, deployment_name: Optional[str] = None) -> None:
        tags = [f"task_queue:{task_queue}", f"error_type:{error_type}"]
        if deployment_name:
            tags.append(f"deployment:{deployment_name}")
        TemporalMetrics.increment("temporal.worker.error", tags=tags)


def track_activity_metrics(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        activity_name = func.__name__
        ActivityMetrics.record_activity_start(activity_name)

        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            duration_ms = (time.time() - start_time) * 1000
            ActivityMetrics.record_activity_success(activity_name, duration_ms)
            return result
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            error_type = type(e).__name__
            ActivityMetrics.record_activity_failure(activity_name, error_type, duration_ms)
            raise

    return wrapper
