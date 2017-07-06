import inspect


class NotInitialized(TypeError):
    pass


def _not_initialized(obj, method, *args, **kwargs):
    raise NotInitialized('{}.{}({}, {}) - not callable, needs initializing.'.format(
        obj, method, args, kwargs)
    )


class NeedsInitMixin(object):
    """A mixin which prevents methods on an object from being called
    before a special initialization function is called on that object.

    Can be used in several ways:

    class MyAppExtension(NeedsInitMixin, object):
        def __init__(self):
            self.init_required(init_func='init_app', exceptions='status')

        def init_app(self, app):
            self.config = app.config
            self.api_client = ApiClient(self.config.credentials)
            self.initialize()
    """
    def initialize(self):
        for name, method in self._originals.iteritems():
            setattr(self, name, method)

    def require_init(self, init_func, exceptions=None):
        self._originals = {}
        exempt = ['__init__', 'initialize', init_func]
        if exceptions is not None:
            exempt += exceptions

        for attr in dir(self):
            if not inspect.ismethod(getattr(self, attr)):
                continue
            if attr in exempt:
                continue

            self._originals[attr] = getattr(self, attr)
            setattr(self, attr, lambda *args, **kwargs: _not_initialized(self, attr, *args, **kwargs))


class NeedsInit(NeedsInitMixin):
    def __init__(self, init_func, exceptions=None):
        self.require_init(init_func=init_func, exceptions=exceptions)
