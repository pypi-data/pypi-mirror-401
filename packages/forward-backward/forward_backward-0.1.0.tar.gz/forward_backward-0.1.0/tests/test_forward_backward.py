import pytest
import forward_backward


def test_version():
    assert forward_backward.__version__ == "0.1.0"


def test_import():
    # Basic import test
    assert forward_backward is not None
