from unittest import mock

import mayan
from mayan.apps.testing.tests.base import GenericViewTestCase

from ..classes import DependencyGroup
from ..permissions import permission_dependencies_view

from .literals import (
    MESSAGE_TEST_MORE_RECENT, MESSAGE_TEST_NOT_LATEST,
    MESSAGE_TEST_UNKNOWN_VERSION, MESSAGE_TEST_UP_TO_DATE,
    TEST_DEPENDENCY_GROUP_NAME, TEST_DEPENDENCY_GROUP_ENTRY_NAME
)
from .mixins import (
    CheckVersionViewTestMixin, DependencyGroupEntryDetailViewTestMixin
)


class CheckVersionViewTestCase(CheckVersionViewTestMixin, GenericViewTestCase):
    @mock.patch(
        autospec=True,
        target='mayan.apps.dependencies.utils.PyPIClient.get_server_versions'
    )
    def test_check_version_no_permission(self, mock_package_releases):
        mock_package_releases.return_value = (mayan.__version__,)
        response = self._request_check_version_view()
        self.assertNotContains(
            response=response, text=MESSAGE_TEST_UP_TO_DATE, status_code=403
        )

    @mock.patch(
        autospec=True,
        target='mayan.apps.dependencies.utils.PyPIClient.get_server_versions'
    )
    def test_check_version_ahead(self, mock_package_releases):
        self.grant_permission(permission=permission_dependencies_view)

        mock_package_releases.return_value = ('1.0.0',)
        response = self._request_check_version_view()
        self.assertContains(
            response=response, text=MESSAGE_TEST_MORE_RECENT, status_code=200
        )

    @mock.patch(
        autospec=True,
        target='mayan.apps.dependencies.utils.PyPIClient.get_server_versions'
    )
    def test_check_version_not_latest_version(self, mock_package_releases):
        self.grant_permission(permission=permission_dependencies_view)

        mock_package_releases.return_value = ('99.99.99',)
        response = self._request_check_version_view()
        self.assertContains(
            response=response, text=MESSAGE_TEST_NOT_LATEST, status_code=200
        )

    @mock.patch(
        autospec=True,
        target='mayan.apps.dependencies.utils.PyPIClient.get_server_versions'
    )
    def test_check_version_unknown_version(self, mock_package_releases):
        self.grant_permission(permission=permission_dependencies_view)

        mock_package_releases.return_value = None
        response = self._request_check_version_view()
        self.assertContains(
            response=response, text=MESSAGE_TEST_UNKNOWN_VERSION,
            status_code=200
        )

    @mock.patch(
        autospec=True,
        target='mayan.apps.dependencies.utils.PyPIClient.get_server_versions'
    )
    def test_check_version_correct_version(self, mock_package_releases):
        self.grant_permission(permission=permission_dependencies_view)

        mock_package_releases.return_value = (mayan.__version__,)
        response = self._request_check_version_view()
        self.assertContains(
            response=response, text='up-to-date', status_code=200
        )


class DependencyGroupEntryDetailViewTestCase(
    DependencyGroupEntryDetailViewTestMixin, GenericViewTestCase
):
    def test_dependency_group_entry_detail_view_with_permission(self):
        test_dependency = DependencyGroup.get(
            name=TEST_DEPENDENCY_GROUP_NAME
        ).get_entry(
            entry_name=TEST_DEPENDENCY_GROUP_ENTRY_NAME
        ).get_dependencies()[0]

        self.grant_permission(permission=permission_dependencies_view)

        response = self.request_test_dependency_group_entry_detail_view()
        self.assertContains(
            response=response, text=test_dependency.name, status_code=200
        )
