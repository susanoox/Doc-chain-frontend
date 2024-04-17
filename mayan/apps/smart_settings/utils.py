import errno
import functools
import os

import yaml

from mayan.apps.common.serialization import yaml_load
from mayan.apps.templating.classes import Template

from .literals import (
    CONFIGURATION_FILENAME, CONFIGURATION_FILENAME_LAST_GOOD
)


class SettingNamespaceSingleton:
    """
    Self hosting bootstrap setting class.
    Allow managing setting in a compatible way before Mayan EDMS starts.
    """
    _setting_kwargs = {}
    _setting_overrides = {}
    _settings = {}

    class SettingNotFound(Exception):
        """Mostly a stand-in or typecast for KeyError for readability."""

    @classmethod
    def load_config_file(cls, filepath):
        try:
            with open(file=filepath) as file_object:
                file_object.seek(0, os.SEEK_END)
                if file_object.tell():
                    file_object.seek(0)
                    try:
                        return yaml_load(stream=file_object)
                    except yaml.YAMLError as exception:
                        exit(
                            'Error loading configuration file: {}; {}'.format(
                                filepath, exception
                            )
                        )
        except IOError as exception:
            if exception.errno == errno.ENOENT:
                # No config file, return empty dictionary
                return {}
            else:
                raise

    @classmethod
    def register_setting(cls, name, klass, kwargs=None):
        cls._settings[name] = klass
        cls._setting_kwargs[name] = kwargs or {}

    def __init__(self, global_symbol_table):
        self.global_symbol_table = global_symbol_table
        self.settings = {}

        for name, klass in self.__class__._settings.items():
            kwargs = self.__class__._setting_kwargs[name].copy()
            kwargs['name'] = name
            setting = klass(**kwargs)
            setting.namespace = self
            self.settings[name] = setting

    @functools.cache
    def get_config_file_content(self):
        filepath = self.get_setting_value(
            name='CONFIGURATION_FILEPATH'
        )

        return self.load_config_file(filepath=filepath) or {}

    def get_setting(self, name):
        return self.settings[name]

    def get_setting_value(self, name):
        """
        Wrapper that calls the individual setting .get_value method.
        Convenience method to allow returning setting values from the
        namespace.
        """
        try:
            setting = self.get_setting(name=name)
        except KeyError:
            raise SettingNamespaceSingleton.SettingNotFound
        else:
            return setting.get_value()

    def get_values(self, only_critical=False):
        """
        Return a dictionary will all the settings and their respective
        resolved values.
        """
        result = {}
        for name, setting in self.settings.items():
            # If only_critical is set to True load only the settings with
            # the critical flag. Otherwise load all.
            if only_critical and setting.critical or not only_critical:
                try:
                    result[name] = setting.get_value()
                except SettingNamespaceSingleton.SettingNotFound:
                    """
                    Not critical, we just avoid adding it to the result
                    dictionary.
                    """
                except Exception as exception:
                    exit(
                        'Unable to load bootstrap setting; {}'.format(
                            exception
                        )
                    )

        return result

    def update_globals(self, global_symbol_table=None, only_critical=False):
        """
        Insert all resolved values into the symbol table of the caller.
        """
        result = self.get_values(only_critical=only_critical)

        if global_symbol_table is None:
            global_symbol_table = self.global_symbol_table

        global_symbol_table.update(result)


