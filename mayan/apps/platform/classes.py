import os
from pathlib import Path

from django.conf import settings
from django.template import loader
from django.template.base import Template
from django.template.context import Context
from django.urls import include, re_path
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from mayan.apps.backends.classes import BaseBackend
from mayan.apps.common.menus import menu_tools
from mayan.apps.common.serialization import yaml_dump, yaml_load
from mayan.apps.task_manager.classes import Worker
from mayan.settings.literals import (
    DEFAULT_DATABASE_NAME, DEFAULT_DATABASE_PASSWORD, DEFAULT_DATABASE_USER,
    DEFAULT_DIRECTORY_INSTALLATION, DEFAULT_ELASTICSEARCH_PASSWORD,
    DEFAULT_KEYCLOAK_ADMIN, DEFAULT_KEYCLOAK_ADMIN_PASSWORD,
    DEFAULT_KEYCLOAK_DATABASE_HOST, DEFAULT_KEYCLOAK_DATABASE_NAME,
    DEFAULT_KEYCLOAK_DATABASE_PASSWORD, DEFAULT_KEYCLOAK_DATABASE_USERNAME,
    DEFAULT_OS_USERNAME, DEFAULT_RABBITMQ_PASSWORD, DEFAULT_RABBITMQ_USER,
    DEFAULT_RABBITMQ_VHOST, DEFAULT_REDIS_PASSWORD,
    DEFAULT_USER_SETTINGS_FOLDER, DOCKER_DIND_IMAGE_VERSION,
    DOCKER_ELASTIC_IMAGE_NAME, DOCKER_ELASTIC_IMAGE_TAG,
    DOCKER_IMAGE_MAYAN_NAME, DOCKER_IMAGE_MAYAN_TAG,
    DOCKER_KEYCLOAK_IMAGE_NAME, DOCKER_KEYCLOAK_IMAGE_TAG,
    DOCKER_KEYCLOAK_POSTGRES_IMAGE_NAME, DOCKER_KEYCLOAK_POSTGRES_IMAGE_TAG,
    DOCKER_LINUX_IMAGE_VERSION, DOCKER_MYSQL_IMAGE_VERSION,
    DOCKER_POSTGRESQL_IMAGE_NAME, DOCKER_POSTGRESQL_IMAGE_TAG,
    DOCKER_RABBITMQ_IMAGE_NAME, DOCKER_RABBITMQ_IMAGE_TAG,
    DOCKER_REDIS_IMAGE_NAME, DOCKER_REDIS_IMAGE_TAG,
    DOCKER_TRAEFIK_IMAGE_NAME, DOCKER_TRAEFIK_IMAGE_TAG,
    GITLAB_CI_BRANCH_BUILDS_DOCKER, GITLAB_CI_BRANCH_BUILDS_DOCUMENTATION,
    GITLAB_CI_BRANCH_BUILDS_PYTHON, GITLAB_CI_BRANCH_DEPLOYMENTS_DEMO,
    GITLAB_CI_BRANCH_DEPLOYMENTS_STAGING,
    GITLAB_CI_BRANCH_RELEASES_ALL_MAJOR,
    GITLAB_CI_BRANCH_RELEASES_ALL_MINOR,
    GITLAB_CI_BRANCH_RELEASES_DOCKER_MAJOR,
    GITLAB_CI_BRANCH_RELEASES_DOCKER_MINOR,
    GITLAB_CI_BRANCH_RELEASES_DOCUMENTATION,
    GITLAB_CI_BRANCH_RELEASES_NIGHTLY,
    GITLAB_CI_BRANCH_RELEASES_PYTHON_MAJOR,
    GITLAB_CI_BRANCH_RELEASES_PYTHON_MINOR,
    GITLAB_CI_BRANCH_RELEASES_STAGING, GITLAB_CI_BRANCH_RELEASES_TESTING,
    GITLAB_CI_BRANCH_TESTS_ALL, GITLAB_CI_BRANCH_TESTS_DOCKER,
    GITLAB_CI_BRANCH_TESTS_PYTHON_ALL, GITLAB_CI_BRANCH_TESTS_PYTHON_BASE,
    GITLAB_CI_BRANCH_TESTS_PYTHON_UPGRADE, GUNICORN_LIMIT_REQUEST_LINE,
    GUNICORN_MAX_REQUESTS, GUNICORN_REQUESTS_JITTER, GUNICORN_TIMEOUT,
    GUNICORN_WORKER_CLASS, GUNICORN_WORKERS
)

