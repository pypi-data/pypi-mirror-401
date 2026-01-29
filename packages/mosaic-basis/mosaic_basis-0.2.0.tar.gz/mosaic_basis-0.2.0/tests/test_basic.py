"""Basic tests to verify the package is properly configured."""

import mosaic_basis


def test_version():
    """Test that the package has a version."""
    assert hasattr(mosaic_basis, "__version__")
    assert isinstance(mosaic_basis.__version__, str)
    assert len(mosaic_basis.__version__) > 0


def test_import():
    """Test that the package can be imported."""
    assert mosaic_basis is not None
