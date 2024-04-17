from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from mayan.apps.common.serialization import yaml_load
from mayan.apps.common.validators import YAMLValidator
from mayan.apps.databases.model_mixins import ExtraDataModelMixin
from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.models.document_type_models import DocumentType
from mayan.apps.events.decorators import method_event
from mayan.apps.events.event_managers import (
    EventManagerMethodAfter, EventManagerSave
)

from .events import (
    event_document_metadata_added, event_document_metadata_edited,
    event_document_metadata_removed, event_metadata_type_created,
    event_metadata_type_edited, event_metadata_type_relationship_updated
)
from .managers import DocumentTypeMetadataTypeManager, MetadataTypeManager
from .model_mixins import (
    DocumentMetadataBusinessLogicMixin, MetadataTypeBusinessLogicMixin
)


class MetadataType(
    ExtraDataModelMixin, MetadataTypeBusinessLogicMixin, models.Model
):
    """
    Model to store a type of metadata. Metadata are user defined properties
    that can be assigned a value for each document. Metadata types need
    to be assigned to a document type before they can be used.
    """
    name = models.CharField(
        max_length=48,
        help_text=_(
            'Name used by other apps to reference this metadata type. '
            'Do not use python reserved words, or spaces.'
        ),
        unique=True, verbose_name=_(message='Name')
    )
    label = models.CharField(
        help_text=_(message='Short description of this metadata type.'),
        max_length=48, verbose_name=_(message='Label')
    )
    default = models.CharField(
        blank=True, max_length=128, null=True, help_text=_(
            'Enter a template to render.'
        ), verbose_name=_(message='Default')
    )
    lookup = models.TextField(
        blank=True, null=True, help_text=_(
            'Enter a template to render. Must result in a comma delimited '
            'string.'
        ), verbose_name=_(message='Lookup')
    )
    validation = models.CharField(
        blank=True, help_text=_(
            'The validator will reject data entry if the value entered does '
            'not conform to the expected format.'
        ), max_length=224, verbose_name=_(message='Validator')
    )
    validation_arguments = models.TextField(
        blank=True, help_text=_(
            'Enter the arguments for the validator in YAML format.'
        ), validators=[YAMLValidator()], verbose_name=_(
            'Validator arguments'
        )
    )
    parser = models.CharField(
        blank=True, help_text=_(
            'The parser will reformat the value entered to conform to the '
            'expected format.'
        ), max_length=224, verbose_name=_(message='Parser')
    )
    parser_arguments = models.TextField(
        blank=True, help_text=_(
            'Enter the arguments for the parser in YAML format.'
        ), validators=[
            YAMLValidator()
        ], verbose_name=_(
            'Parser arguments'
        )
    )

    objects = MetadataTypeManager()

    class Meta:
        ordering = ('label',)
        verbose_name = _(message='Metadata type')
        verbose_name_plural = _(message='Metadata types')

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return reverse(
            viewname='metadata:metadata_type_edit', kwargs={
                'metadata_type_id': self.pk
            }
        )

    def natural_key(self):
        return (self.name,)

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'event': event_metadata_type_created,
            'target': 'self',
        },
        edited={
            'event': event_metadata_type_edited,
            'target': 'self',
        }
    )
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def validate_value(self, document_type, value):
        # Check default
        if not value and self.default:
            value = self.get_default_value()

        if not value and self.get_required_for(document_type=document_type):
            raise ValidationError(
                message=_(
                    '"%s" is required for this document type.'
                ) % self.label
            )

        if self.lookup:
            lookup_options = self.get_lookup_values()

            if value and value not in lookup_options:
                raise ValidationError(
                    message=_(message='Value is not one of the provided options.')
                )

        if self.validation:
            validator_class = import_string(dotted_path=self.validation)
            validator_arguments = yaml_load(
                stream=self.validation_arguments or '{}'
            )
            validator = validator_class(**validator_arguments)
            try:
                validator.validate(value)
            except ValidationError as exception:
                raise ValidationError(
                    message=_(
                        'Metadata type validation error; %(exception)s'
                    ) % {
                        'exception': ','.join(exception)
                    }
                ) from exception

        if self.parser:
            parser_class = import_string(dotted_path=self.parser)
            parser_arguments = yaml_load(
                stream=self.parser_arguments or '{}'
            )
            parser = parser_class(**parser_arguments)
            value = parser.parse(value)

        return value


