from mayan.apps.testing.tests.mixins import TestMixinObjectCreationTrack

from ...classes import BaseDocumentFilenameGenerator
from ...models.document_type_models import DocumentType, DocumentTypeFilename

from ..literals import (
    TEST_DOCUMENT_TYPE_DELETE_PERIOD, TEST_DOCUMENT_TYPE_DELETE_TIME_UNIT,
    TEST_DOCUMENT_TYPE_LABEL, TEST_DOCUMENT_TYPE_LABEL_EDITED,
    TEST_DOCUMENT_TYPE_QUICK_LABEL, TEST_DOCUMENT_TYPE_QUICK_LABEL_EDITED
)


class DocumentTypeTestMixin(TestMixinObjectCreationTrack):
    _test_object_model = DocumentType
    _test_object_name = '_test_document_type'
    auto_create_test_document_type = True
    auto_delete_test_document_type = True

    def setUp(self):
        super().setUp()

        self._test_document_types = []

        if self.auto_create_test_document_type:
            self._create_test_document_type()

    def tearDown(self):
        if self.auto_delete_test_document_type:
            for document_type in DocumentType.objects.all():
                document_type.delete()
        super().tearDown()

    def _create_test_document_type(self, label=None):
        label = label or '{}_{}'.format(
            TEST_DOCUMENT_TYPE_LABEL, len(self._test_document_types)
        )

        self._test_document_type = DocumentType.objects.create(label=label)
        self._test_document_types.append(self._test_document_type)


class DocumentTypeQuickLabelTestMixin(DocumentTypeTestMixin):
    _test_object_model = DocumentTypeFilename
    _test_object_name = '_test_document_type_quick_label'

    def _create_test_document_type_quick_label(self):
        self._test_document_type_quick_label = self._test_document_type.filenames.create(
            filename=TEST_DOCUMENT_TYPE_QUICK_LABEL
        )


class DocumentQuickLabelViewTestMixin(DocumentTypeQuickLabelTestMixin):
    def _request_test_document_quick_label_edit_view(self, extra_data=None):
        data = {
            'document_type_available_filenames': self._test_document_type_quick_label.pk,
            'label': ''
            # View needs at least an empty label for quick
            # label to work. Cause is unknown.
        }
        data.update(
            extra_data or {}
        )

        return self.post(
            viewname='documents:document_properties_edit', kwargs={
                'document_id': self._test_document.pk
            }, data=data
        )


class DocumentTypeAPIViewTestMixin(DocumentTypeTestMixin):
    def _request_test_document_type_create_api_view(self):
        self._test_object_track()

        response = self.post(
            viewname='rest_api:documenttype-list', data={
                'label': TEST_DOCUMENT_TYPE_LABEL
            }
        )

        self._test_object_set()

        return response

    def _request_test_document_type_delete_api_view(self):
        return self.delete(
            viewname='rest_api:documenttype-detail', kwargs={
                'document_type_id': self._test_document_type.pk
            }
        )

    def _request_test_document_type_detail_api_view(self):
        return self.get(
            viewname='rest_api:documenttype-detail', kwargs={
                'document_type_id': self._test_document_type.pk
            }
        )

    def _request_test_document_type_edit_via_patch_api_view(self):
        return self.patch(
            viewname='rest_api:documenttype-detail', kwargs={
                'document_type_id': self._test_document_type.pk
            }, data={'label': TEST_DOCUMENT_TYPE_LABEL_EDITED}
        )

    def _request_test_document_type_edit_via_put_api_view(self):
        return self.put(
            viewname='rest_api:documenttype-detail', kwargs={
                'document_type_id': self._test_document_type.pk
            }, data={'label': TEST_DOCUMENT_TYPE_LABEL_EDITED}
        )

    def _request_test_document_type_list_api_view(self):
        return self.get(viewname='rest_api:documenttype-list')


class DocumentTypeFilenameGeneratorViewTestMixin(DocumentTypeTestMixin):
    def _request_test_document_type_filename_generator_get_view(self):
        return self.get(
            viewname='documents:document_type_filename_generator', kwargs={
                'document_type_id': self._test_document_type.pk
            }
        )

    def _request_test_document_type_filename_generator_post_view(self):
        return self.post(
            viewname='documents:document_type_filename_generator', kwargs={
                'document_type_id': self._test_document_type.pk
            }, data={
                'filename_generator_backend': BaseDocumentFilenameGenerator.get_default()
            }
        )


