from django import forms
from django.utils.html import escape
from django.utils.translation import gettext_lazy as _

from mayan.apps.views.forms import DetailForm

from .models import Key


class KeyDetailForm(DetailForm):
    def __init__(self, *args, **kwargs):
        instance = kwargs['instance']

        extra_fields = (
            {
                'field': 'key_id', 'label': _(message='Key ID')
            },
            {
                'func': lambda x: escape(instance.user_id),
                'label': _(message='User ID')
            },
            {
                'field': 'creation_date', 'label': _(message='Creation date'),
                'widget': forms.widgets.DateInput
            },
            {
                'func': lambda x: instance.expiration_date or _(message='None'),
                'label': _(message='Expiration date'),
                'widget': forms.widgets.DateInput
            },
            {
                'field': 'fingerprint', 'label': _(message='Fingerprint')
            },
            {
                'field': 'length', 'label': _(message='Length')
            },
            {
                'field': 'algorithm', 'label': _(message='Algorithm')
            },
            {
                'func': lambda x: instance.get_key_type_display(),
                'label': _(message='Type')
            }
        )

        kwargs['extra_fields'] = extra_fields
        super().__init__(*args, **kwargs)

    class Meta:
        fields = ()
        model = Key


class KeySearchForm(forms.Form):
    term = forms.CharField(
        label=_(message='Term'),
        help_text=_(message='Name, e-mail, key ID or key fingerprint to look for.')
    )
