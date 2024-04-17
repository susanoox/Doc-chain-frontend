from django.utils.translation import gettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_e

queue_search = CeleryQueue(
    label=_(message='Search'), name='search', worker=worker_e
)
queue_search_slow = CeleryQueue(
    label=_(message='Search slow'), name='search_slow', worker=worker_e
)

queue_search.add_task_type(
    dotted_path='mayan.apps.dynamic_search.tasks.task_deindex_instance',
    label=_(message='Remove a model instance from the search engine.'),
    name='task_deindex_instance'
)
queue_search.add_task_type(
    dotted_path='mayan.apps.dynamic_search.tasks.task_index_instance',
    label=_(message='Index a model instance to the search engine.'),
    name='task_index_instance'
)
queue_search.add_task_type(
    dotted_path='mayan.apps.dynamic_search.tasks.task_index_instances',
    label=_(message='Index all instances of a search model to the search engine.'),
    name='task_index_instances'
)
queue_search.add_task_type(
    dotted_path='mayan.apps.dynamic_search.tasks.task_index_related_instance_m2m',
    label=_(
        'Index all related instances of a search model after a many to many '
        'event.'
    ),
    name='task_index_related_instance_m2m'
)

queue_search_slow.add_task_type(
    dotted_path='mayan.apps.dynamic_search.tasks.task_reindex_backend',
    label=_(message='Reset the search backend indices and index all instances again.'),
    name='task_reindex_backend'
)
