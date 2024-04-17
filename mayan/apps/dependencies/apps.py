from django.utils.translation import gettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import (
    menu_about, menu_list_facet, menu_return, menu_tools
)
from mayan.apps.navigation.classes import SourceColumn
from mayan.apps.views.column_widgets import TwoStateWidget

from .classes import Dependency, DependencyGroup, DependencyGroupEntry
from .links import (
    link_check_version, link_dependency_group_entry_detail,
    link_dependency_group_entry_list, link_dependency_group_list,
    link_packages_licenses, link_dependency_tool
)


class DependenciesApp(MayanAppConfig):
    app_namespace = 'dependencies'
    app_url = 'dependencies'
    has_rest_api = False
    has_tests = True
    name = 'mayan.apps.dependencies'
    verbose_name = _(message='Dependencies')

    def ready(self):
        super().ready()

        Dependency.load_modules()

        SourceColumn(
            attribute='get_label', is_identifier=True, label=_(message='Label'),
            order=-1, source=Dependency
        )
        SourceColumn(
            attribute='name', include_label=True, label=_(message='Internal name'),
            order=0, source=Dependency
        )
        SourceColumn(
            attribute='get_help_text', include_label=True,
            label=_(message='Description'), order=1, source=Dependency
        )
        SourceColumn(
            attribute='class_name_verbose_name', include_label=True,
            label=_(message='Type'), order=2, source=Dependency
        )
        SourceColumn(
            attribute='get_other_data', include_label=True,
            label=_(message='Other data'), order=3, source=Dependency
        )
        SourceColumn(
            attribute='app_label_verbose_name', include_label=True,
            label=_(message='Declared by'), order=4, source=Dependency
        )
        SourceColumn(
            attribute='get_version_string', include_label=True,
            label=_(message='Version'), order=5, source=Dependency
        )
        SourceColumn(
            attribute='get_environments_verbose_name', include_label=True,
            label=_(message='Environment'), order=6, source=Dependency
        )
        SourceColumn(
            attribute='check', include_label=True, label=_(message='Check'), order=7,
            source=Dependency, widget=TwoStateWidget
        )

        SourceColumn(
            attribute='label', is_identifier=True, label=_(message='Label'),
            order=0, source=DependencyGroup
        )
        SourceColumn(
            attribute='help_text', include_label=True,
            label=_(message='Description'), order=1, source=DependencyGroup
        )

        SourceColumn(
            attribute='label', is_identifier=True, label=_(message='Label'), order=0,
            source=DependencyGroupEntry
        )
        SourceColumn(
            attribute='help_text', include_label=True,
            label=_(message='Description'), order=1, source=DependencyGroupEntry
        )

        # Position #7 which is after "License" link.
        menu_about.bind_links(
            links=(link_packages_licenses,), position=7
        )
        menu_list_facet.bind_links(
            links=(link_dependency_group_entry_list,),
            sources=(DependencyGroup,)
        )
        menu_list_facet.bind_links(
            links=(link_dependency_group_entry_detail,),
            sources=(DependencyGroupEntry,)
        )
        menu_return.bind_links(
            links=(link_dependency_group_list,),
            sources=(
                DependencyGroup, 'dependencies:dependency_group_list'
            )
        )
        menu_tools.bind_links(
            links=(link_dependency_tool, link_check_version)
        )
