import os

from django import forms as django_forms
from django.apps import apps
from django.conf import settings
from django.contrib.admin.utils import (
    get_fields_from_path, help_text_for_field, label_for_field
)
from django.core.exceptions import FieldDoesNotExist, ImproperlyConfigured
from django.db import models
from django.forms import Form as DjangoForm, ModelForm as DjangoModelForm
from django.utils.translation import gettext_lazy as _

from mayan.apps.common.utils import resolve_attribute

from .form_mixins import FormMixinDynamicFields, FormMixinFieldsets
from .form_options import DetailFormOption, FilteredSelectionFormOptions
from .widgets import DisableableSelectWidget, PlainWidget, TextAreaDiv


class Form(FormMixinFieldsets, DjangoForm):
    """Mayan's default form class."""


class ModelForm(FormMixinFieldsets, DjangoModelForm):
    """Mayan's default model form class."""


class ChoiceForm(Form):
    """
    Form to be used in side by side templates used to add or remove
    items from a many to many field.
    """
    search = django_forms.CharField(
        label=_(message='Search'), required=False,
        widget=django_forms.widgets.TextInput(
            attrs={
                'autocomplete': 'off',
                'class': 'views-select-search',
                'placeholder': 'Filter list'
            }
        )
    )
    selection = django_forms.MultipleChoiceField(
        required=False, widget=DisableableSelectWidget()
    )

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop(
            'choices', []
        )
        label = kwargs.pop(
            'label', _(message='Selection')
        )
        help_text = kwargs.pop('help_text', None)
        disabled_choices = kwargs.pop(
            'disabled_choices', ()
        )
        super().__init__(*args, **kwargs)
        self.fields['selection'].choices = choices
        self.fields['selection'].label = label
        self.fields['selection'].help_text = help_text
        self.fields['selection'].widget.disabled_choices = disabled_choices
        self.fields['selection'].widget.attrs.update(
            {
                'class': 'full-height input-hotkey-double-click',
                'data-height-difference': '495'
            }
        )


class DetailForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.opts = DetailFormOption(
            form=self, kwargs=kwargs, options=getattr(self, 'Meta', None)
        )
        super().__init__(*args, **kwargs)

        for field_index, extra_field in enumerate(iterable=self.opts.extra_fields):
            obj = extra_field.get('object', self.instance)
            field = extra_field.get('field', None)
            func = extra_field.get('func', None)
            label = extra_field.get('label', None)
            help_text = extra_field.get('help_text', None)

            if field:
                if not label:
                    # If label is not specified try to get it from the object
                    # itself.
                    try:
                        fields = get_fields_from_path(model=obj, path=field)
                    except FieldDoesNotExist:
                        # Might be property of a method.
                        label = getattr(
                            getattr(obj, field), 'short_description',
                            field
                        )
                    else:
                        label = label_for_field(
                            model=obj, name=fields[-1].name
                        )

                if not help_text:
                    # If help_text is not specified try to get it from the
                    # object itself.
                    try:
                        fields = get_fields_from_path(model=obj, path=field)
                    except FieldDoesNotExist:
                        # Might be property of a method.
                        help_text = getattr(
                            getattr(obj, field), 'help_text', None
                        )
                    else:
                        help_text = help_text_for_field(
                            model=obj, name=fields[-1].name
                        )

                value = resolve_attribute(attribute=field, obj=obj)

            if func:
                value = func(obj)

            field = field or 'anonymous_field_{}'.format(field_index)

            if isinstance(value, models.query.QuerySet):
                self.fields[field] = django_forms.ModelMultipleChoiceField(
                    queryset=value, label=label
                )
            else:
                self.fields[field] = django_forms.CharField(
                    initial=value, label=label, help_text=help_text,
                    widget=extra_field.get('widget', PlainWidget)
                )

        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs.update(
                {'readonly': 'readonly'}
            )


class DynamicForm(FormMixinDynamicFields, Form):
    """Normal dynamic form."""


class DynamicModelForm(FormMixinDynamicFields, ModelForm):
    """Dynamic model form."""


