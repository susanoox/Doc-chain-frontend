from django.utils.translation import gettext_lazy as _

DEFAULT_EVENT_LIST_EXPORT_FILENAME = 'events_list.csv'

DEFAULT_EVENTS_DISABLE_ASYNCHRONOUS_MODE = False

EVENT_MANAGER_ORDER_AFTER = 1
EVENT_MANAGER_ORDER_BEFORE = 2

EVENT_TYPE_NAMESPACE_NAME = 'events'
EVENT_EVENTS_CLEARED_NAME = 'event_cleared'
EVENT_EVENTS_EXPORTED_NAME = 'event_exported'

TEXT_UNKNOWN_EVENT_ID = _(message='Unknown or obsolete event type: %s')
