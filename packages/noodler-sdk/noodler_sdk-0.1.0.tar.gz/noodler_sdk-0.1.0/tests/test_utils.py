from unittest.mock import Mock, patch

from noodler.tracing.utils import get_tracer


def test_get_tracer():
    """Test get_tracer function."""
    with patch("noodler.tracing.utils.trace") as mock_trace:
        mock_tracer = Mock()
        mock_trace.get_tracer.return_value = mock_tracer

        tracer = get_tracer("test.module")

        mock_trace.get_tracer.assert_called_once_with("test.module")
        assert tracer == mock_tracer
