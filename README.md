# needinit

This is a tiny python library to implement a fairly useful pattern of
preventing method calls on an object which has not been initialized.

## How does it work?

Any object which extends `NeedsInit` or `NeedsInitMixin` (and calls `.require_init`)
gets its methods temporarily replaced by a lambda which raises a `NotInitialized`
TypeError exception.  Calling `.initialize()` on the object will replace the lambdas
with the originals, and can either be done externally before configuring the object
or from within a configuration/setup method.

```python
In [1]: from needinit import NeedsInit

In [2]: class MyObject(NeedsInit):
   ...:     def something(self):
   ...:         return "hello, I'm ready for action"
   ...:

In [3]: o = MyObject()

In [4]: o.something()
... stack trace suppressed
NotInitialized: <__main__.MyObject object at 0x104382ed0>.something((), {}) - not callable, needs initializing.

In [5]: o.initialize()

In [6]: o.something()
Out[6]: "hello, I'm ready for action"
```

## Exempting methods

`NeedsInit` can take a list of `exempt` methods which is very useful to allow calling
non-constructor configuration/init methods -- the use case for which this library was
written, but other cases aren't hard to imagine, such as some status/inspection methods.

The `__init__`, `require_init`, and `initialize` methods are always exempt.

```python
from needinit import NeedsInit


class MyAppExtension(NeedsInit):
    def __init__(self, some_param, *args, **kwargs):
        super(MyAppExtension, self).__init__(*args, exempt=['init_app'], **kwargs)
        self.some_param = some_param

    def init_app(self, app):
        self.initialize()  # all methods are now re-enabled
        self.initialize_session(app.config['API_KEY'])

    def initialize_session(self, api_key):
        self.session = SessionMaker(api_key=api_key, environment=self.some_param)
```
