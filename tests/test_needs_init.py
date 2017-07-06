import pytest
from needinit import NeedsInitMixin, NotInitialized


class MyObject(NeedsInitMixin, object):
    def __init__(self, exceptions=None):
        self.require_init(init_func='configure', exceptions=exceptions)

    def configure(self):
        self.initialize()

    def something(self):
        return "something"


def test_needs_init():
    o = MyObject()
    with pytest.raises(NotInitialized):
        o.something()

    o.configure()
    assert o.something() == "something"
