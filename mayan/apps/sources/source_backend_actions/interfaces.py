from rest_framework import status
from rest_framework.response import Response

from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import classproperty
from django.utils.translation import gettext_lazy as _

from ..exceptions import SourceActionExceptionInterfaceArgumentMissing

from .arguments import argument_request
from .interface_arguments import SourceBackendActionInterfaceArgument


class SourceBackendActionInterfaceMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        new_class = super().__new__(
            mcs, name, bases, attrs
        )

        mcs.update_arguments(new_class=new_class)

        return new_class

    @classmethod
    def update_arguments(mcs, new_class):
        argument_list = []
        for mro_klass in new_class.mro():
            argument_base = getattr(mro_klass, 'Argument', None)
            if argument_base:
                for item_name in dir(argument_base):
                    item = getattr(argument_base, item_name)
                    try:
                        if isinstance(item, SourceBackendActionInterfaceArgument):
                            item.name = item_name

                            if item.required and item.has_default:
                                raise ImproperlyConfigured(
                                    'Argument `{}` cannot be required and '
                                    'also provide a default.'.format(
                                        item.name
                                    )
                                )
                            elif not item.required and not item.has_default:
                                raise ImproperlyConfigured(
                                    'Optional argument `{}` must specify a '
                                    'default.'.format(
                                        item.name
                                    )
                                )

                            if item not in argument_list:
                                argument_list.append(item)
                    except TypeError:
                        """Expected error. Ignore and continue."""

        setattr(new_class, 'arguments', argument_list)


class SourceBackendActionInterface(
    metaclass=SourceBackendActionInterfaceMetaclass
):
    hidden = False

    @classproperty
    def arguments_visible(cls):
        for argument in cls.arguments:
            if not argument.hidden:
                yield argument

    @classproperty
    def name(cls):
        return str(cls.__name__)

    def __init__(self, action):
        """
        Load:     Data arrives in the context, is processed by the interface,
                  and stored in the action_kwargs.

        Retrieve: Action data is stored in action_data, context is used as
                  persistent storage for the MRO and the final return value
                  is set in interface_result.
        """
        self.action = action
        self.action_data = None
        self.action_kwargs = {}
        self.context = {}
        self.interface_result = None

    def get_confirmation_context(self, request):
        return {}

    def load(self, **kwargs):
        for argument in self.arguments:
            try:
                value = kwargs.pop(argument.name)
            except KeyError:
                if argument.required:
                    raise SourceActionExceptionInterfaceArgumentMissing(
                        'Argument `{}` missing for interface `{}`.'.format(
                            argument.name, self.name
                        )
                    )
                else:
                    value = argument.default

            self.context[argument.name] = value

        self.process_interface_context()

        return self.action_kwargs

    def process_action_data(self):
        return

    def process_interface_context(self):
        return

    def retrieve(self, data, context=None):
        self.context = context
        self.action_data = data
        self.process_action_data()
        return self.interface_result


class SourceBackendActionInterfaceRequest(SourceBackendActionInterface):
    class Argument:
        request = argument_request


class SourceBackendActionInterfaceRequestRESTAPI(
    SourceBackendActionInterfaceRequest
):
    def process_action_data(self):
        if self.action_data:
            headers = self.context['view'].get_success_headers(
                data=self.action_data
            )

            self.interface_result = Response(
                data=self.action_data, headers=headers,
                status=status.HTTP_200_OK
            )
        else:
            self.interface_result = Response(status=status.HTTP_200_OK)


class SourceBackendActionInterfaceRequestView(
    SourceBackendActionInterfaceRequest
):
    """
    Interface for HTML views.
    """


class SourceBackendActionInterfaceRequestViewForm(
    SourceBackendActionInterfaceRequestView
):
    class Argument:
        forms = SourceBackendActionInterfaceArgument(
            help_text=_(
                'Forms containing the upload data generated by the '
                'upload views.'
            )
        )


class SourceBackendActionInterfaceTask(SourceBackendActionInterface):
    """
    Interface that every action needs to received the background task
    arguments.
    """
