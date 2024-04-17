from django.utils.translation import gettext_lazy as _

from mayan.settings.literals import (
    MAYAN_WORKER_A_CONCURRENCY, MAYAN_WORKER_A_MAX_MEMORY_PER_CHILD,
    MAYAN_WORKER_A_MAX_TASKS_PER_CHILD, MAYAN_WORKER_A_NICE_LEVEL,
    MAYAN_WORKER_B_CONCURRENCY, MAYAN_WORKER_B_MAX_MEMORY_PER_CHILD,
    MAYAN_WORKER_B_MAX_TASKS_PER_CHILD, MAYAN_WORKER_B_NICE_LEVEL,
    MAYAN_WORKER_C_CONCURRENCY, MAYAN_WORKER_C_MAX_MEMORY_PER_CHILD,
    MAYAN_WORKER_C_MAX_TASKS_PER_CHILD, MAYAN_WORKER_C_NICE_LEVEL,
    MAYAN_WORKER_D_CONCURRENCY, MAYAN_WORKER_D_MAX_MEMORY_PER_CHILD,
    MAYAN_WORKER_D_MAX_TASKS_PER_CHILD, MAYAN_WORKER_D_NICE_LEVEL,
    MAYAN_WORKER_E_CONCURRENCY, MAYAN_WORKER_E_MAX_MEMORY_PER_CHILD,
    MAYAN_WORKER_E_MAX_TASKS_PER_CHILD, MAYAN_WORKER_E_NICE_LEVEL
)

from .classes import Worker

worker_a = Worker(
    concurrency=MAYAN_WORKER_A_CONCURRENCY,
    description=_(message='Low latency high volume tasks'),
    label=('Worker A'),
    maximum_memory_per_child=MAYAN_WORKER_A_MAX_MEMORY_PER_CHILD,
    maximum_tasks_per_child=MAYAN_WORKER_A_MAX_TASKS_PER_CHILD,
    name='worker_a', nice_level=MAYAN_WORKER_A_NICE_LEVEL
)
worker_b = Worker(
    concurrency=MAYAN_WORKER_B_CONCURRENCY,
    description=_(message='Medium latency tasks'), label=('Worker B'),
    maximum_memory_per_child=MAYAN_WORKER_B_MAX_MEMORY_PER_CHILD,
    maximum_tasks_per_child=MAYAN_WORKER_B_MAX_TASKS_PER_CHILD,
    name='worker_b', nice_level=MAYAN_WORKER_B_NICE_LEVEL
)
worker_c = Worker(
    concurrency=MAYAN_WORKER_C_CONCURRENCY,
    description=_(message='Medium latency tasks'), label=('Worker C'),
    maximum_memory_per_child=MAYAN_WORKER_C_MAX_MEMORY_PER_CHILD,
    maximum_tasks_per_child=MAYAN_WORKER_C_MAX_TASKS_PER_CHILD,
    name='worker_c', nice_level=MAYAN_WORKER_C_NICE_LEVEL
)
worker_d = Worker(
    concurrency=MAYAN_WORKER_D_CONCURRENCY,
    description=_(message='Low latency, long lived tasks'),
    label=('Worker D'),
    maximum_memory_per_child=MAYAN_WORKER_D_MAX_MEMORY_PER_CHILD,
    maximum_tasks_per_child=MAYAN_WORKER_D_MAX_TASKS_PER_CHILD,
    name='worker_d', nice_level=MAYAN_WORKER_D_NICE_LEVEL
)
worker_e = Worker(
    concurrency=MAYAN_WORKER_E_CONCURRENCY,
    description=_(message='Low latency, long lived tasks'),
    label=('Worker E'),
    maximum_memory_per_child=MAYAN_WORKER_E_MAX_MEMORY_PER_CHILD,
    maximum_tasks_per_child=MAYAN_WORKER_E_MAX_TASKS_PER_CHILD,
    name='worker_e', nice_level=MAYAN_WORKER_E_NICE_LEVEL
)
