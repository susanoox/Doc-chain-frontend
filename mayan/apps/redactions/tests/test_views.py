from mayan.apps.acls.classes import ModelPermission
from mayan.apps.converter.models import LayerTransformation
from mayan.apps.converter.tests.mixins import TransformationViewTestMixin
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..layers import layer_redactions
from ..permissions import (
    permission_redaction_create, permission_redaction_delete,
    permission_redaction_edit, permission_redaction_view
)
from ..transformations import TransformationRedactionPercent

from .literals import TEST_REDACTION_ARGUMENT, TEST_REDACTION_ARGUMENT_EDITED


class RedactionViewTestCase(
    TransformationViewTestMixin, GenericDocumentViewTestCase
):
    _test_layer = layer_redactions
    _test_transformation_argument = TEST_REDACTION_ARGUMENT
    _test_transformation_argument_edited = TEST_REDACTION_ARGUMENT_EDITED
    auto_create_test_layer = False
    auto_create_test_transformation_class = False
    TestTransformationClass = TransformationRedactionPercent

    def setUp(self):
        super().setUp()

        ModelPermission.register(
            model=self._test_transformation_object_parent._meta.model, permissions=(
                permission_redaction_create,
                permission_redaction_delete,
                permission_redaction_edit,
                permission_redaction_view
            )
        )

    def test_redaction_create_post_view_no_permission(self):
        transformation_count = LayerTransformation.objects.count()

        self._clear_events()

        response = self._request_transformation_create_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            LayerTransformation.objects.count(), transformation_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_redaction_create_post_view_with_permission(self):
        self.grant_access(
            obj=self._test_transformation_object_parent,
            permission=permission_redaction_create
        )
        transformation_count = LayerTransformation.objects.count()

        self._clear_events()

        response = self._request_transformation_create_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            LayerTransformation.objects.count(), transformation_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_redaction_create_get_view_no_permission(self):
        transformation_count = LayerTransformation.objects.count()

        self._clear_events()

        response = self._request_transformation_create_get_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            LayerTransformation.objects.count(), transformation_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_redaction_create_get_view_with_permission(self):
        self.grant_access(
            obj=self._test_transformation_object_parent,
            permission=permission_redaction_create
        )
        transformation_count = LayerTransformation.objects.count()

        self._clear_events()

        response = self._request_transformation_create_get_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            LayerTransformation.objects.count(), transformation_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_redaction_delete_view_no_permission(self):
        self._create_test_transformation()
        transformation_count = LayerTransformation.objects.count()

        self._clear_events()

        response = self._request_transformation_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            LayerTransformation.objects.count(), transformation_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_redaction_delete_view_with_access(self):
        self._create_test_transformation()
        self.grant_access(
            obj=self._test_transformation_object_parent,
            permission=permission_redaction_delete
        )
        transformation_count = LayerTransformation.objects.count()

        self._clear_events()

        response = self._request_transformation_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            LayerTransformation.objects.count(), transformation_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_redaction_edit_view_no_permission(self):
        self._create_test_transformation()
        transformation_arguments = self._test_transformation.arguments

        self._clear_events()

        response = self._request_transformation_edit_view()
        self.assertEqual(response.status_code, 404)

        self._test_transformation.refresh_from_db()
        self.assertEqual(
            transformation_arguments, self._test_transformation.arguments
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_redaction_edit_view_with_access(self):
        self._create_test_transformation()
        self.grant_access(
            obj=self._test_transformation_object_parent,
            permission=permission_redaction_edit
        )
        transformation_arguments = self._test_transformation.arguments

        self._clear_events()

        response = self._request_transformation_edit_view()
        self.assertEqual(response.status_code, 302)

        self._test_transformation.refresh_from_db()
        self.assertNotEqual(
            transformation_arguments, self._test_transformation.arguments
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_redaction_list_view_no_permission(self):
        self._create_test_transformation()

        self._clear_events()

        response = self._request_transformation_list_view()
        self.assertNotContains(
            response=response, text=str(self._test_transformation_object_parent), status_code=404
        )
        self.assertNotContains(
            response=response,
            text=self._test_transformation.get_transformation_class().label,
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_redaction_list_view_with_access(self):
        self._create_test_transformation()
        self.grant_access(
            obj=self._test_transformation_object_parent,
            permission=permission_redaction_view
        )

        self._clear_events()

        response = self._request_transformation_list_view()
        self.assertContains(
            response=response, text=str(self._test_transformation_object_parent), status_code=200
        )
        self.assertContains(
            response=response,
            text=self._test_transformation.get_transformation_class().label,
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_redaction_select_get_view_no_permission(self):
        transformation_count = LayerTransformation.objects.count()

        self._clear_events()

        response = self._request_test_transformation_select_get_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            LayerTransformation.objects.count(), transformation_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_redaction_select_get_view_with_access(self):
        self.grant_access(
            obj=self._test_transformation_object_parent,
            permission=permission_redaction_create
        )
        transformation_count = LayerTransformation.objects.count()

        self._clear_events()

        response = self._request_test_transformation_select_get_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            LayerTransformation.objects.count(), transformation_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_redaction_select_post_view_no_permission(self):
        transformation_count = LayerTransformation.objects.count()

        self._clear_events()

        response = self._request_test_transformation_select_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            LayerTransformation.objects.count(), transformation_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_redaction_select_post_view_with_access(self):
        self.grant_access(
            obj=self._test_transformation_object_parent,
            permission=permission_redaction_create
        )
        transformation_count = LayerTransformation.objects.count()

        self._clear_events()

        response = self._request_test_transformation_select_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            LayerTransformation.objects.count(), transformation_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
