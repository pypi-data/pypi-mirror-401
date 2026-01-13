from opentelemetry import trace
from opentelemetry.trace import Tracer


def get_tracer(name: str) -> Tracer:
    """Get a tracer instance for the given name.

    Args:
        name: The name of the tracer (typically __name__ or module name).

    Returns:
        A Tracer instance from the global tracer provider.
    """
    return trace.get_tracer(name)
