#!/usr/bin/env python

import os
import sys

from dateutil import parser
import sh

import django
from django.template import Template, Context
from django.utils.encoding import force_str

sys.path.insert(
    0, os.path.abspath('..')
)
sys.path.insert(
    1, os.path.abspath('.')
)

import mayan  # NOQA
from mayan.settings import BASE_DIR as mayan_base_dir  # NOQA
from mayan.settings import literals  # NOQA

try:
    BUILD = sh.Command('git').bake('describe', '--tags', '--always', 'HEAD')
    DATE = sh.Command('git').bake('--no-pager', 'log', '-1', '--format=%cd')
except sh.CommandNotFound:
    BUILD = None
    DATE = None

BASE_DIR = os.path.join(mayan_base_dir, '..')
REQUIREMENTS_FILE = 'requirements.txt'
SETUP_TEMPLATE = 'setup.py.tmpl'
MAYAN_TEMPLATE = '__init__.py.tmpl'


def generate_build_number():
    if BUILD and DATE:
        try:
            result = '{}_{}'.format(
                BUILD(), DATE()
            ).replace('\n', '')
        except sh.ErrorReturnCode_128:
            result = ''
    else:
        result = ''
    return result


def generate_commit_timestamp():
    datetime = parser.parse(
        force_str(
            s=DATE()
        )
    )
    return datetime.strftime('%y%m%d%H%M')


def get_requirements(base_directory, filename):
    result = []

    file_requirements = os.path.join(base_directory, filename)

    with open(file=file_requirements) as file_object:
        for line in file_object:
            if line.startswith('-r'):
                line = line.split('\n')[0][3:]
                directory, filename = os.path.split(line)
                result.extend(
                    get_requirements(
                        base_directory=os.path.join(
                            base_directory, directory
                        ), filename=filename
                    )
                )
            elif not line.startswith('\n'):
                result.append(
                    line.split('\n')[0]
                )

    return result


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mayan.settings')
    django.setup()

    requirements = get_requirements(
        base_directory=BASE_DIR, filename=REQUIREMENTS_FILE
    )

    with open(file=SETUP_TEMPLATE) as file_object:
        template = file_object.read()
        result = Template(template).render(
            context=Context(
                {'requirements': requirements}
            )
        )

    with open(file='setup.py', mode='w') as file_object:
        file_object.write(result)

    with open(file=MAYAN_TEMPLATE) as file_object:
        template = file_object.read()

        # Ignore local version if any
        upstream_version = '.'.join(
            mayan.__version__.split('+')[0].split('.')
        )

        local_version = getattr(literals, 'LOCAL_VERSION')

        if local_version:
            version_final = '{}+{}'.format(upstream_version, local_version)
        else:
            version_final = upstream_version

        upstream_build = '0x{:06X}'.format(mayan.__build__)

        result = Template(template).render(
            context=Context(
                {
                    'build': upstream_build,
                    'build_string': generate_build_number(),
                    'django_series': literals.DJANGO_SERIES,
                    'timestamp': generate_commit_timestamp(),
                    'version': version_final
                }
            )
        )

    with open(file=os.path.join(BASE_DIR, 'mayan', '__init__.py'), mode='w') as file_object:
        file_object.write(result)
