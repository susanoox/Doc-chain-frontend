import logging
import sys
import uuid

from django.utils.translation import gettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig

from .backends.base import LockingBackend
from .literals import COMMAND_NAME_LOCK_MANAGER_PURGE_LOCKS, TEST_LOCK_NAME
from .settings import setting_backend

logger = logging.getLogger(name=__name__)


class LockManagerApp(MayanAppConfig):
    has_tests = True
    name = 'mayan.apps.lock_manager'
    verbose_name = _(message='Lock manager')

    def ready(self):
        super().ready()

        if COMMAND_NAME_LOCK_MANAGER_PURGE_LOCKS not in sys.argv:
            logger.debug('Starting lock backend connectivity test')
            # Don't test for locks during the `task_manager_purge_locks`
            # command as there may be some stuck locks which will block
            # the command.
            lock_name = '{}-{}'.format(
                TEST_LOCK_NAME, uuid.uuid4()
            )
            lock_instance = LockingBackend.get_backend()
            try:
                lock = lock_instance.acquire_lock(
                    name=lock_name, timeout=1
                )
            except Exception as exception:
                raise RuntimeError(
                    'Error initializing the locking backend: {}; {}'.format(
                        setting_backend.value, exception
                    )
                ) from exception
            else:
                lock.release()