from .settings import (
    setting_client_backend_arguments, setting_client_backend_enabled
)
from .utils import load_env_file


class ClientBackend(BaseBackend):
    _loader_module_name = 'client_backends'

    @classmethod
    def get_backend_instance(cls, name):
        backend_class = cls.get(name=name)
        kwargs = setting_client_backend_arguments.value.get(
            name, {}
        )
        return backend_class(**kwargs)

    @classmethod
    def post_load_modules(cls):
        cls.register_url_patterns()
        cls.register_links()
        cls.launch_backends()

    @classmethod
    def launch_backends(cls):
        for backend_name in setting_client_backend_enabled.value:
            cls.get_backend_instance(name=backend_name).launch()

    @classmethod
    def register_links(cls):
        for backend_name in setting_client_backend_enabled.value:
            backend_instance = cls.get_backend_instance(name=backend_name)
            menu_tools.bind_links(
                links=backend_instance.get_links()
            )

    @classmethod
    def register_url_patterns(cls):
        # Hidden import.
        from .urls import urlpatterns

        for backend_name in setting_client_backend_enabled.value:
            backend_instance = cls.get_backend_instance(name=backend_name)

            top_url = '{}/'.format(
                getattr(
                    backend_instance, '_url_namespace',
                    backend_instance.__class__.__name__
                )
            )

            urlpatterns += (
                re_path(
                    route=r'^{}'.format(top_url), view=include(
                        backend_instance.get_url_patterns()
                    )
                ),
            )

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def get_links(self):
        return ()


class Variable:
    def __init__(self, name, default, environment_name):
        self.name = name
        self.default = default
        self.environment_name = environment_name

    def _get_value(self):
        return os.environ.get(self.environment_name, self.default)

    def get_value(self):
        return mark_safe(
            s=self._get_value()
        )


class YAMLVariable(Variable):
    def _get_value(self):
        value = os.environ.get(self.environment_name)
        if value:
            value = yaml_load(stream=value)
        else:
            value = self.default

        return yaml_dump(
            data=value, allow_unicode=True, default_flow_style=True,
            width=999
        ).replace('...\n', '').replace('\n', '')


class PlatformTemplate:
    _registry = {}
    context = {}
    context_defaults = {}
    label = None
    name = None
    settings = None
    template_name = None
    template_string = None
    variables = None

    @classmethod
    def all(cls):
        return cls._registry.values()

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def register(cls, klass):
        cls._registry[klass.name] = klass

    def __str__(self):
        return str(
            self.get_label()
        )

    def get_context(self):
        return self.context

    def get_context_defaults(self):
        return self.context_defaults

    def get_label(self):
        return self.label or self.name

    def get_settings_context(self):
        result = {}
        for setting in self.settings or ():
            if setting.value:
                result[setting.global_name] = setting.value

        return result

    def get_template_name(self):
        return self.template_name or 'platform/{}.tmpl'.format(self.name)

    def get_variables_context(self):
        result = {}
        for variable in self.variables or ():
            result[variable.name] = variable.get_value()

        return result

    def render(self, context_string=None):
        """
        context_string allows the management command to pass context to this
        method as a JSON string
        """
        context = {}

        context.update(
            self.get_context_defaults()
        )
        context.update(
            self.get_settings_context()
        )
        context.update(
            self.get_variables_context()
        )
        # get_context goes last to server as the override
        context.update(
            self.get_context()
        )

        if context_string:
            context.update(
                yaml_load(stream=context_string)
            )

        if self.template_string:
            template = Template(template_string=self.template_string)
            return template.render(
                context=Context(dict_=context)
            )
        else:
            return loader.render_to_string(
                context=context, template_name=self.get_template_name()
            )


class PlatformTemplateDockerEntrypoint(PlatformTemplate):
    label = _(message='Template for entrypoint.sh file inside a Docker image.')
    name = 'docker_entrypoint'
    template_name = 'platform/docker/entrypoint.tmpl'

    def get_context(self):
        context = load_env_file()
        context.update(
            {
                'workers': Worker.all()
            }
        )
        return context


