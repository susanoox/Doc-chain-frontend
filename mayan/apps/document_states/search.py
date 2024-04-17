from django.utils.translation import gettext_lazy as _

from mayan.apps.documents.search import search_model_document

# Document

search_model_document.add_model_field(
    field='workflows__log_entries__comment',
    label=_(message='Document workflow transition comment')
)
