import pytest

from noodler.tracing.config import setup


def test_setup_valid_url():
    """Test setup with valid URL."""
    setup(
        base_url="http://localhost:8000",
        api_key="test-key",
        service_name="test-service",
    )


def test_setup_valid_https_url():
    """Test setup with valid HTTPS URL."""
    setup(
        base_url="https://api.example.com",
        api_key="test-key",
    )


@pytest.mark.skip(reason="TODO")
def test_setup_invalid_url_no_scheme():
    """Test setup with URL missing scheme."""
    with pytest.raises(ValueError, match="must include a scheme"):
        setup(
            base_url="localhost:8000",
            api_key="test-key",
        )


def test_setup_invalid_url_wrong_scheme():
    """Test setup with invalid scheme."""
    with pytest.raises(ValueError, match="must use http:// or https://"):
        setup(
            base_url="ftp://localhost:8000",
            api_key="test-key",
        )


def test_setup_invalid_url_no_host():
    """Test setup with URL missing host."""
    with pytest.raises(ValueError, match="must include a host"):
        setup(
            base_url="http://",
            api_key="test-key",
        )


def test_setup_empty_base_url():
    """Test setup with empty base_url."""
    with pytest.raises(ValueError, match="must be a non-empty string"):
        setup(
            base_url="",
            api_key="test-key",
        )


def test_setup_empty_api_key():
    """Test setup with empty api_key."""
    with pytest.raises(ValueError, match="must be a non-empty string"):
        setup(
            base_url="http://localhost:8000",
            api_key="",
        )


def test_setup_whitespace_api_key():
    """Test setup with whitespace-only api_key."""
    with pytest.raises(ValueError, match="must be a non-empty string"):
        setup(
            base_url="http://localhost:8000",
            api_key="   ",
        )


def test_setup_empty_service_name():
    """Test setup with empty service_name."""
    with pytest.raises(ValueError, match="must be a non-empty string"):
        setup(
            base_url="http://localhost:8000",
            api_key="test-key",
            service_name="",
        )


def test_setup_custom_service_name():
    """Test setup with custom service name."""
    setup(
        base_url="http://localhost:8000",
        api_key="test-key",
        service_name="my-custom-service",
    )


def test_setup_url_with_trailing_slash():
    """Test setup with URL that has trailing slash."""
    # Should handle trailing slash correctly
    setup(
        base_url="http://localhost:8000/",
        api_key="test-key",
    )