class PlatformTemplateDockerComposefile(PlatformTemplate):
    label = _(message='Template that generates the Docker Compose file.')
    name = 'docker_docker_compose'
    template_name = 'platform/docker/docker-compose.yml.tmpl'

    def __init__(self):
        self.variables = (
            Variable(
                name='DEFAULT_DATABASE_NAME',
                default=DEFAULT_DATABASE_NAME,
                environment_name='MAYAN_DEFAULT_DATABASE_NAME'
            ),
            Variable(
                name='DEFAULT_DATABASE_PASSWORD',
                default=DEFAULT_DATABASE_PASSWORD,
                environment_name='MAYAN_DEFAULT_DATABASE_PASSWORD'
            ),
            Variable(
                name='DEFAULT_DATABASE_USER',
                default=DEFAULT_DATABASE_USER,
                environment_name='MAYAN_DEFAULT_DATABASE_USER'
            ),
            Variable(
                name='DEFAULT_ELASTICSEARCH_PASSWORD',
                default=DEFAULT_ELASTICSEARCH_PASSWORD,
                environment_name='MAYAN_DEFAULT_ELASTICSEARCH_PASSWORD'
            ),
            Variable(
                name='DEFAULT_KEYCLOAK_ADMIN',
                default=DEFAULT_KEYCLOAK_ADMIN,
                environment_name='MAYAN_DEFAULT_KEYCLOAK_ADMIN'
            ),
            Variable(
                name='DEFAULT_KEYCLOAK_ADMIN_PASSWORD',
                default=DEFAULT_KEYCLOAK_ADMIN_PASSWORD,
                environment_name='MAYAN_DEFAULT_KEYCLOAK_ADMIN_PASSWORD'
            ),
            Variable(
                name='DEFAULT_KEYCLOAK_DATABASE_HOST',
                default=DEFAULT_KEYCLOAK_DATABASE_HOST,
                environment_name='MAYAN_DEFAULT_KEYCLOAK_DATABASE_HOST'
            ),
            Variable(
                name='DEFAULT_KEYCLOAK_DATABASE_NAME',
                default=DEFAULT_KEYCLOAK_DATABASE_NAME,
                environment_name='MAYAN_DEFAULT_KEYCLOAK_DATABASE_NAME'
            ),
            Variable(
                name='DEFAULT_KEYCLOAK_DATABASE_PASSWORD',
                default=DEFAULT_KEYCLOAK_DATABASE_PASSWORD,
                environment_name='MAYAN_DEFAULT_KEYCLOAK_DATABASE_PASSWORD'
            ),
            Variable(
                name='DEFAULT_KEYCLOAK_DATABASE_USERNAME',
                default=DEFAULT_KEYCLOAK_DATABASE_USERNAME,
                environment_name='MAYAN_DEFAULT_KEYCLOAK_DATABASE_USERNAME'
            ),
            Variable(
                name='DEFAULT_RABBITMQ_PASSWORD',
                default=DEFAULT_RABBITMQ_PASSWORD,
                environment_name='MAYAN_DEFAULT_RABBITMQ_PASSWORD'
            ),
            Variable(
                name='DEFAULT_RABBITMQ_USER',
                default=DEFAULT_RABBITMQ_USER,
                environment_name='MAYAN_DEFAULT_RABBITMQ_USER'
            ),
            Variable(
                name='DEFAULT_RABBITMQ_VHOST',
                default=DEFAULT_RABBITMQ_VHOST,
                environment_name='MAYAN_DEFAULT_RABBITMQ_VHOST'
            ),
            Variable(
                name='DEFAULT_REDIS_PASSWORD',
                default=DEFAULT_REDIS_PASSWORD,
                environment_name='MAYAN_DEFAULT_REDIS_PASSWORD'
            ),
            Variable(
                name='DOCKER_ELASTIC_IMAGE_NAME',
                default=DOCKER_ELASTIC_IMAGE_NAME,
                environment_name='MAYAN_DOCKER_ELASTIC_IMAGE_NAME'
            ),
            Variable(
                name='DOCKER_ELASTIC_IMAGE_TAG',
                default=DOCKER_ELASTIC_IMAGE_TAG,
                environment_name='MAYAN_DOCKER_ELASTIC_IMAGE_TAG'
            ),
            Variable(
                name='DOCKER_IMAGE_MAYAN_NAME',
                default=DOCKER_IMAGE_MAYAN_NAME,
                environment_name='MAYAN_DOCKER_IMAGE_MAYAN_NAME'
            ),
            Variable(
                name='DOCKER_IMAGE_MAYAN_TAG',
                default=DOCKER_IMAGE_MAYAN_TAG,
                environment_name='MAYAN_DOCKER_IMAGE_MAYAN_TAG'
            ),
            Variable(
                name='DOCKER_KEYCLOAK_IMAGE_NAME',
                default=DOCKER_KEYCLOAK_IMAGE_NAME,
                environment_name='MAYAN_DOCKER_KEYCLOAK_IMAGE_NAME'
            ),
            Variable(
                name='DOCKER_KEYCLOAK_IMAGE_TAG',
                default=DOCKER_KEYCLOAK_IMAGE_TAG,
                environment_name='MAYAN_DOCKER_KEYCLOAK_IMAGE_TAG'
            ),
            Variable(
                name='DOCKER_KEYCLOAK_POSTGRES_IMAGE_NAME',
                default=DOCKER_KEYCLOAK_POSTGRES_IMAGE_NAME,
                environment_name='MAYAN_DOCKER_KEYCLOAK_POSTGRES_IMAGE_NAME'
            ),
            Variable(
                name='DOCKER_KEYCLOAK_POSTGRES_IMAGE_TAG',
                default=DOCKER_KEYCLOAK_POSTGRES_IMAGE_TAG,
                environment_name='MAYAN_DOCKER_KEYCLOAK_POSTGRES_IMAGE_TAG'
            ),
            Variable(
                name='DOCKER_POSTGRESQL_IMAGE_NAME',
                default=DOCKER_POSTGRESQL_IMAGE_NAME,
                environment_name='MAYAN_DOCKER_POSTGRESQL_IMAGE_NAME'
            ),
            Variable(
                name='DOCKER_POSTGRESQL_IMAGE_TAG',
                default=DOCKER_POSTGRESQL_IMAGE_TAG,
                environment_name='MAYAN_DOCKER_POSTGRESQL_IMAGE_TAG'
            ),
            Variable(
                name='DOCKER_RABBITMQ_IMAGE_NAME',
                default=DOCKER_RABBITMQ_IMAGE_NAME,
                environment_name='MAYAN_DOCKER_RABBITMQ_IMAGE_NAME'
            ),
            Variable(
                name='DOCKER_RABBITMQ_IMAGE_TAG',
                default=DOCKER_RABBITMQ_IMAGE_TAG,
                environment_name='MAYAN_DOCKER_RABBITMQ_IMAGE_TAG'
            ),
            Variable(
                name='DOCKER_REDIS_IMAGE_NAME',
                default=DOCKER_REDIS_IMAGE_NAME,
                environment_name='MAYAN_DOCKER_REDIS_IMAGE_NAME'
            ),
            Variable(
                name='DOCKER_REDIS_IMAGE_TAG',
                default=DOCKER_REDIS_IMAGE_TAG,
                environment_name='MAYAN_DOCKER_REDIS_IMAGE_TAG'
            ),
            Variable(
                name='DOCKER_TRAEFIK_IMAGE_NAME',
                default=DOCKER_TRAEFIK_IMAGE_NAME,
                environment_name='MAYAN_DOCKER_TRAEFIK_IMAGE_NAME'
            ),
            Variable(
                name='DOCKER_TRAEFIK_IMAGE_TAG',
                default=DOCKER_TRAEFIK_IMAGE_TAG,
                environment_name='MAYAN_DOCKER_TRAEFIK_IMAGE_TAG'
            ),
        )


