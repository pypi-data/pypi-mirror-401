import pytest
import fwdbwd


def test_version():
    assert fwdbwd.__version__ == "0.1.0"


def test_import():
    # Basic import test
    assert fwdbwd is not None
