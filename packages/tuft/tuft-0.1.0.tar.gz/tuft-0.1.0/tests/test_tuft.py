import pytest
import tuft


def test_version():
    assert tuft.__version__ == "0.1.0"


def test_import():
    # Basic import test
    assert tuft is not None
