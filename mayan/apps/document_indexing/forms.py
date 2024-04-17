from django import forms
from django.forms.formsets import formset_factory
from django.utils.translation import gettext_lazy as _

from mayan.apps.documents.models.document_models import Document
from mayan.apps.templating.fields import ModelTemplateField
from mayan.apps.views.forms import FilteredSelectionForm, Form

from .literals import RELATIONSHIP_CHOICES
from .models.index_template_models import IndexTemplate, IndexTemplateNode
from .permissions import permission_index_template_rebuild


class IndexTemplateEventTriggerRelationshipForm(Form):
    stored_event_type_id = forms.IntegerField(
        widget=forms.widgets.HiddenInput()
    )
    namespace = forms.CharField(
        label=_(message='Namespace'), required=False, widget=forms.TextInput(
            attrs={'readonly': 'readonly'}
        )
    )
    namespace = forms.CharField(
        label=_(message='Namespace'), required=False, widget=forms.TextInput(
            attrs={'readonly': 'readonly'}
        )
    )
    label = forms.CharField(
        label=_(message='Label'), required=False, widget=forms.TextInput(
            attrs={'readonly': 'readonly'}
        )
    )
    relationship = forms.ChoiceField(
        choices=RELATIONSHIP_CHOICES, label=_(message='Enabled'),
        widget=forms.RadioSelect()
    )


IndexTemplateEventTriggerRelationshipFormSet = formset_factory(
    form=IndexTemplateEventTriggerRelationshipForm, extra=0
)


class IndexTemplateFilteredForm(FilteredSelectionForm):
    class Meta:
        allow_multiple = True
        field_name = 'index_templates'
        help_text = _(message='Index templates to be queued for rebuilding.')
        label = _(message='Index templates')
        queryset = IndexTemplate.objects.filter(enabled=True)
        permission = permission_index_template_rebuild
        widget_attributes = {'class': 'select2'}


class IndexTemplateNodeForm(forms.ModelForm):
    """
    A standard model form to allow users to create a new index template node
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['index'].widget = forms.widgets.HiddenInput()
        self.fields['parent'].widget = forms.widgets.HiddenInput()
        self.fields['expression'] = ModelTemplateField(
            label=_(message='Template'), model=Document,
            model_variable='document', required=False
        )

    class Meta:
        fields = (
            'parent', 'index', 'expression', 'enabled', 'link_documents'
        )
        model = IndexTemplateNode
