import logging

from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _

from mayan.apps.document_states.classes import WorkflowAction
from mayan.apps.document_states.literals import BASE_WORKFLOW_TEMPLATE_STATE_ACTION_HELP_TEXT
from mayan.apps.document_states.models.workflow_instance_models import WorkflowInstance
from mayan.apps.user_management.querysets import get_user_queryset

from .models import Message

logger = logging.getLogger(name=__name__)


class WorkflowActionMessageSend(WorkflowAction):
    form_fields = {
        'username_list': {
            'label': _(message='Username list'),
            'class': 'mayan.apps.templating.fields.ModelTemplateField',
            'kwargs': {
                'initial_help_text': _(
                    format_lazy(
                        '{}. {}',
                        _(
                            'Comma separated list of usernames that will '
                            'receive the message.'
                        ),
                        BASE_WORKFLOW_TEMPLATE_STATE_ACTION_HELP_TEXT
                    )
                ),
                'model': WorkflowInstance,
                'model_variable': 'workflow_instance',
                'required': True
            }
        },
        'subject': {
            'label': _(message='Subject'),
            'class': 'mayan.apps.templating.fields.ModelTemplateField',
            'kwargs': {
                'initial_help_text': _(
                    format_lazy(
                        '{}. {}',
                        _(
                            'Subject of the message to be sent.'
                        ), BASE_WORKFLOW_TEMPLATE_STATE_ACTION_HELP_TEXT
                    )
                ),
                'model': WorkflowInstance,
                'model_variable': 'workflow_instance',
                'required': True
            }
        },
        'body': {
            'label': _(message='Body'),
            'class': 'mayan.apps.templating.fields.ModelTemplateField',
            'kwargs': {
                'initial_help_text': _(
                    format_lazy(
                        '{}. {}',
                        _(
                            'The actual text to send.'
                        ), BASE_WORKFLOW_TEMPLATE_STATE_ACTION_HELP_TEXT
                    )
                ),
                'model': WorkflowInstance,
                'model_variable': 'workflow_instance',
                'required': True
            }
        }
    }
    label = _(message='Send user message')

    @classmethod
    def get_form_fieldsets(cls):
        fieldsets = super().get_form_fieldsets()

        fieldsets += (
            (
                _(message='Recipients'), {
                    'fields': ('username_list',)
                },
            ), (
                _(message='Content'), {
                    'fields': ('subject', 'body')
                }
            )
        )
        return fieldsets

    def execute(self, context):
        username_list = self.render_field(
            field_name='username_list', context=context
        ) or ''
        username_list = username_list.split(',')

        subject = self.render_field(
            field_name='subject', context=context
        ) or ''

        body = self.render_field(
            field_name='body', context=context
        ) or ''

        for user in get_user_queryset().filter(username__in=username_list):
            Message.objects.create(
                user=user, body=body, subject=subject
            )