class PlatformTemplateDockerSupervisord(PlatformTemplate):
    label = _(message='Template for Supervisord inside a Docker image.')
    name = 'docker_supervisord'
    template_name = 'platform/docker/supervisord.tmpl'

    def get_context(self):
        return {
            'OS_USERNAME': DEFAULT_OS_USERNAME,
            'autorestart': 'false',
            'shell_path': '/bin/sh',
            'stderr_logfile': '/dev/fd/2',
            'stderr_logfile_maxbytes': '0',
            'stdout_logfile': '/dev/fd/1',
            'stdout_logfile_maxbytes': '0',
            'workers': Worker.all()
        }


class PlatformTemplateDockerfile(PlatformTemplate):
    label = _(message='Template that generates a Dockerfile file.')
    name = 'docker_dockerfile'
    template_name = 'platform/docker/dockerfile.tmpl'

    def __init__(self):
        self.variables = (
            Variable(
                name='DOCKER_LINUX_IMAGE_VERSION',
                default=DOCKER_LINUX_IMAGE_VERSION,
                environment_name='MAYAN_DOCKER_LINUX_IMAGE_VERSION'
            ),
        )


class PlatformTemplateGitLabCI(PlatformTemplate):
    label = _(message='Template that generates a GitLab CI config file.')
    name = 'gitlab-ci'

    def __init__(self):
        self.variables = (
            Variable(
                name='DEFAULT_DATABASE_NAME',
                default=DEFAULT_DATABASE_NAME,
                environment_name='MAYAN_DEFAULT_DATABASE_NAME'
            ),
            Variable(
                name='DEFAULT_DATABASE_PASSWORD',
                default=DEFAULT_DATABASE_PASSWORD,
                environment_name='MAYAN_DEFAULT_DATABASE_PASSWORD'
            ),
            Variable(
                name='DEFAULT_DATABASE_USER',
                default=DEFAULT_DATABASE_USER,
                environment_name='MAYAN_DEFAULT_DATABASE_USER'
            ),
            Variable(
                name='DOCKER_DIND_IMAGE_VERSION',
                default=DOCKER_DIND_IMAGE_VERSION,
                environment_name='MAYAN_DOCKER_DIND_IMAGE_VERSION'
            ),
            Variable(
                name='DOCKER_LINUX_IMAGE_VERSION',
                default=DOCKER_LINUX_IMAGE_VERSION,
                environment_name='MAYAN_DOCKER_LINUX_IMAGE_VERSION'
            ),
            Variable(
                name='DOCKER_MYSQL_IMAGE_VERSION',
                default=DOCKER_MYSQL_IMAGE_VERSION,
                environment_name='MAYAN_DOCKER_MYSQL_IMAGE_VERSION'
            ),
            Variable(
                name='DOCKER_POSTGRESQL_IMAGE_NAME',
                default=DOCKER_POSTGRESQL_IMAGE_NAME,
                environment_name='MAYAN_DOCKER_POSTGRESQL_IMAGE_NAME'
            ),
            Variable(
                name='DOCKER_POSTGRESQL_IMAGE_TAG',
                default=DOCKER_POSTGRESQL_IMAGE_TAG,
                environment_name='MAYAN_DOCKER_POSTGRESQL_IMAGE_TAG'
            ),
            Variable(
                name='GITLAB_CI_BRANCH_BUILDS_DOCKER',
                default=GITLAB_CI_BRANCH_BUILDS_DOCKER,
                environment_name='MAYAN_GITLAB_CI_BRANCH_BUILDS_DOCKER'
            ),
            Variable(
                name='GITLAB_CI_BRANCH_BUILDS_DOCUMENTATION',
                default=GITLAB_CI_BRANCH_BUILDS_DOCUMENTATION,
                environment_name='MAYAN_GITLAB_CI_BRANCH_BUILDS_DOCUMENTATION'
            ),
            Variable(
                name='GITLAB_CI_BRANCH_BUILDS_PYTHON',
                default=GITLAB_CI_BRANCH_BUILDS_PYTHON,
                environment_name='MAYAN_GITLAB_CI_BRANCH_BUILDS_PYTHON'
            ),
            Variable(
                name='GITLAB_CI_BRANCH_DEPLOYMENTS_DEMO',
                default=GITLAB_CI_BRANCH_DEPLOYMENTS_DEMO,
                environment_name='MAYAN_GITLAB_CI_BRANCH_DEPLOYMENTS_DEMO'
            ),
            Variable(
                name='GITLAB_CI_BRANCH_DEPLOYMENTS_STAGING',
                default=GITLAB_CI_BRANCH_DEPLOYMENTS_STAGING,
                environment_name='MAYAN_GITLAB_CI_BRANCH_DEPLOYMENTS_STAGING'
            ),
            Variable(
                name='GITLAB_CI_BRANCH_RELEASES_ALL_MAJOR',
                default=GITLAB_CI_BRANCH_RELEASES_ALL_MAJOR,
                environment_name='MAYAN_GITLAB_CI_BRANCH_RELEASES_ALL_MAJOR'
            ),
            Variable(
                name='GITLAB_CI_BRANCH_RELEASES_ALL_MINOR',
                default=GITLAB_CI_BRANCH_RELEASES_ALL_MINOR,
                environment_name='MAYAN_GITLAB_CI_BRANCH_RELEASES_ALL_MINOR'
            ),
            Variable(
                name='GITLAB_CI_BRANCH_RELEASES_DOCKER_MAJOR',
                default=GITLAB_CI_BRANCH_RELEASES_DOCKER_MAJOR,
                environment_name='MAYAN_GITLAB_CI_BRANCH_RELEASES_DOCKER_MAJOR'
            ),
            Variable(
                name='GITLAB_CI_BRANCH_RELEASES_DOCKER_MINOR',
                default=GITLAB_CI_BRANCH_RELEASES_DOCKER_MINOR,
                environment_name='MAYAN_GITLAB_CI_BRANCH_RELEASES_DOCKER_MINOR'
            ),
            Variable(
                name='GITLAB_CI_BRANCH_RELEASES_DOCUMENTATION',
                default=GITLAB_CI_BRANCH_RELEASES_DOCUMENTATION,
                environment_name='MAYAN_GITLAB_CI_BRANCH_RELEASES_DOCUMENTATION'
            ),
            Variable(
                name='GITLAB_CI_BRANCH_RELEASES_NIGHTLY',
                default=GITLAB_CI_BRANCH_RELEASES_NIGHTLY,
                environment_name='MAYAN_GITLAB_CI_BRANCH_RELEASES_NIGHTLY'
            ),
            Variable(
                name='GITLAB_CI_BRANCH_RELEASES_PYTHON_MAJOR',
                default=GITLAB_CI_BRANCH_RELEASES_PYTHON_MAJOR,
                environment_name='MAYAN_GITLAB_CI_BRANCH_RELEASES_PYTHON_MAJOR'
            ),
            Variable(
                name='GITLAB_CI_BRANCH_RELEASES_PYTHON_MINOR',
                default=GITLAB_CI_BRANCH_RELEASES_PYTHON_MINOR,
                environment_name='MAYAN_GITLAB_CI_BRANCH_RELEASES_PYTHON_MINOR'
            ),
            Variable(
                name='GITLAB_CI_BRANCH_RELEASES_STAGING',
                default=GITLAB_CI_BRANCH_RELEASES_STAGING,
                environment_name='MAYAN_GITLAB_CI_BRANCH_RELEASES_STAGING'
            ),
            Variable(
                name='GITLAB_CI_BRANCH_RELEASES_TESTING',
                default=GITLAB_CI_BRANCH_RELEASES_TESTING,
                environment_name='MAYAN_GITLAB_CI_BRANCH_RELEASES_TESTING'
            ),
            Variable(
                name='GITLAB_CI_BRANCH_TESTS_ALL',
                default=GITLAB_CI_BRANCH_TESTS_ALL,
                environment_name='MAYAN_GITLAB_CI_BRANCH_TESTS_ALL'
            ),
            Variable(
                name='GITLAB_CI_BRANCH_TESTS_DOCKER',
                default=GITLAB_CI_BRANCH_TESTS_DOCKER,
                environment_name='MAYAN_GITLAB_CI_BRANCH_TESTS_DOCKER'
            ),
            Variable(
                name='GITLAB_CI_BRANCH_TESTS_PYTHON_ALL',
                default=GITLAB_CI_BRANCH_TESTS_PYTHON_ALL,
                environment_name='MAYAN_GITLAB_CI_BRANCH_TESTS_PYTHON_ALL'
            ),
            Variable(
                name='GITLAB_CI_BRANCH_TESTS_PYTHON_BASE',
                default=GITLAB_CI_BRANCH_TESTS_PYTHON_BASE,
                environment_name='MAYAN_GITLAB_CI_BRANCH_TESTS_PYTHON_BASE'
            ),
            Variable(
                name='GITLAB_CI_BRANCH_TESTS_PYTHON_UPGRADE',
                default=GITLAB_CI_BRANCH_TESTS_PYTHON_UPGRADE,
                environment_name='MAYAN_GITLAB_CI_BRANCH_TESTS_PYTHON_UPGRADE'
            )
        )