class BaseSetting:
    @staticmethod
    def safe_string_value_to_string(value):
        return value.encode('utf-8').decode()

    def __init__(
        self, name, critical=False, default_value=None,
        has_default=False
    ):
        self.critical = critical
        self.default_value = default_value
        self.has_default = has_default
        self.name = name

    def _get_value(self):
        """
        By default will try to get the value from the namespace symbol table,
        then the configuration file, and finally from the environment.
        """
        # Resolution order
        # 1 - Environment
        # 2 - Config
        # 3 - Global
        # 4 - Default
        try:
            return self.load_value_from_environment()
        except SettingNamespaceSingleton.SettingNotFound:
            try:
                return self.load_value_from_config_file()
            except SettingNamespaceSingleton.SettingNotFound:
                try:
                    return self.load_value_from_global_system_table()
                except KeyError:
                    if self.has_default:
                        return self.get_default_value()
                    else:
                        raise SettingNamespaceSingleton.SettingNotFound

    def get_default_value(self):
        return self.default_value

    def get_environment_name(self):
        return 'MAYAN_{}'.format(self.name)

    def get_template_environment_name(self):
        return 'MAYAN_{}'.format(
            self.get_template_name()
        )

    def get_template_name(self):
        return 'SETTING_TEMPLATE_{}'.format(self.name)

    def get_template_string(self):
        try:
            return self.get_template_string_from_environment()
        except KeyError:
            try:
                return self.get_template_string_from_config_file()
            except KeyError:
                return self.get_template_string_from_global_system_table()

    def get_template_string_from_config_file(self):
        self.namespace.get_config_file_content()[
            self.get_template_name()
        ]

    def get_template_string_from_environment(self):
        return os.environ[
            self.get_template_environment_name()
        ]

    def get_template_string_from_global_system_table(self):
        return self.namespace.global_symbol_table[
            self.get_template_name()
        ]

    def get_value(self):
        try:
            return self.namespace._setting_overrides[self.name]
        except KeyError:
            try:
                template_string = self.get_template_string()
            except KeyError:
                return self._get_value()
            else:
                setting_template = Template(template_string=template_string)
                context = {}
                context.update(self.namespace.global_symbol_table)
                context.update(
                    self.namespace.get_config_file_content()
                )
                context.update(os.environ)

                value = setting_template.render(context=context)
                value = BaseSetting.safe_string_value_to_string(value=value)

                return value

    def load_value_from_config_file(self):
        try:
            return self.namespace.get_config_file_content()[self.name]
        except KeyError:
            raise SettingNamespaceSingleton.SettingNotFound

    def load_value_from_environment(self):
        try:
            value = os.environ[
                self.get_environment_name()
            ]
        except KeyError:
            raise SettingNamespaceSingleton.SettingNotFound
        else:
            try:
                return yaml_load(stream=value)
            except yaml.YAMLError as exception:
                raise ValueError(
                    'Error loading setting environment variable "{}", '
                    'value: "{}"; {}'.format(
                        self.name, value, exception
                    )
                )

    def load_value_from_global_system_table(self):
        return self.namespace.global_symbol_table[self.name]

    def set_value(self, value):
        self.namespace._setting_overrides[self.name] = value


class FilesystemBootstrapSetting(BaseSetting):
    def __init__(self, name, critical=False, path_parts=None):
        self.critical = critical
        self.has_default = True
        self.name = name
        self.path_parts = path_parts

    def _get_value(self):
        """
        It is not possible to look for this setting in the config file
        because not even the config file setup has completed.
        This setting only supports being set from the environment.
        """
        try:
            return self.load_value_from_environment()
        except SettingNamespaceSingleton.SettingNotFound:
            if self.has_default:
                return self.get_default_value()
            else:
                raise SettingNamespaceSingleton.SettingNotFound

    def get_default_value(self):
        """
        The default value of this setting class is not static but calculated.
        """
        # Can't use BASE_DIR from django.conf.settings.
        # Use it from the `global_symbol_table` which should be the
        # same.
        try:
            BASE_DIR = self.namespace._setting_overrides['MEDIA_ROOT']
        except KeyError:
            BASE_DIR = self.namespace.global_symbol_table.get(
                'MEDIA_ROOT', self.namespace.global_symbol_table['BASE_DIR']
            )

        return os.path.join(BASE_DIR, *self.path_parts)

    def get_template_string(self):
        try:
            return self.get_template_string_from_environment()
        except KeyError:
            return self.get_template_string_from_global_system_table()


class MediaBootstrapSetting(FilesystemBootstrapSetting):
    def get_default_value(self):
        """
        The default value of this setting class is not static but calculated.
        """
        return os.path.join(
            self.namespace.get_setting_value(name='MEDIA_ROOT'),
            *self.path_parts
        )


def smart_yaml_load(value):
    if isinstance(value, dict):
        return value
    else:
        return yaml_load(
            stream=value or '{}'
        )


# FilesystemBootstrapSetting settings

SettingNamespaceSingleton.register_setting(
    klass=MediaBootstrapSetting, kwargs={
        'critical': True, 'path_parts': (CONFIGURATION_FILENAME,)
    }, name='CONFIGURATION_FILEPATH'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, kwargs={
        'critical': True, 'has_default': True, 'default_value': False
    }, name='CONFIGURATION_FILE_IGNORE'
)

# MediaBootstrapSetting settings

SettingNamespaceSingleton.register_setting(
    klass=MediaBootstrapSetting, kwargs={
        'critical': True, 'path_parts': (CONFIGURATION_FILENAME_LAST_GOOD,)
    }, name='CONFIGURATION_LAST_GOOD_FILEPATH'
)
SettingNamespaceSingleton.register_setting(
    klass=FilesystemBootstrapSetting, kwargs={
        'critical': True, 'path_parts': ('media',)
    }, name='MEDIA_ROOT'
)

