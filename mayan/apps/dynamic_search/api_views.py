from rest_framework.exceptions import ParseError

from mayan.apps.rest_api import generics

from .api_view_mixins import SearchModelAPIViewMixin
from .exceptions import DynamicSearchException
from .search_models import SearchModel
from .serializers import (
    DummySearchResultModelSerializer, SearchModelSerializer
)
from .view_mixins import SearchResultViewMixin


class APISearchView(
    SearchResultViewMixin, SearchModelAPIViewMixin, generics.ListAPIView
):
    """
    get: Perform a search operation.
    """

    def get_serializer_class(self):
        if getattr(self, 'swagger_fake_view', False):
            return DummySearchResultModelSerializer
        else:
            return self.search_model.serializer

    def get_source_queryset(self):
        try:
            return self.get_search_queryset()
        except DynamicSearchException as exception:
            raise ParseError(
                detail=str(exception)
            )


class APISearchModelList(generics.ListAPIView):
    """
    get: Returns a list of all the available search models.
    """

    serializer_class = SearchModelSerializer

    def get_source_queryset(self):
        # This changes after the initial startup as search models are
        # automatically loaded.
        return SearchModel.all()