class PlatformTemplateSupervisord(PlatformTemplate):
    label = _(message='Template for Supervisord.')
    name = 'supervisord'

    def __init__(self):
        self.variables = (
            Variable(
                name='GUNICORN_REQUESTS_JITTER',
                default=GUNICORN_REQUESTS_JITTER,
                environment_name='MAYAN_GUNICORN_REQUESTS_JITTER'
            ),
            Variable(
                name='GUNICORN_LIMIT_REQUEST_LINE',
                default=GUNICORN_LIMIT_REQUEST_LINE,
                environment_name='MAYAN_GUNICORN_GUNICORN_LIMIT_REQUEST_LINE'
            ),
            Variable(
                name='GUNICORN_MAX_REQUESTS',
                default=GUNICORN_MAX_REQUESTS,
                environment_name='MAYAN_GUNICORN_MAX_REQUESTS'
            ),
            Variable(
                name='GUNICORN_TIMEOUT',
                default=GUNICORN_TIMEOUT,
                environment_name='MAYAN_GUNICORN_TIMEOUT'
            ),
            Variable(
                name='GUNICORN_WORKER_CLASS',
                default=GUNICORN_WORKER_CLASS,
                environment_name='MAYAN_GUNICORN_WORKER_CLASS'
            ),
            Variable(
                name='GUNICORN_WORKERS',
                default=GUNICORN_WORKERS,
                environment_name='MAYAN_GUNICORN_WORKERS'
            ),
            Variable(
                name='GUNICORN_TIMEOUT',
                default=GUNICORN_TIMEOUT,
                environment_name='MAYAN_GUNICORN_TIMEOUT'
            ),
            Variable(
                name='INSTALLATION_PATH',
                default=DEFAULT_DIRECTORY_INSTALLATION,
                environment_name='MAYAN_INSTALLATION_PATH'
            ),
            Variable(
                name='OS_USERNAME', default=DEFAULT_OS_USERNAME,
                environment_name='MAYAN_OS_USERNAME'
            ),
            Variable(
                name='USER_SETTINGS_FOLDER',
                default=DEFAULT_USER_SETTINGS_FOLDER,
                environment_name='MAYAN_USER_SETTINGS_FOLDER'
            ),
            YAMLVariable(
                name='MEDIA_ROOT', default=settings.MEDIA_ROOT,
                environment_name='MAYAN_MEDIA_ROOT'
            )
        )

    def get_context(self):
        *_, user_settings_folder, media_root = self.variables

        return {
            'autorestart': 'true',
            'shell_path': '/bin/sh',
            'user_settings_folder': Path(
                media_root.get_value()
            ) / user_settings_folder.get_value(),
            'workers': Worker.all()
        }


class PlatformTemplateWorkerQueues(PlatformTemplate):
    label = _(message='Template showing the queues of a worker.')
    name = 'worker_queues'

    variables = (
        Variable(
            name='WORKER_NAME', default=None,
            environment_name='MAYAN_WORKER_NAME'
        ),
    )

    def get_context(self):
        worker_name = self.get_variables_context().get('WORKER_NAME')
        try:
            queues = Worker.get(name=worker_name).queues
        except KeyError:
            raise KeyError(
                'Worker name "{}" not found.'.format(worker_name)
            )

        return {
            'queues': queues, 'queue_names': sorted(
                map(lambda x: x.name, queues)
            )
        }


PlatformTemplate.register(klass=PlatformTemplateDockerEntrypoint)
PlatformTemplate.register(klass=PlatformTemplateDockerComposefile)
PlatformTemplate.register(klass=PlatformTemplateDockerSupervisord)
PlatformTemplate.register(klass=PlatformTemplateDockerfile)
PlatformTemplate.register(klass=PlatformTemplateGitLabCI)
PlatformTemplate.register(klass=PlatformTemplateSupervisord)
PlatformTemplate.register(klass=PlatformTemplateWorkerQueues)
