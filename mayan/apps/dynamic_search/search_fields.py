import functools

from django.contrib.admin.utils import (
    get_fields_from_path, reverse_field_path
)
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.db.models.constants import LOOKUP_SEP
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from .exceptions import DynamicSearchException, DynamicSearchModelException
from .literals import QUERY_PARAMETER_ANY_FIELD
from .value_transformations import ValueTransformation


class SearchField:
    _registry = []
    _registry_by_class = {}

    # Collection is a field that return multiple related fields as a
    # queryset.
    collection = None
    # Concrete is true if the search fields maps 1 to 1 with a real model
    # field.
    concrete = None
    # Priority ensures concrete and collection fields are processed before
    # virtual fields.
    priority = None

    @staticmethod
    class ValueTransformationNull(ValueTransformation):
        def _execute(self):
            return self.value

    @classmethod
    def all(cls):
        return cls._registry

    @classmethod
    def get_by_class(cls, klass):
        return cls._registry_by_class[klass]

    @classmethod
    def get_classes(cls):
        return cls._registry

    @classmethod
    def init(cls, *args, **kwargs):
        for klass in cls.all():
            if klass.check(*args, **kwargs):
                return klass(*args, **kwargs)

        raise DynamicSearchException(
            'No available `SearchField` subclass for this model field.'
        )

    @classmethod
    def register(cls, klass):
        cls._registry.append(klass)

    def __init__(self, field, search_model, help_text=None, label=None):
        self._label = label
        self._field_name = field
        self.help_text = help_text
        self.search_model = search_model

        self.__class__._registry_by_class.setdefault(
            self.__class__, []
        )
        self.__class__._registry_by_class[self.__class__].append(self)

    def __repr__(self):
        return '<{}: {}.{}>'.format(
            self.__class__.__name__, self.model._meta.label,
            self.field_name
        )

    def __str__(self):
        return '{}.{}'.format(
            self.model._meta.label, self.field_name
        )

    def _get_class_registry_index(self):
        return self.__class__._registry.index(self.__class__)

    @cached_property
    def field_class(self):
        return self.model_field.__class__

    @cached_property
    def field_name(self):
        return self._field_name

    @cached_property
    def field_name_model_list(self):
        result = []

        model_list = get_fields_from_path(
            model=self.model, path=self.field_name
        )

        for model in model_list:
            remote_field = model.remote_field

            if remote_field:
                base_model = remote_field.model
            else:
                base_model = self.search_model.base_model

            result.append(base_model)

        return result

    def do_value_index_transform(self, search_backend, value):
        return self.do_value_transform(
            key='index', search_backend=search_backend, value=value
        )

    def do_value_search_transform(self, search_backend, value):
        return self.do_value_transform(
            key='search', search_backend=search_backend, value=value
        )

    def do_value_transform(self, key, search_backend, value):
        transformations = self.get_backend_field_transformations(
            search_backend=search_backend
        )

        transformation_class_list = transformations.get(
            key, (SearchField.ValueTransformationNull,)
        )

        for transformation_class in transformation_class_list:
            value = transformation_class(value=value).execute()

        return value

    @functools.cache
    def get_backend_field_query_type_list(self, search_backend):
        return self.get_search_field_type_backend_dictionary(
            search_backend=search_backend
        ).get(
            'query_type_list', []
        )

    @functools.cache
    def get_backend_field_transformations(self, search_backend):
        return self.get_search_field_type_backend_dictionary(
            search_backend=search_backend
        ).get(
            'transformations', {}
        )

    def get_help_text(self):
        return self.help_text or getattr(self.model_field, 'help_text', '')

    def get_label(self):
        return self.label or self.field_name

    def get_model_field(self):
        return get_fields_from_path(
            model=self.model, path=self.field_name
        )[-1]

    @functools.cache
    def get_search_field_type_backend_dictionary(self, search_backend):
        try:
            search_backend_field_type_attributes = search_backend.get_field_type_mapping()[
                self.field_class
            ]
        except KeyError:
            return {}
        else:
            return search_backend_field_type_attributes

    @property
    def label(self):
        return self._label or self.model_field.verbose_name

    @cached_property
    def model(self):
        return self.search_model.model

    @cached_property
    def model_field(self):
        return self.get_model_field()

    @cached_property
    def related_model(self):
        return self.model_field.model

    @cached_property
    def reverse_path(self):
        return reverse_field_path(model=self.model, path=self.field_name)[1]


