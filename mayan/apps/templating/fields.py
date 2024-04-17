from django import forms
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _

import mayan

from .widgets import ModelTemplateWidget, TemplateWidget


class TemplateField(forms.CharField):
    widget = TemplateWidget

    def __init__(self, initial_help_text='', *args, **kwargs):
        self.initial_help_text = initial_help_text

        super().__init__(*args, **kwargs)

        self.help_text = format_lazy(
            '{} {}', self.initial_help_text,
            _(
                'Use Django\'s default templating language '
                '(https://docs.djangoproject.com/en/%(django_version)s/ref/templates/builtins/). '
            ) % {
                'django_version': mayan.__django_version__
            }
        )


class ModelTemplateField(TemplateField):
    widget = ModelTemplateWidget

    def __init__(self, model, model_variable, *args, **kwargs):
        self.model = model
        self.model_variable = model_variable

        super().__init__(*args, **kwargs)

        self.help_text = format_lazy(
            '{} {}', self.initial_help_text,
            _(
                'Use Django\'s default templating language '
                '(https://docs.djangoproject.com/en/%(django_version)s/ref/templates/builtins/). '
                'The {{ %(variable)s }} variable is available to the template.'
            ) % {
                'django_version': mayan.__django_version__,
                'variable': self.model_variable
            }
        )
        self.widget.attrs['app_label'] = self.model._meta.app_label
        self.widget.attrs['model_name'] = self.model._meta.model_name
        self.widget.attrs['data-model-variable'] = self.model_variable
