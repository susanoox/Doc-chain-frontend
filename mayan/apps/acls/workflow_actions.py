import logging

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.document_states.classes import WorkflowAction
from mayan.apps.documents.models.document_models import Document
from mayan.apps.permissions.classes import Permission
from mayan.apps.permissions.models import Role

from .classes import ModelPermission
from .permissions import permission_acl_edit

__all__ = (
    'GrantAccessAction', 'GrantDocumentAccessAction', 'RevokeAccessAction',
    'RevokeDocumentAccessAction'
)
logger = logging.getLogger(name=__name__)


class GrantAccessAction(WorkflowAction):
    form_field_widgets = {
        'content_type': {
            'class': 'django.forms.widgets.Select', 'kwargs': {
                'attrs': {'class': 'select2'}
            }
        },
        'roles': {
            'class': 'django.forms.widgets.SelectMultiple', 'kwargs': {
                'attrs': {'class': 'select2'}
            }
        },
        'permissions': {
            'class': 'django.forms.widgets.SelectMultiple', 'kwargs': {
                'attrs': {'class': 'select2'}
            }
        }
    }
    form_fields = {
        'content_type': {
            'label': _(message='Object type'),
            'class': 'django.forms.ModelChoiceField', 'kwargs': {
                'help_text': _(
                    'Type of the object for which the access will be '
                    'modified.'
                ),
                'queryset': ContentType.objects.none(),
                'required': True
            }
        }, 'object_id': {
            'label': _(message='Object ID'),
            'class': 'django.forms.IntegerField', 'kwargs': {
                'help_text': _(
                    'Numeric identifier of the object for which the access '
                    'will be modified.'
                ), 'required': True
            }
        }, 'roles': {
            'label': _(message='Roles'),
            'class': 'django.forms.ModelMultipleChoiceField', 'kwargs': {
                'help_text': _(message='Roles whose access will be modified.'),
                'queryset': Role.objects.all(), 'required': True
            }
        }, 'permissions': {
            'label': _(message='Permissions'),
            'class': 'django.forms.MultipleChoiceField', 'kwargs': {
                'help_text': _(
                    'Permissions to grant/revoke to/from the role for the '
                    'object selected above.'
                ), 'choices': (),
                'required': True
            }
        }
    }
    label = _(message='Grant object access')

    @classmethod
    def clean(cls, request, form_data=None):
        ContentType = apps.get_model(
            app_label='contenttypes', model_name='ContentType'
        )

        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )

        content_type = ContentType.objects.get(
            pk=int(
                form_data['action_data']['content_type']
            )
        )
        obj = content_type.get_object_for_this_type(
            pk=int(
                form_data['action_data']['object_id']
            )
        )

        try:
            AccessControlList.objects.check_access(
                obj=obj, permission=permission_acl_edit,
                user=request.user
            )
        except Exception as exception:
            raise ValidationError(message=exception)
        else:
            return form_data

    @classmethod
    def get_form_fields(cls, *args, **kwargs):
        fields = super().get_form_fields(*args, **kwargs)

        fields['content_type']['kwargs']['queryset'] = ModelPermission.get_classes(
            as_content_type=True
        ).order_by('model')

        fields['permissions']['kwargs']['choices'] = Permission.get_choices()

        return fields

    @classmethod
    def get_form_fieldsets(cls):
        fieldsets = super().get_form_fieldsets()

        fieldsets += (
            (
                _(message='Object'), {
                    'fields': ('content_type', 'object_id')
                }
            ), (
                _(message='Access'), {
                    'fields': ('roles', 'permissions')
                },
            ),
        )
        return fieldsets

    def get_execute_data(self):
        ContentType = apps.get_model(
            app_label='contenttypes', model_name='ContentType'
        )

        content_type = ContentType.objects.get(
            pk=self.kwargs['content_type']
        )
        self.obj = content_type.get_object_for_this_type(
            pk=self.kwargs['object_id']
        )
        self.roles = Role.objects.filter(
            pk__in=self.kwargs['roles']
        )
        self.permissions = [
            Permission.get(
                pk=permission
            ) for permission in self.kwargs['permissions']
        ]

    def execute(self, context):
        self.get_execute_data()

        for role in self.roles:
            for permission in self.permissions:
                AccessControlList.objects.grant(
                    obj=self.obj, permission=permission, role=role
                )


class RevokeAccessAction(GrantAccessAction):
    label = _(message='Revoke object access')

    def execute(self, context):
        self.get_execute_data()

        for role in self.roles:
            for permission in self.permissions:
                AccessControlList.objects.revoke(
                    obj=self.obj, permission=permission, role=role
                )


class GrantDocumentAccessAction(WorkflowAction):
    form_field_widgets = {
        'roles': {
            'class': 'django.forms.widgets.SelectMultiple', 'kwargs': {
                'attrs': {'class': 'select2'}
            }
        },
        'permissions': {
            'class': 'django.forms.widgets.SelectMultiple', 'kwargs': {
                'attrs': {'class': 'select2'}
            }
        }
    }
    form_fields = {
        'roles': {
            'label': _(message='Roles'),
            'class': 'django.forms.ModelMultipleChoiceField', 'kwargs': {
                'help_text': _(message='Roles whose access will be modified.'),
                'queryset': Role.objects.all(), 'required': True
            }
        }, 'permissions': {
            'label': _(message='Permissions'),
            'class': 'django.forms.MultipleChoiceField', 'kwargs': {
                'help_text': _(
                    'Permissions to grant/revoke to/from the role for the '
                    'object selected above.'
                ), 'choices': (),
                'required': True
            }
        }
    }
    label = _(message='Grant document access')

    @classmethod
    def get_form_fields(cls, *args, **kwargs):
        fields = super().get_form_fields(*args, **kwargs)

        fields['permissions']['kwargs']['choices'] = ModelPermission.get_choices_for_class(
            klass=Document
        )

        return fields

    @classmethod
    def get_form_fieldsets(cls):
        fieldsets = super().get_form_fieldsets()

        fieldsets += (
            (
                _(message='Access'), {
                    'fields': ('roles', 'permissions')
                },
            ),
        )
        return fieldsets

    def get_execute_data(self):
        self.roles = Role.objects.filter(
            pk__in=self.kwargs['roles']
        )
        self.permissions = [
            Permission.get(
                pk=permission
            ) for permission in self.kwargs['permissions']
        ]

    def execute(self, context):
        self.get_execute_data()

        for role in self.roles:
            for permission in self.permissions:
                AccessControlList.objects.grant(
                    obj=context['workflow_instance'].document,
                    permission=permission, role=role
                )


class RevokeDocumentAccessAction(GrantDocumentAccessAction):
    label = _(message='Revoke document access')

    def execute(self, context):
        self.get_execute_data()

        for role in self.roles:
            for permission in self.permissions:
                AccessControlList.objects.revoke(
                    obj=context['workflow_instance'].document,
                    permission=permission, role=role
                )
