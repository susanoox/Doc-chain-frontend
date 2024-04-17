from unittest import mock

from django.core.files import File

from mayan.apps.storage.models import SharedUploadedFile
from mayan.apps.testing.tests.base import BaseTestCase

from ..events import (
    event_document_created, event_document_file_created,
    event_document_file_edited, event_document_version_created,
    event_document_version_edited, event_document_version_page_created
)
from ..models.document_file_models import DocumentFile
from ..models.document_models import Document
from ..tasks.document_tasks import task_document_upload

from .literals import (
    TEST_DOCUMENT_SMALL_CHECKSUM, TEST_DOCUMENT_SMALL_MIMETYPE,
    TEST_DOCUMENT_SMALL_SIZE, TEST_FILE_SMALL_FILENAME
)
from .mixins.document_mixins import DocumentTestMixin


class DocumentTaskTestCase(DocumentTestMixin, BaseTestCase):
    auto_upload_test_document = False

    @staticmethod
    def _test_post_document_create_callback(document, test_argument):
        return test_argument

    def test_task_document_upload(self):
        self._calculate_test_document_path()

        with open(file=self._test_document_path, mode='rb') as file_object:
            test_shared_uploaded_file = SharedUploadedFile.objects.create(
                file=File(file=file_object)
            )

        self._clear_events()

        task_document_upload.apply_async(
            kwargs={
                'document_type_id': self._test_document_type.pk,
                'shared_uploaded_file_id': test_shared_uploaded_file.pk,
                'user_id': self._test_case_user.pk
            }
        )

        self._test_document = Document.objects.first()
        self._test_document_file = self._test_document.file_latest
        self._test_document_version = self._test_document.version_active
        self._test_document_version_page = self._test_document_version.pages.first()

        self.assertEqual(
            self._test_document.document_type.label,
            self._test_document_type.label
        )
        self.assertEqual(
            self._test_document.label, TEST_FILE_SMALL_FILENAME
        )

        self.assertEqual(
            self._test_document_file.exists(), True
        )
        self.assertEqual(
            self._test_document_file.size, TEST_DOCUMENT_SMALL_SIZE
        )

        self.assertEqual(
            self._test_document_file.mimetype, TEST_DOCUMENT_SMALL_MIMETYPE
        )
        self.assertEqual(
            self._test_document_file.filename, TEST_FILE_SMALL_FILENAME
        )
        self.assertEqual(self._test_document_file.encoding, 'binary')
        self.assertEqual(
            self._test_document_file.checksum, TEST_DOCUMENT_SMALL_CHECKSUM
        )
        self.assertEqual(
            self._test_document_file.pages.count(), 1
        )

        self.assertEqual(
            self._test_document_version.pages.count(), 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 6)

        # Document created.

        self.assertEqual(events[0].action_object, self._test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_document)
        self.assertEqual(events[0].verb, event_document_created.id)

        # Document file created.

        self.assertEqual(events[1].action_object, self._test_document)
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, self._test_document_file)
        self.assertEqual(events[1].verb, event_document_file_created.id)

        # Document file edited (MIME type, page count update).

        self.assertEqual(events[2].action_object, self._test_document)
        self.assertEqual(events[2].actor, self._test_case_user)
        self.assertEqual(events[2].target, self._test_document_file)
        self.assertEqual(events[2].verb, event_document_file_edited.id)

        # Document version created.

        self.assertEqual(events[3].action_object, self._test_document)
        self.assertEqual(events[3].actor, self._test_case_user)
        self.assertEqual(
            events[3].target, self._test_document.version_active
        )
        self.assertEqual(events[3].verb, event_document_version_created.id)

        # Document version page created.

        self.assertEqual(
            events[4].action_object, self._test_document_version
        )
        self.assertEqual(events[4].actor, self._test_case_user)
        self.assertEqual(
            events[4].target, self._test_document_version_page
        )
        self.assertEqual(
            events[4].verb, event_document_version_page_created.id
        )

        self.assertEqual(events[5].action_object, self._test_document)
        self.assertEqual(events[5].actor, self._test_case_user)
        self.assertEqual(events[5].target, self._test_document_version)
        self.assertEqual(events[5].verb, event_document_version_edited.id)

    @mock.patch(target='mayan.apps.documents.tests.test_document_tasks.DocumentTaskTestCase._test_post_document_create_callback')
    def test_task_post_document_create_callback(self, mocked_callback):
        self._calculate_test_document_path()

        with open(file=self._test_document_path, mode='rb') as file_object:
            test_shared_uploaded_file = SharedUploadedFile.objects.create(
                file=File(file=file_object)
            )

        test_document_count = Document.objects.count()
        test_document_file_count = DocumentFile.objects.count()

        self._clear_events()

        callback_dict = {
            'post_document_create': {
                'dotted_path': 'mayan.apps.documents.tests.test_document_tasks.DocumentTaskTestCase',
                'function_name': '_test_post_document_create_callback',
                'kwargs': {'test_argument': 'test_value'}
            }
        }

        task_document_upload.apply_async(
            kwargs={
                'callback_dict': callback_dict,
                'document_type_id': self._test_document_type.pk,
                'shared_uploaded_file_id': test_shared_uploaded_file.pk,
                'user_id': self._test_case_user.pk
            }
        )

        self.assertEqual(
            Document.objects.count(), test_document_count + 1
        )
        self.assertEqual(
            DocumentFile.objects.count(), test_document_file_count + 1
        )

        self._test_document = Document.objects.first()
        self._test_document_file = self._test_document.file_latest
        self._test_document_version = self._test_document.version_active
        self._test_document_version_page = self._test_document_version.pages.first()

        self.assertEqual(mocked_callback.call_count, 1)
        mocked_callback.assert_called_with(
            document=self._test_document, test_argument='test_value'
        )

        self.assertEqual(
            self._test_document.document_type.label,
            self._test_document_type.label
        )
        self.assertEqual(
            self._test_document.label, TEST_FILE_SMALL_FILENAME
        )

        self.assertEqual(
            self._test_document_file.exists(), True
        )
        self.assertEqual(
            self._test_document_file.size, TEST_DOCUMENT_SMALL_SIZE
        )

        self.assertEqual(
            self._test_document_file.mimetype, TEST_DOCUMENT_SMALL_MIMETYPE
        )
        self.assertEqual(
            self._test_document_file.filename, TEST_FILE_SMALL_FILENAME
        )
        self.assertEqual(self._test_document_file.encoding, 'binary')
        self.assertEqual(
            self._test_document_file.checksum, TEST_DOCUMENT_SMALL_CHECKSUM
        )
        self.assertEqual(
            self._test_document_file.pages.count(), 1
        )

        self.assertEqual(
            self._test_document_version.pages.count(), 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 6)

        # Document created.

        self.assertEqual(events[0].action_object, self._test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_document)
        self.assertEqual(events[0].verb, event_document_created.id)

        # Document file created.

        self.assertEqual(events[1].action_object, self._test_document)
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, self._test_document_file)
        self.assertEqual(events[1].verb, event_document_file_created.id)

        # Document file edited (MIME type, page count update).

        self.assertEqual(events[2].action_object, self._test_document)
        self.assertEqual(events[2].actor, self._test_case_user)
        self.assertEqual(events[2].target, self._test_document_file)
        self.assertEqual(events[2].verb, event_document_file_edited.id)

        # Document version created.

        self.assertEqual(events[3].action_object, self._test_document)
        self.assertEqual(events[3].actor, self._test_case_user)
        self.assertEqual(
            events[3].target, self._test_document.version_active
        )
        self.assertEqual(events[3].verb, event_document_version_created.id)

        # Document version page created.

        self.assertEqual(
            events[4].action_object, self._test_document_version
        )
        self.assertEqual(events[4].actor, self._test_case_user)
        self.assertEqual(
            events[4].target, self._test_document_version_page
        )
        self.assertEqual(
            events[4].verb, event_document_version_page_created.id
        )

        self.assertEqual(events[5].action_object, self._test_document)
        self.assertEqual(events[5].actor, self._test_case_user)
        self.assertEqual(events[5].target, self._test_document_version)
        self.assertEqual(events[5].verb, event_document_version_edited.id)
