import pytest
from ..decorators import debug


class MockDebugger(object):
    def __init__(self):
        self.called = False

    def post_mortem(self, tb):
        self.called = True


def test_debug_debugger_not_called_if_no_error():

    mock_debugger = MockDebugger()

    @debug(use_debugger=mock_debugger)
    def f(): return 0

    assert f() == 0
    assert not mock_debugger.called


def test_debug_debugger_not_called_if_debug_False():

    mock_debugger = MockDebugger()

    @debug(False, use_debugger=mock_debugger)
    def f(): raise Exception('error')

    with pytest.raises(Exception):
        f()


def test_debug_debugger_called_if_debug_True_and_raises():

    mock_debugger = MockDebugger()

    @debug(use_debugger=mock_debugger)
    def f(): raise Exception('error')

    f()
    assert mock_debugger.called