class FileDisplayForm(Form):
    DIRECTORY = None
    FILENAME = None

    text = django_forms.CharField(
        label='',
        widget=TextAreaDiv(
            attrs={
                'class': 'full-height scrollable',
                'data-height-difference': 270
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.DIRECTORY or self.FILENAME:
            file_path = os.path.join(
                settings.BASE_DIR, os.sep.join(self.DIRECTORY), self.FILENAME
            )
            with open(file=file_path) as file_object:
                self.fields['text'].initial = file_object.read()


class FilteredSelectionForm(Form):
    """
    Form to select the from a list of choice filtered by access. Can be
    configure to allow single or multiple selection.
    """
    def __init__(self, *args, **kwargs):
        opts = FilteredSelectionFormOptions(
            form=self, kwargs=kwargs, options=getattr(self, 'Meta', None)
        )

        if opts.queryset is None:
            if not opts.model:
                raise ImproperlyConfigured(
                    '{} requires a queryset or a model to be specified as '
                    'a meta option or passed during initialization.'.format(
                        self.__class__.__name__
                    )
                )

            queryset = opts.model.objects.all()
        else:
            queryset = opts.queryset

        if opts.allow_multiple:
            extra_kwargs = {}
            field_class = django_forms.ModelMultipleChoiceField
            widget_class = django_forms.widgets.SelectMultiple
        else:
            extra_kwargs = {'empty_label': None}
            field_class = django_forms.ModelChoiceField
            widget_class = django_forms.widgets.Select

        if opts.widget_class:
            widget_class = opts.widget_class

        if opts.permission:
            AccessControlList = apps.get_model(
                app_label='acls', model_name='AccessControlList'
            )
            queryset = AccessControlList.objects.restrict_queryset(
                permission=opts.permission, queryset=queryset,
                user=opts.user
            )

        super().__init__(*args, **kwargs)

        self.fields[opts.field_name] = field_class(
            help_text=opts.help_text, label=opts.label,
            queryset=queryset, required=opts.required,
            widget=widget_class(attrs=opts.widget_attributes),
            **extra_kwargs
        )


class RelationshipForm(Form):
    def __init__(self, *args, **kwargs):
        self._event_actor = kwargs.pop('_event_actor')
        super().__init__(*args, **kwargs)

        self.fields['label'] = django_forms.CharField(
            label=_(message='Label'), required=False,
            widget=django_forms.TextInput(
                attrs={'readonly': 'readonly'}
            )
        )
        self.fields['relationship_type'] = django_forms.ChoiceField(
            choices=self.RELATIONSHIP_CHOICES, label=_(message='Relationship'),
            widget=django_forms.RadioSelect()
        )

        self.sub_object = self.initial.get('sub_object')
        if self.sub_object:
            self.fields['label'].initial = str(self.sub_object)

            self.initial_relationship_type = self.get_relationship_type()

            self.fields['relationship_type'].initial = self.initial_relationship_type

    def get_new_relationship_instance(self):
        related_manager = getattr(
            self.initial.get('object'),
            self.initial['relationship_related_field']
        )
        main_field_name = related_manager.field.name

        return related_manager.model(
            **{
                main_field_name: self.initial.get('object'),
                self.initial['relationship_related_query_field']: self.initial.get('sub_object')
            }
        )

    def get_queryset_relationship(self):
        return getattr(
            self.initial.get('object'),
            self.initial['relationship_related_field']
        ).filter(
            **{
                self.initial['relationship_related_query_field']: self.initial.get('sub_object')
            }
        )

    def get_relationship_instance(self):
        queryset_relationship = self.get_queryset_relationship()
        if queryset_relationship.exists():
            return queryset_relationship.get()
        else:
            return self.get_new_relationship_instance()

    def save(self):
        if self.sub_object:
            if self.cleaned_data['relationship_type'] != self.initial_relationship_type:
                save_method = getattr(
                    self, 'save_relationship_{}'.format(
                        self.cleaned_data['relationship_type']
                    )
                )
                save_method()
