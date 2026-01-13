import logging
from urllib.parse import urlparse
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

logger = logging.getLogger(__name__)


def setup(
    base_url: str,
    api_key: str,
    service_name: str = "noodler-service",
) -> None:
    """Configure OpenTelemetry tracing for Noodler.

    This function sets up the global OpenTelemetry tracer provider with
    an OTLP HTTP exporter that sends traces to the Noodler endpoint.

    Args:
        base_url: The base URL for the Noodler API (e.g., "http://127.0.0.1:8000").
                  The endpoint "/api/traces/" will be appended automatically.
                  Must be a valid HTTP or HTTPS URL.
        api_key: The API key for authentication. Must be a non-empty string.
                 Will be formatted as "Bearer {api_key}".
        service_name: The service name to use in traces. Defaults to "noodler-service".
                      Must be a non-empty string.

    Raises:
        ValueError: If base_url is not a valid URL, api_key is empty, or
                    service_name is empty.

    Note:
        This function is idempotent and can be called multiple times.
        Subsequent calls will reconfigure the tracer provider.
    """
    # Validate base_url
    if not base_url or not isinstance(base_url, str):
        raise ValueError("base_url must be a non-empty string")

    # Parse and validate URL format
    parsed = urlparse(base_url)
    if not parsed.scheme:
        raise ValueError(
            f"base_url must include a scheme (http:// or https://): {base_url}"
        )
    if parsed.scheme not in ("http", "https"):
        raise ValueError(
            f"base_url must use http:// or https:// scheme, got: {parsed.scheme}"
        )
    if not parsed.netloc:
        raise ValueError(f"base_url must include a host: {base_url}")

    # Validate api_key
    if not api_key or not isinstance(api_key, str) or not api_key.strip():
        raise ValueError("api_key must be a non-empty string")

    # Validate service_name
    if (
        not service_name
        or not isinstance(service_name, str)
        or not service_name.strip()
    ):
        raise ValueError("service_name must be a non-empty string")

    # Construct the full endpoint URL
    endpoint = f"{base_url.rstrip('/')}/api/traces/"

    logger.info(
        f"Setting up OpenTelemetry tracing: endpoint={endpoint}, service_name={service_name}"
    )
    logger.debug("Using BatchSpanProcessor for span export")

    # Build headers with authorization
    headers = {
        "Content-Type": "application/x-protobuf",
        "Authorization": f"Bearer {api_key}",
    }

    # Shutdown existing provider if it's an SDK TracerProvider
    existing_provider = trace.get_tracer_provider()
    if isinstance(existing_provider, TracerProvider):
        logger.debug("Shutting down existing TracerProvider")
        existing_provider.shutdown()

    # Create resource with service name
    resource = Resource.create(attributes={SERVICE_NAME: service_name})

    # Create tracer provider
    tracer_provider = TracerProvider(resource=resource)

    # Create and add span processor (using BatchSpanProcessor for better performance)
    processor = BatchSpanProcessor(
        OTLPSpanExporter(
            endpoint=endpoint,
            headers=headers,
        )
    )
    tracer_provider.add_span_processor(processor)

    # Set the global default provider
    trace.set_tracer_provider(tracer_provider)
    logger.info("OpenTelemetry tracer provider configured successfully")
