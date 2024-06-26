from django.urls import reverse

from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.documents.tests.literals import TEST_FILE_SMALL_PATH

from ..links import (
    link_document_file_signature_detached_delete,
    link_document_file_signature_detail
)
from ..permissions import (
    permission_document_file_signature_delete,
    permission_document_file_signature_view
)
from .literals import TEST_SIGNED_DOCUMENT_PATH
from .mixins import DetachedSignatureTestMixin


class DocumentSignatureLinksTestCase(
    DetachedSignatureTestMixin, GenericDocumentViewTestCase
):
    def test_document_file_signature_detail_link_no_permission(self):
        self._test_document_path = TEST_SIGNED_DOCUMENT_PATH
        self._upload_test_document()

        self.add_test_view(
            test_object=self._test_document.file_latest.signatures.first()
        )
        context = self.get_test_view()
        resolved_link = link_document_file_signature_detail.resolve(
            context=context
        )

        self.assertEqual(resolved_link, None)

    def test_document_file_signature_detail_link_with_permission(self):
        self._test_document_path = TEST_SIGNED_DOCUMENT_PATH
        self._upload_test_document()

        self.grant_access(
            obj=self._test_document,
            permission=permission_document_file_signature_view
        )

        self.add_test_view(
            test_object=self._test_document.file_latest.signatures.first()
        )
        context = self.get_test_view()
        resolved_link = link_document_file_signature_detail.resolve(
            context=context
        )

        self.assertNotEqual(resolved_link, None)
        self.assertEqual(
            resolved_link.url,
            reverse(
                viewname=link_document_file_signature_detail.view,
                kwargs={
                    'signature_id': self._test_document.file_latest.signatures.first().pk,
                }
            )
        )

    def test_document_file_signature_detached_delete_link_no_permission(self):
        self._test_document_path = TEST_FILE_SMALL_PATH
        self._upload_test_document()

        self._upload_test_detached_signature()

        self.add_test_view(
            test_object=self._test_document.file_latest.signatures.first()
        )
        context = self.get_test_view()
        resolved_link = link_document_file_signature_detached_delete.resolve(
            context=context
        )
        self.assertEqual(resolved_link, None)

    def test_document_file_signature_detached_delete_link_with_permission(self):
        self._test_document_path = TEST_FILE_SMALL_PATH
        self._upload_test_document()

        self._upload_test_detached_signature()

        self.grant_access(
            obj=self._test_document,
            permission=permission_document_file_signature_delete
        )

        self.add_test_view(
            test_object=self._test_document.file_latest.signatures.first()
        )
        context = self.get_test_view()
        resolved_link = link_document_file_signature_detached_delete.resolve(
            context=context
        )
        self.assertNotEqual(resolved_link, None)
        self.assertEqual(
            resolved_link.url,
            reverse(
                viewname=link_document_file_signature_detached_delete.view,
                kwargs={
                    'signature_id': self._test_document.file_latest.signatures.first().pk,
                }
            )
        )
