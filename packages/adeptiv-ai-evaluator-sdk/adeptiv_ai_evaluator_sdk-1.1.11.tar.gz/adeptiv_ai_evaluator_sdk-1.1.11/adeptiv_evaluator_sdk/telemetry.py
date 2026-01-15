# adeptiv_evaluator_sdk/telemetry.py

import logging
import uuid

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

from adeptiv_evaluator_sdk.config import config


EXECUTION_ID = str(uuid.uuid4())

def init_telemetry():
    resource = Resource.create(
        {
            "service.name": config.project_name,
            "adeptiv.api_key": config.api_key,
            # Execution-level grouping
            "adeptiv.execution_id": EXECUTION_ID,
        }
    )

    tracer_provider = TracerProvider(resource=resource)

    tracer_provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(
                endpoint=f"{config.otlp_endpoint}/v1/traces",
                headers={
                    "Authorization": f"Bearer {config.otlp_api_key or config.api_key}",
                    "x-api-key": config.otlp_api_key or config.api_key,
                },
            )
        )
    )

    trace.set_tracer_provider(tracer_provider)
    tracer = trace.get_tracer("adeptiv-genai")

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(config.project_name)

    return tracer, logger, EXECUTION_ID
