from django.urls import re_path

from .api_views.source_action_api_views import (
    APISourceActionDetailView, APISourceActionExecuteView,
    APISourceActionListView
)
from .api_views.source_api_views import APISourceListView, APISourceView
from .views.document_file_views import (
    DocumentFileSourceMetadataList, DocumentFileUploadView
)
from .views.document_views import DocumentUploadView
from .views.source_views import (
    SourceActionView, SourceBackendSelectionView, SourceCreateView,
    SourceDeleteView, SourceEditView, SourceListView, SourceTestView
)
from .wizards import DocumentCreateWizard

urlpatterns_documents = [
    re_path(
        route=r'^sources/documents/wizard/$',
        name='document_upload_wizard', view=DocumentCreateWizard.as_view()
    ),
    re_path(
        route=r'^sources/(?P<source_id>\d+)/documents/upload/$',
        name='document_upload', view=DocumentUploadView.as_view()
    ),
    re_path(
        route=r'^sources/any/documents/upload/$',
        name='document_upload', view=DocumentUploadView.as_view()
    )
]

urlpatterns_document_files = [
    re_path(
        route=r'^document_files/(?P<document_file_id>\d+)/source_metadata/$',
        name='document_file_source_metadata_list',
        view=DocumentFileSourceMetadataList.as_view()
    ),
    re_path(
        route=r'^sources/(?P<source_id>\d+)/documents/(?P<document_id>\d+)/files/upload/$',
        name='document_file_upload', view=DocumentFileUploadView.as_view()
    ),
    re_path(
        route=r'^sources/any/documents/(?P<document_id>\d+)/files/upload/$',
        name='document_file_upload', view=DocumentFileUploadView.as_view()
    )
]

urlpatterns_sources = [

    re_path(
        route=r'^sources/$', name='source_list',
        view=SourceListView.as_view()
    ),
    re_path(
        route=r'^sources/backend/selection/$',
        name='source_backend_selection',
        view=SourceBackendSelectionView.as_view()
    ),
    re_path(
        route=r'^sources/(?P<backend_path>[a-zA-Z0-9_.]+)/create/$',
        name='source_create', view=SourceCreateView.as_view()
    ),
    re_path(
        route=r'^sources/(?P<source_id>\d+)/actions/(?P<action_name>[a-zA-Z0-9_.]+)/$',
        name='source_action', view=SourceActionView.as_view()
    ),
    re_path(
        route=r'^sources/(?P<source_id>\d+)/delete/$',
        name='source_delete', view=SourceDeleteView.as_view()
    ),
    re_path(
        route=r'^sources/(?P<source_id>\d+)/edit/$', name='source_edit',
        view=SourceEditView.as_view()
    ),
    re_path(
        route=r'^sources/(?P<source_id>\d+)/test/$',
        name='source_test', view=SourceTestView.as_view()
    )
]

urlpatterns = []
urlpatterns.extend(urlpatterns_documents)
urlpatterns.extend(urlpatterns_document_files)
urlpatterns.extend(urlpatterns_sources)

api_urls = [
    re_path(
        route=r'^sources/$', name='source-list',
        view=APISourceListView.as_view()
    ),
    re_path(
        route=r'^sources/(?P<source_id>[0-9]+)/$',
        name='source-detail', view=APISourceView.as_view()
    ),
    re_path(
        route=r'^sources/(?P<source_id>[0-9]+)/actions/$',
        name='source_action-list', view=APISourceActionListView.as_view()
    ),
    re_path(
        route=r'^sources/(?P<source_id>[0-9]+)/actions/(?P<action_name>[a-zA-Z0-9_.]+)/$',
        name='source_action-detail', view=APISourceActionDetailView.as_view()
    ),
    re_path(
        route=r'^sources/(?P<source_id>[0-9]+)/actions/(?P<action_name>[a-zA-Z0-9_.]+)/execute/$',
        name='source_action-execute', view=APISourceActionExecuteView.as_view()
    )
]
