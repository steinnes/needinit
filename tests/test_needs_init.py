import pytest
from needinit import NeedsInitMixin, NotInitialized


class MyObject(NeedsInitMixin, object):
    def __init__(self, exempt=None):
        self.require_init(exempt=exempt)

    def configure(self):
        self.initialize()

    def something(self):
        return "something"


class MySubObject(MyObject):
    def my_method(self):
        return "hello"

    def __init__(self, *args, **kwargs):
        self.my_member = 'oh hai'
        super(MySubObject, self).__init__(*args, **kwargs)


def test_needs_init_initialize_within_exempt_function():
    o = MyObject(exempt=['configure'])
    with pytest.raises(NotInitialized):
        o.something()

    o.configure()
    assert o.something() == "something"


def test_needs_init_initialize_directly_called():
    o = MyObject()
    with pytest.raises(NotInitialized):
        o.something()

    o.initialize()
    assert o.something() == "something"


def test_needs_init_patches_only_methods():
    o = MySubObject()
    assert o.my_member == 'oh hai'
    with pytest.raises(NotInitialized):
        o.my_method()


def test_needs_init_does_not_patch_exempt_methods():
    o = MySubObject(exempt=['something'])

    with pytest.raises(NotInitialized):
        o.my_method()
    assert o.something() == "something"
