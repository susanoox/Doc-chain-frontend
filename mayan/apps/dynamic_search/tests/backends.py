from django.utils.module_loading import import_string

from ..literals import DEFAULT_TEST_SEARCH_BACKEND
from ..search_backends import SearchBackend
from ..settings import setting_backend_arguments


class DummySearchBackend(SearchBackend):
    feature_reindex = True


class TestSearchBackendProxy:
    _test_backend_path = None
    _test_class = None

    def __getattr__(self, attr):
        return getattr(self._backend, attr)

    def __init__(self, *args, **kwargs):
        if self._test_class:
            backend_path = getattr(
                self._test_class, '_test_search_backend_path',
                DEFAULT_TEST_SEARCH_BACKEND
            )
        else:
            backend_path = DEFAULT_TEST_SEARCH_BACKEND
            SearchBackend._disable()

        if self.__class__._test_backend_path != backend_path:
            self.__class__._test_backend_path = backend_path

            self.__class__._backend_kwargs = setting_backend_arguments.value.copy()
            self.__class__._backend_class = import_string(
                dotted_path=backend_path
            )

        self.__class__._backend_kwargs['_test_mode'] = True
        self.__class__._backend = self._backend_class(
            **self.__class__._backend_kwargs
        )

    def _search(self, *args, **kwargs):
        _skip_refresh = kwargs.pop('_skip_refresh', False)

        if not _skip_refresh:
            self._backend.refresh()

        return self._backend._search(*args, **kwargs)
