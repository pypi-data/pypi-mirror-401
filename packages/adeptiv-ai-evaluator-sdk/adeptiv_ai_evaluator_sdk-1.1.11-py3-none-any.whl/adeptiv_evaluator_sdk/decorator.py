# adeptiv_evaluator_sdk/decorator.py

import time
import functools
import inspect

from opentelemetry.trace import Status, StatusCode
from adeptiv_evaluator_sdk.config import config
from adeptiv_evaluator_sdk.telemetry import init_telemetry

_tracer, _logger, EXECUTION_ID = init_telemetry()


def _validate():
    if not config.api_key:
        raise ValueError("Adeptiv API key is required (config.api_key)")


def trace_llm(
    name: str = None,
    model: str = None,
    operation: str = "llm",
    workflow_id: str = None,
):
    def decorator(func):
        span_name = name or func.__name__

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            _validate()
            wf_id = workflow_id or config.workflow_id

            with _tracer.start_as_current_span(span_name) as span:
                start = time.time()

                span.set_attribute("adeptiv.api_key", config.api_key)
                span.set_attribute("adeptiv.workflow_id", wf_id)
                span.set_attribute("adeptiv.execution_id", EXECUTION_ID)

                span.set_attribute("genai.operation", operation)
                span.set_attribute("genai.model", model or "unknown")

                span.set_attribute("agent.input", str(args))

                try:
                    result = func(*args, **kwargs)

                    span.set_attribute(
                        "genai.latency_ms",
                        (time.time() - start) * 1000,
                    )
                    span.set_attribute("status", "success")

                    span.set_attribute("agent.output", str(result))
                    span.set_attribute("genai.response.type", type(result).__name__)
                    span.set_attribute("genai.response.size", len(str(result)))

                    return result

                except Exception as e:
                    span.record_exception(e)
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    span.set_attribute("status", "error")
                    raise

        return wrapper
    return decorator


def trace_agent(
    agent_name: str,
    model: str = None,
    workflow_id: str = None,
):
    def decorator(func):

        def enrich(span, args, result=None):
            span.set_attribute("adeptiv.api_key", config.api_key)
            span.set_attribute("adeptiv.workflow_id", workflow_id or config.workflow_id)
            span.set_attribute("adeptiv.execution_id", EXECUTION_ID)

            span.set_attribute("agent.name", agent_name)
            span.set_attribute("genai.operation", "agent")
            span.set_attribute("genai.model", model or "unknown")

            span.set_attribute("agent.input", str(args))

            if result :
                span.set_attribute("agent.output", str(result))

        if inspect.iscoroutinefunction(func):
            async def async_wrapper(*args, **kwargs):
                _validate()
                with _tracer.start_as_current_span(f"agent.{agent_name}") as span:
                    start = time.time()
                    result = await func(*args, **kwargs)
                    enrich(span, args, result)
                    span.set_attribute(
                        "genai.latency_ms",
                        (time.time() - start) * 1000,
                    )
                    span.set_attribute("status", "success")
                    return result
            return async_wrapper

        def sync_wrapper(*args, **kwargs):
            _validate()
            with _tracer.start_as_current_span(f"agent.{agent_name}") as span:
                start = time.time()
                result = func(*args, **kwargs)
                enrich(span, args, result)
                span.set_attribute(
                    "genai.latency_ms",
                    (time.time() - start) * 1000,
                )
                span.set_attribute("status", "success")
                return result

        return sync_wrapper

    return decorator