class DocumentMetadata(
    DocumentMetadataBusinessLogicMixin, ExtraDataModelMixin, models.Model
):
    """
    Model used to link an instance of a metadata type with a value to a
    document.
    """
    document = models.ForeignKey(
        on_delete=models.CASCADE, related_name='metadata', to=Document,
        verbose_name=_(message='Document')
    )
    metadata_type = models.ForeignKey(
        on_delete=models.CASCADE, to=MetadataType, verbose_name=_(message='Type')
    )
    value = models.TextField(
        blank=True, help_text=_(
            'The actual value stored in the metadata type field for '
            'the document.'
        ), null=True, verbose_name=_(message='Value')
    )

    class Meta:
        ordering = ('metadata_type',)
        unique_together = ('document', 'metadata_type')
        verbose_name = _(message='Document metadata')
        verbose_name_plural = _(message='Document metadata')

    def __str__(self):
        return str(self.metadata_type)

    def clean_fields(self, *args, **kwargs):
        """
        Pass the value of the metadata being created to the parsers and
        validators for cleanup before saving.
        """
        super().clean_fields(*args, **kwargs)

        self.value = self.metadata_type.validate_value(
            document_type=self.document.document_type, value=self.value
        )

    @method_event(
        event_manager_class=EventManagerMethodAfter,
        action_object='metadata_type',
        event=event_document_metadata_removed,
        target='document'
    )
    def delete(self, enforce_required=True, *args, **kwargs):
        """
        Delete a metadata from a document. enforce_required which defaults
        to True, prevents deletion of required metadata at the model level.
        It used set to False when deleting document metadata on document
        type change.
        """
        is_required_for_document_type = enforce_required and self.document.document_type.metadata.filter(
            required=True
        ).filter(metadata_type=self.metadata_type).exists()

        if is_required_for_document_type:
            raise ValidationError(
                message=_(
                    'Metadata type is required for this document type.'
                )
            )

        return super().delete(*args, **kwargs)

    def natural_key(self):
        return self.document.natural_key() + self.metadata_type.natural_key()
    natural_key.dependencies = [
        'documents.Document', 'metadata.MetadataType'
    ]

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'action_object': 'metadata_type',
            'event': event_document_metadata_added,
            'target': 'document'
        },
        edited={
            'action_object': 'metadata_type',
            'event': event_document_metadata_edited,
            'target': 'document'
        }
    )
    def save(self, *args, **kwargs):
        is_not_valid_for_document_type = not self.document.document_type.metadata.filter(
            metadata_type=self.metadata_type
        ).exists()

        if is_not_valid_for_document_type:
            raise ValidationError(
                message=_(
                    'Metadata type is not valid for this document type.'
                )
            )

        return super().save(*args, **kwargs)


class DocumentTypeMetadataType(ExtraDataModelMixin, models.Model):
    """
    Model used to store the relationship between a metadata type and a
    document type.
    """
    document_type = models.ForeignKey(
        on_delete=models.CASCADE, related_name='metadata', to=DocumentType,
        verbose_name=_(message='Document type')
    )
    metadata_type = models.ForeignKey(
        on_delete=models.CASCADE, related_name='document_types',
        to=MetadataType, verbose_name=_(message='Metadata type')
    )
    required = models.BooleanField(
        default=False, verbose_name=_(message='Required')
    )

    objects = DocumentTypeMetadataTypeManager()

    class Meta:
        ordering = ('metadata_type',)
        unique_together = ('document_type', 'metadata_type')
        verbose_name = _(message='Document type metadata type options')
        verbose_name_plural = _(message='Document type metadata types options')

    def __str__(self):
        return str(self.metadata_type)

    @method_event(
        event_manager_class=EventManagerMethodAfter,
        action_object='metadata_type',
        event=event_metadata_type_relationship_updated,
        target='document_type'
    )
    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'action_object': 'metadata_type',
            'event': event_metadata_type_relationship_updated,
            'target': 'document_type'
        },
        edited={
            'action_object': 'metadata_type',
            'event': event_metadata_type_relationship_updated,
            'target': 'document_type'
        }
    )
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