# Normal settings

SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, kwargs={
        'has_default': True,
        'default_value': ['127.0.0.1', 'localhost', '[::1]']
    }, name='ALLOWED_HOSTS'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, name='APPEND_SLASH'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, name='AUTH_PASSWORD_VALIDATORS'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, name='AUTHENTICATION_BACKENDS'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting,
    kwargs={
        'has_default': True,
        'default_value': False
    }, name='CSRF_COOKIE_SECURE'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting,
    kwargs={
        'has_default': True,
        'default_value': []
    }, name='CSRF_TRUSTED_ORIGINS'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting,
    kwargs={
        'has_default': True,
        'default_value': False
    }, name='CSRF_USE_SESSIONS'
)
SettingNamespaceSingleton.register_setting(
    name='DATA_UPLOAD_MAX_MEMORY_SIZE', klass=BaseSetting,
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, kwargs={
        'has_default': True, 'default_value': None
    }, name='DATABASES'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, kwargs={
        'has_default': True, 'default_value': False
    }, name='DEBUG'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, name='DEFAULT_FROM_EMAIL'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, name='DISALLOWED_USER_AGENTS'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, name='EMAIL_BACKEND'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, name='EMAIL_HOST'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, name='EMAIL_HOST_PASSWORD'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, name='EMAIL_HOST_USER'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, name='EMAIL_PORT'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, name='EMAIL_TIMEOUT'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, name='EMAIL_USE_SSL'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, name='EMAIL_USE_TLS'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, name='FILE_UPLOAD_MAX_MEMORY_SIZE'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, kwargs={
        'has_default': True, 'default_value': ['127.0.0.1']
    }, name='INTERNAL_IPS'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, kwargs={
        'has_default': True, 'default_value': 'common:home'
    }, name='LOGIN_REDIRECT_URL'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, kwargs={
        'has_default': True, 'default_value': 'authentication:login_view'
    }, name='LOGIN_URL'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, kwargs={
        'has_default': True, 'default_value': 'authentication:login_view'
    }, name='LOGOUT_REDIRECT_URL'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, name='LANGUAGES'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, name='LANGUAGE_CODE'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, name='SESSION_COOKIE_NAME'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, name='SESSION_ENGINE'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, name='STATIC_URL'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, name='STORAGES',
    kwargs={
        'has_default': True, 'default_value': {}
    }
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, name='TIME_ZONE'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, name='WSGI_APPLICATION'
)

# Celery

SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, kwargs={
        'has_default': True, 'default_value': True
    }, name='CELERY_TASK_ALWAYS_EAGER'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, name='CELERY_BROKER_LOGIN_METHOD'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, kwargs={
        'has_default': True, 'default_value': 'memory://'
    }, name='CELERY_BROKER_URL'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, name='CELERY_BROKER_USE_SSL'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, name='CELERY_RESULT_BACKEND'
)

# Mayan

SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, kwargs={
        'has_default': True, 'default_value': False
    }, name='COMMON_DISABLE_LOCAL_STORAGE'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, kwargs={
        'critical': True, 'has_default': True, 'default_value': ()
    }, name='COMMON_DISABLED_APPS'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, kwargs={
        'critical': True, 'has_default': True, 'default_value': ()
    }, name='COMMON_EXTRA_APPS'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, kwargs={
        'critical': True, 'has_default': True, 'default_value': ()
    }, name='COMMON_EXTRA_APPS_PRE'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, kwargs={
        'has_default': True, 'default_value': None
    }, name='DATABASE_ENGINE'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, kwargs={
        'has_default': True, 'default_value': None
    }, name='DATABASE_NAME'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, kwargs={
        'has_default': True, 'default_value': None
    }, name='DATABASE_USER'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, kwargs={
        'has_default': True, 'default_value': None
    }, name='DATABASE_PASSWORD'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, kwargs={
        'has_default': True, 'default_value': None
    }, name='DATABASE_HOST'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, kwargs={
        'has_default': True, 'default_value': None
    }, name='DATABASE_PORT'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, kwargs={
        'has_default': True, 'default_value': 0
    }, name='DATABASE_CONN_MAX_AGE'
)
SettingNamespaceSingleton.register_setting(
    klass=BaseSetting, kwargs={
        'has_default': True, 'default_value': False
    }, name='TESTING'
)
