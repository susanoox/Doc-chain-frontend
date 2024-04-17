import logging

from mayan.apps.common.utils import return_attrib

from .literals import EVENT_MANAGER_ORDER_AFTER

logger = logging.getLogger(name=__name__)


class EventManager:
    """
    keep_attributes - List of event related object attributes that should
    not be removed after the event is committed.
    """
    EVENT_ATTRIBUTES = ('ignore', 'keep_attributes', 'type')
    EVENT_ARGUMENTS = ('actor', 'action_object', 'target')

    def __init__(self, instance, **kwargs):
        self.instance = instance
        self.instance_event_attributes = {}
        self.kwargs = kwargs

    def commit(self):
        if not self.instance_event_attributes['ignore']:
            self._commit()
        else:
            # If the event is ignored, restore the event related attributes
            # that were removed via .pop().
            for key, value in self.instance_event_attributes.items():
                if key not in ('ignore', 'type'):
                    setattr(
                        self.instance, '_event_{}'.format(key), value
                    )

    def get_event_arguments(self, argument_map):
        result = {}

        for argument in self.EVENT_ARGUMENTS:
            # Grab the static argument value from the argument map.
            # If the argument is not in the map, it is dynamic and must be
            # obtained from the instance attributes.
            value = argument_map.get(
                argument, self.instance_event_attributes[argument]
            )

            if value == 'self':
                result[argument] = self.instance
            elif isinstance(value, str):
                result[argument] = return_attrib(
                    attrib=value, obj=self.instance
                )
            else:
                result[argument] = value

        return result

    def pop_event_attributes(self):
        for attribute in self.EVENT_ATTRIBUTES:
            # If the attribute is not set or is set but is None.
            if not self.instance_event_attributes.get(attribute, None):
                full_name = '_event_{}'.format(attribute)
                value = self.instance.__dict__.pop(full_name, None)
                self.instance_event_attributes[attribute] = value

        keep_attributes = self.instance_event_attributes['keep_attributes'] or ()

        # Allow passing a runtime defined event.
        if self.instance_event_attributes['type']:
            self.kwargs['event'] = self.instance_event_attributes['type']

        for attribute in self.EVENT_ARGUMENTS:
            # If the attribute is not set or is set but is None.
            if not self.instance_event_attributes.get(attribute, None):
                full_name = '_event_{}'.format(attribute)
                if full_name in keep_attributes:
                    value = self.instance.__dict__.get(full_name, None)
                else:
                    value = self.instance.__dict__.pop(full_name, None)

                self.instance_event_attributes[attribute] = value

    def prepare(self):
        """Optional method to gather information before the actual commit."""


class EventManagerMethodAfter(EventManager):
    order = EVENT_MANAGER_ORDER_AFTER

    def _commit(self):
        kwargs = self.get_event_arguments(argument_map=self.kwargs)
        self.kwargs['event'].commit(**kwargs)


class EventManagerSave(EventManager):
    order = EVENT_MANAGER_ORDER_AFTER

    def _commit(self):
        if self.created:
            if 'created' in self.kwargs:
                kwargs = self.get_event_arguments(
                    argument_map=self.kwargs['created']
                )
                self.kwargs['created']['event'].commit(**kwargs)
        else:
            if 'edited' in self.kwargs:
                kwargs = self.get_event_arguments(
                    argument_map=self.kwargs['edited']
                )
                self.kwargs['edited']['event'].commit(**kwargs)

    def prepare(self):
        self.created = not self.instance.pk
