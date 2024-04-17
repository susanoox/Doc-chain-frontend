from django.utils.translation import gettext_lazy as _

from mayan.apps.permissions.classes import PermissionNamespace

namespace = PermissionNamespace(
    name='document_states', label=_(message='Document workflows')
)

permission_workflow_template_create = namespace.add_permission(
    name='workflow_create', label=_(message='Create workflow templates')
)
permission_workflow_template_delete = namespace.add_permission(
    name='workflow_delte', label=_(message='Delete workflow templates')
)
permission_workflow_template_edit = namespace.add_permission(
    name='workflow_edit', label=_(message='Edit workflow templates')
)
permission_workflow_template_view = namespace.add_permission(
    name='workflow_view', label=_(message='View workflow templates')
)
# Translators: This text refers to the permission to grant user the ability to
# 'transition workflows' from one state to another, to move the workflow
# forwards
permission_workflow_instance_transition = namespace.add_permission(
    name='workflow_transition', label=_(message='Transition workflow instances')
)
permission_workflow_tools = namespace.add_permission(
    name='workflow_tools', label=_(message='Execute workflow tools')
)
