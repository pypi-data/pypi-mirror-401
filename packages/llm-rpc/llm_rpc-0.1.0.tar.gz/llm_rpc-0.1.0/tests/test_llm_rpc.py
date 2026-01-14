import pytest
import llm_rpc


def test_version():
    assert llm_rpc.__version__ == "0.1.0"


def test_import():
    # Basic import test
    assert llm_rpc is not None