class SearchFieldConcrete(SearchField):
    concrete = True

    def _do_field_name_verify(self):
        try:
            self.model_field
        except FieldDoesNotExist:
            raise DynamicSearchModelException(
                'Unknown field or field path `{}`.'.format(self.field_name)
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._do_field_name_verify()


class SearchFieldDirect(SearchFieldConcrete):
    """
    Search for terms in fields that directly belong to the parent
    SearchModel.
    """

    collection = False
    priority = 0

    @classmethod
    def check(cls, *args, **kwargs):
        return LOOKUP_SEP not in kwargs['field'] and not kwargs['field'] == QUERY_PARAMETER_ANY_FIELD

    def get_instance_value(
        self, instance, search_backend, exclude_kwargs=None,
        exclude_model=None, instance_field_data=None
    ):
        value = getattr(instance, self.field_name)

        value = self.do_value_index_transform(
            search_backend=search_backend, value=value
        )

        return search_backend.do_native_type_conversion(value=value)


class SearchFieldRelated(SearchFieldConcrete):
    collection = True
    priority = 1

    @classmethod
    def check(cls, *args, **kwargs):
        return LOOKUP_SEP in kwargs['field'] and not kwargs['field'] == QUERY_PARAMETER_ANY_FIELD

    def get_instance_value(
        self, instance, search_backend, exclude_kwargs=None,
        exclude_model=None, instance_field_data=None
    ):
        last_field = self.field_name.split(LOOKUP_SEP)[-1]

        sub_queryset = self.related_model._meta.default_manager.filter(
            **{
                '{}'.format(self.reverse_path): instance.pk
            }
        ).values_list(last_field, flat=True)

        sub_queryset = sub_queryset.filter(
            **{
                '{field_name}{lookup_separator}isnull'.format(
                    field_name=last_field, lookup_separator=LOOKUP_SEP
                ): False
            }
        )

        if exclude_model and self.related_model == exclude_model:
            sub_queryset = sub_queryset.exclude(**exclude_kwargs)

        result = []

        sub_queryset = sub_queryset.distinct()

        for item in sub_queryset:
            item_value = self.do_value_index_transform(
                search_backend=search_backend, value=item
            )
            if item_value:
                result.append(item_value)

        return search_backend.do_native_type_conversion(value=result)


class SearchFieldVirtual(SearchField):
    """
    Base class for all virtual search field that are not populated by
    directly reading model instance attributes but a calculation.

    Also cover search fields that might not translate to a single model
    field.

    Virtual search fields need to be registered after the other search
    field in order to have access to their instance data when doing
    model instance indexing.
    """

    collection = False
    concrete = False
    priority = 2

    @cached_property
    def field_class(self):
        return models.TextField

    def get_model_field(self):
        return get_fields_from_path(
            model=self.model, path='id'
        )[-1]


class SearchFieldVirtualAllFields(SearchFieldVirtual):
    label = _(message='Any')

    @classmethod
    def check(cls, *args, **kwargs):
        return kwargs['field'] == QUERY_PARAMETER_ANY_FIELD

    @cached_property
    def field_composition(self):
        return [
            search_field for search_field in self.search_model.search_fields if search_field.concrete
        ]

    def get_instance_value(
        self, instance, search_backend, exclude_model=None,
        exclude_kwargs=None, instance_field_data=None
    ):
        return None


SearchField.register(klass=SearchFieldDirect)
SearchField.register(klass=SearchFieldRelated)
SearchField.register(klass=SearchFieldVirtualAllFields)
