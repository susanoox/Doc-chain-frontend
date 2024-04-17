from mayan.apps.documents.models.document_models import Document
from mayan.apps.rest_api import generics
from mayan.apps.rest_api.api_view_mixins import ExternalObjectAPIViewMixin

from .permissions import (
    permission_document_comment_create, permission_document_comment_delete,
    permission_document_comment_edit, permission_document_comment_view
)
from .serializers import CommentSerializer


class APICommentListView(
    ExternalObjectAPIViewMixin, generics.ListCreateAPIView
):
    """
    get: Returns a list of all the document comments.
    post: Create a new document comment.
    """
    external_object_queryset = Document.valid.all()
    external_object_pk_url_kwarg = 'document_id'
    mayan_external_object_permission_map = {
        'GET': permission_document_comment_view,
        'POST': permission_document_comment_create
    }
    ordering_fields = ('id', 'submit_date')
    serializer_class = CommentSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
            'document': self.get_external_object(),
            'user': self.request.user
        }

    def get_source_queryset(self):
        return self.get_external_object().comments.all()


class APICommentView(
    ExternalObjectAPIViewMixin, generics.RetrieveUpdateDestroyAPIView
):
    """
    delete: Delete the selected document comment.
    get: Returns the details of the selected document comment.
    """
    external_object_queryset = Document.valid.all()
    external_object_pk_url_kwarg = 'document_id'
    mayan_external_object_permission_map = {
        'DELETE': permission_document_comment_delete,
        'GET': permission_document_comment_view,
        'PATCH': permission_document_comment_edit,
        'PUT': permission_document_comment_edit
    }
    lookup_url_kwarg = 'comment_id'
    serializer_class = CommentSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
            'document': self.get_external_object()
        }

    def get_source_queryset(self):
        return self.get_external_object().comments.all()
