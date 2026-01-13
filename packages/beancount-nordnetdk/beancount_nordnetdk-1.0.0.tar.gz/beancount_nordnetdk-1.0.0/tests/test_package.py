"""Test package-level imports and exports."""

import beancount_nordnetdk


def test_package_exports():
    """Test that the package exports NordnetDKImporter."""
    assert hasattr(beancount_nordnetdk, "NordnetDKImporter")
    assert callable(beancount_nordnetdk.NordnetDKImporter)


def test_importer_class_name():
    """Test that the importer class has the correct name."""
    assert beancount_nordnetdk.NordnetDKImporter.__name__ == "NordnetDKImporter"