class DocumentTypeQuickLabelAPIViewTestMixin(DocumentTypeQuickLabelTestMixin):
    def _request_test_document_type_quick_label_create_api_view(self):
        self._test_object_track()

        response = self.post(
            viewname='rest_api:documenttype-quicklabel-list', kwargs={
                'document_type_id': self._test_document_type.pk
            }, data={
                'filename': TEST_DOCUMENT_TYPE_QUICK_LABEL
            }
        )

        self._test_object_set()

        return response

    def _request_test_document_type_quick_label_delete_api_view(self):
        return self.delete(
            viewname='rest_api:documenttype-quicklabel-detail', kwargs={
                'document_type_id': self._test_document_type.pk,
                'document_type_quick_label_id': self._test_document_type_quick_label.pk
            }
        )

    def _request_test_document_type_quick_label_detail_api_view(self):
        return self.get(
            viewname='rest_api:documenttype-quicklabel-detail', kwargs={
                'document_type_id': self._test_document_type.pk,
                'document_type_quick_label_id': self._test_document_type_quick_label.pk
            }
        )

    def _request_test_document_type_quick_label_edit_via_patch_api_view(self):
        return self.patch(
            viewname='rest_api:documenttype-quicklabel-detail', kwargs={
                'document_type_id': self._test_document_type.pk,
                'document_type_quick_label_id': self._test_document_type_quick_label.pk
            }, data={'filename': TEST_DOCUMENT_TYPE_QUICK_LABEL_EDITED}
        )

    def _request_test_document_type_quick_label_edit_via_put_api_view(self):
        return self.put(
            viewname='rest_api:documenttype-quicklabel-detail', kwargs={
                'document_type_id': self._test_document_type.pk,
                'document_type_quick_label_id': self._test_document_type_quick_label.pk
            }, data={'filename': TEST_DOCUMENT_TYPE_QUICK_LABEL_EDITED}
        )

    def _request_test_document_type_quick_label_list_api_view(self):
        return self.get(
            viewname='rest_api:documenttype-quicklabel-list', kwargs={
                'document_type_id': self._test_document_type.pk
            }
        )


class DocumentTypeQuickLabelViewTestMixin(DocumentTypeQuickLabelTestMixin):
    def _request_test_quick_label_create_view(self):
        return self.post(
            viewname='documents:document_type_filename_create', kwargs={
                'document_type_id': self._test_document_type.pk
            }, data={
                'filename': TEST_DOCUMENT_TYPE_QUICK_LABEL
            }
        )

    def _request_test_quick_label_delete_view(self):
        return self.post(
            viewname='documents:document_type_filename_delete', kwargs={
                'document_type_filename_id': self._test_document_type_quick_label.pk
            }
        )

    def _request_test_quick_label_edit_view(self):
        return self.post(
            viewname='documents:document_type_filename_edit', kwargs={
                'document_type_filename_id': self._test_document_type_quick_label.pk
            }, data={
                'filename': TEST_DOCUMENT_TYPE_QUICK_LABEL_EDITED
            }
        )

    def _request_test_quick_label_list_view(self):
        return self.get(
            viewname='documents:document_type_filename_list', kwargs={
                'document_type_id': self._test_document_type.pk
            }
        )


class DocumentTypeRetentionPoliciesViewTestMixin(DocumentTypeTestMixin):
    def _request_test_document_type_retention_policies_get_view(self):
        return self.get(
            viewname='documents:document_type_retention_policies', kwargs={
                'document_type_id': self._test_document_type.pk
            }
        )

    def _request_test_document_type_retention_policies_post_view(
        self, extra_data=None
    ):
        data = {
            'document_stub_expiration_interval': self._test_document_type.document_stub_expiration_interval,
            'document_stub_pruning_enabled': self._test_document_type.document_stub_pruning_enabled
        }

        if extra_data is not None:
            data.update(extra_data)

        return self.post(
            viewname='documents:document_type_retention_policies',
            kwargs={'document_type_id': self._test_document_type.pk},
            data=data
        )


class DocumentTypeViewTestMixin(DocumentTypeTestMixin):
    def _request_test_document_type_create_view(self):
        return self.post(
            viewname='documents:document_type_create',
            data={
                'label': TEST_DOCUMENT_TYPE_LABEL,
                'delete_time_period': TEST_DOCUMENT_TYPE_DELETE_PERIOD,
                'delete_time_unit': TEST_DOCUMENT_TYPE_DELETE_TIME_UNIT
            }
        )

    def _request_test_document_type_delete_view(self):
        return self.post(
            viewname='documents:document_type_delete', kwargs={
                'document_type_id': self._test_document_type.pk
            }
        )

    def _request_test_document_type_edit_view(self):
        return self.post(
            viewname='documents:document_type_edit', kwargs={
                'document_type_id': self._test_document_type.pk
            }, data={
                'label': TEST_DOCUMENT_TYPE_LABEL_EDITED
            }
        )

    def _request_test_document_type_list_view(self):
        return self.get(viewname='documents:document_type_list')
