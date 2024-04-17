4.6.3 (2024-03-28)
==================
- Merge changes from 4.5.11.
- Add path support to the URL class.
- Fix document print and password reset templates.
- Fix display of build number.

4.6.2 (2024-03-04)
==================
- Add clamav to the makefile ``setup-dev-operating-system-packages`` target.
- Update the Debian Docker image from 12.4-slim to 12.5-slim.
- Move the flanker dependency from the sources to the source_emails app.
- Update dependency versions:

  - redis from 5.0.1 to 5.0.2.
  - django from 4.2.10 to 4.2.11.
  - ruff from 0.2.1 to 0.3.0.
  - sentry-sdk from 1.40.1 to 1.40.6.
  - jsonschema from 4.20.0 to 4.21.1.
  - extract-msg from 0.47.0 to 0.48.0.

4.6.1 (2024-02-07)
==================
- Merge changes from versions 4.5.9 and 4.4.12.
- Update dependency versions:

  - django from 4.2.8 to 4.2.10 due to CVE-2024-24680.
  - django-mptt from 0.15.0 to 0.16.0.
  - importlib-metadata from 6.8.0 to 7.0.1.
  - pycountry from 22.3.5 to 23.12.11.
  - django-silk from 5.0.4 to 5.1.0.
  - ruff from 0.2.1 to 0.1.6.
  - jstree from 3.3.16. 3.3.12.
  - django-solo from 2.1.0 to 2.2.0.
  - pytz from 2023.3.post1 to 2024.1.
  - greenlet from 3.0.1 to 3.0.3.
  - sentry-sdk from 1.40.0 to 1.40.1.
  - psutil from 5.9.6 to 5.9.8.
  - sphinx from 4.5.0 to 5.3.0.
  - sphinx_rtd_theme from 0.5.2 to 2.0.0.

- Code style updates.

  - Sort imports
  - Collapse long import lines
  - Expand import lines that are too short
  - Fix variable names

- Update translation files.
- Fix sources app class method name.
- Fix typos.

4.6 (2024-01-11)
================
- Improve the index mirroring profile. Add ``MAYAN_MIRROR_INDEX_NAME`` to
  allow mounting different indexes without modifying the Docker Compose
  file.
- Refactor the smart settings app. Setting value changes no longer take
  effect immediately or trigger saving the configuration file. Added a new
  view to save the current settings into a new configuration file. Setting
  post edit functions are now execute during startup and not after editing
  the setting. Added a new view and link to revert unsaved settings.
- Override the test runner's logging setup to avoid having its output
  being concatenated when calling management commands and makefile targets.
- Add ``ruff`` dependency, version 0.1.6.
- Update dependency versions:

  - Docker

    - Debian image from 12.1-slim to 12.2-slim.

  - JavaScript

    - jQuery from version 3.6.0 to 3.7.1.

  - Python

    - Update use of ``psycopg2`` version to 2.x to ``psycopg`` version 3.1.14.
    - AMQP from 5.1.0 to 5.2.0.
    - PIP from 23.2.1 to 23.3.2.
    - Add the Django series version to the setup generation script.
    - ``django-test-migrations`` from 1.1.0 to 1.3.0.
    - ``redis`` from 4.6.0 to 5.0.1.
    - ``wheel`` from 0.41.0 to 0.42.0.
    - ``bleach`` from 6.0.0 to 6.1.0.
    - ``django-auth-ldap`` from 4.4.0 to 4.6.0.
    - ``mozilla-django-oidc`` from 2.0.0 to 3.0.0.
    - ``pyotp`` from 2.6.0 to 2.9.0.
    - ``django-solo`` from 2.0.0 to 2.1.0.
    - ``django`` from 3.2 to 4.2.8.
    - ``django-mptt`` from 0.14.0 to 0.15.0.
    - ``sh`` from 2.0.4 to 2.0.6.
    - ``django-debug-toolbar`` from 3.2.4 to 4.2.0.
    - ``django-rosetta`` from 0.9.9 to 0.10.0.
    - ``django-silk`` from 5.0.3 to 5.0.3.
    - ``ipython`` from 8.14.0 to 8.18.1.
    - ``Pillow`` from 10.0.0 to 10.2.0.
    - ``pypdf`` from 3.14.0 to 3.17.1.
    - ``qrcode`` from 7.3.1 to 7.4.2.
    - ``node-semver`` from 0.8.1 to 0.9.0.
    - ``python_gnupg`` from 0.4.8 to 0.4.9.
    - ``graphviz`` from 0.17 to 0.20.1.
    - ``dateparser`` from 1.1.8 to 1.2.0.
    - ``pytz`` from 2022 to 2023.3.post1.
    - ``gevent`` from 22.10.2 to 23.9.1.
    - ``greenlet`` from 2.0.2 to 3.0.1.
    - ``sentry-sdk`` from 1.29.0 to 1.38.0.
    - ``whitenoise`` from 6.5.0 to 6.6.0.
    - ``django-cors-headers`` from 4.2.0 to 4.3.1.
    - ``jsonschema`` from 4.18.0 to 4.20.0.
    - ``CairoSVG`` from 2.5.2 to 2.7.1.
    - ``boto3`` from 1.28.16 to 1.33.7.
    - ``django-storages`` from 1.13.2 to 1.14.2.
    - ``extract-msg`` from 0.37.1 to 0.46.2.
    - ``pycryptodome`` from 3.18.0 to 3.19.0.
    - ``celery`` from 5.3.5 to 5.3.6.
    - ``coverage`` from 5.5 to 6.5.0.
    - ``coveralls`` from 3.2.0 to 3.3.1.
    - ``psutil`` from 5.8.0 to 5.9.6.
    - ``django-widget-tweaks`` from 1.4.12 to 1.5.0.

- Refactor file metadata app:

  - Allow multiple drivers to execute for the same MIME types.
  - Automatically find and import file metadata drivers.
  - Add a normalized internal name field for file metadata drive attributes.
    This solves the issue where attributes with spaces were not usable
    in templates. Spaces are converted into underscores. Uppercase letters
    in attributes are converted to lowercase.
  - Existing file metadata template references need to be updated for
    attribute letter casing.
  - Add view to display all detected file metadata drivers.
  - Process all file metadata drivers as parallel background tasks.

- Add antivirus scanning for documents. Implemented as a file metadata
  driver and a new app named ``file_metadata_clamav``. ClamAV and the latest
  database are included in the Docker image.
- Support source column resolution for non model subclasses.
- Convert the Docker Compose file into a platform template.
- Generate unique test lock names to avoid unintended lock errors when
  validating the lock manager backend. Closes GitLab issue #1157, thanks
  to Mathias Behrle (@mbehrle) for the report.
- Commit the event "document version edited" when a document version pages
  are remapped.
- Normalize the permission system to work with single permissions per filter
  or check.
- Mailer app refactor

  - Replace uses of ``mailer`` and ``user mailer`` to ``mailing profile``.
  - Add mailing profile API.
  - Add generic object mailing API. Supports emailing object links and
    object attachments.
  - Add class ``ModelMailingAction`` to defined available mailing actions
    per model.
  - Use the ``__title__`` and ``__website__`` from the ``mayan`` module
    as the email's body project name and website.

- Move file metadata queue to worker D.
- Update minimum and recommended requirements.
- Lower the severity of searching indexing problems to ``INFO``. This
  reduces user confusion between normal messages when processing the
  asynchronous task queue and actual coding errors.
- Expose Django's setting named ``CSRF_TRUSTED_ORIGINS`` via the smart
  settings app.
- Expose Django's setting named ``CSRF_COOKIE_SECURE`` via the smart
  settings app.
- Expose Django's setting named ``CSRF_USE_SESSIONS`` via the smart
  settings app.
- Optimize document type retention policy queries.
- Minor optimization to the ACL calculation queries.
- Fix search query warning when parsing dates. Default all date values the
  timezone UTC.
- Convert worker nice levels from literals to config constants.
- Optimize the file cache eviction selection.
- Convert the Docker Compose Keycloak services into a platform template.
- Check if database tables are available before preloading and caching
  permissions and file metadata drivers.
- Use the correct ``post_load_modules`` method to execute initialization
  code after app module loading.
- Reorganize make files. Remove unused and outdated targets. Move all Docker
  related targets to the Docker make file. Improve staging targets.
- Reorganize templates:

  - Unify the blocks ``content`` and ``content_plain``.
  - Show the logo in the login form.
  - Move the logo font to the ``head`` template.
  - Split templates into small components.
  - Move templates into sub-folders and shorten their names.

- Fix double separator in the user menu.
- Theme updates.
- Switch from Apache 2.0 to GPL 2.0 license.

4.5.11 (2024-03-28)
===================
- Ensure credentials ``post_processing`` method is called.
- Fix periodic source document type field to use the intended Select2 widget.
- Fix workflow transition field model typo.
- Merge changes from version 4.4.14.
- Fix MSG file uncompressed uploads.
- Add additional sources migrations for users that skipped the previous
  migrations during the upgrade.
- Fine tune the commit of the credential used event.
- Lower the severity of searching indexing problems to ``INFO``. This
  reduces user confusion between normal messages when processing the
  asynchronous task queue and actual coding errors.

4.5.10 (2024-03-03)
===================
- Include changes from version 4.4.13.
- Minor code style fixes.
- Fix typos.
- Updated the download file API to handle anonymous user gracefully.
- Update Docker container image versions:

  - Debian from 12.4-slim to 12.5-slim
  - PostgreSQL from 13.12-alpine to 13.13-alpine
  - Python from 3.11.7-slim to 3.11.8-slim
  - RabbitMQ from 3.12.12-alpine to 3.12.13-alpine

- Test updates:

  - Remove more direct uses of ``values_list``.
  - Remove more direct imports of base test mixins.
  - Sort test mixins.
  - Testing style updates.

- Update Django from version 3.2.23 to 3.2.24.

4.5.9 (2024-02-05)
==================
- Minor query optimizations.
- Changes from version 4.4.12.
- Update dependency version:

  - django-test-migrations from 1.1.0 to 1.3.0.
  - pypdf from 3.14.0 to 3.17.4 due to CVE-2023-46250.
  - safety from 2.3.5 to 3.0.1.

- Don't raise an error if a form view has no form defined. This can be the
  case for dynamic forms based on ACL where the current user has no access
  for any of the fields.
- Complete the changes started in version 4.5 to normalize how the
  project/installation title and URL are calculated. The setting
  ``COMMON_PROJECT_URL`` is now removed as its intended purpose is now
  performed by the settings ``ORGANIZATIONS_INSTALLATION_URL`` and
  ``ORGANIZATIONS_URL_BASE_PATH``. This change also fixes the title of the
  REST API documentation showing the text 'None' when the
  ``COMMON_PROJECT_TITLE`` setting was left to its default value.
- Update Docker image tags:

  - debian from 12.2-slim to 12.4-slim.
  - elastic from 7.17.9 to 7.17.17.
  - keycloak from 20.0.1 to 20.0.5-0.
  - postgresql from 13.11-alpine to 13.13-alpine.
  - python from 3.11.4-slim to 3.11.7-slim.
  - rabbitmq from 3.12.2-alpine to 3.12.12-alpine.
  - redis from 7.0.12-alpine to 7.0.15-alpine.

4.5.8 (2023-12-07)
==================
- Code style fixes.
- Add sanity check to ``DynamicFormBackendMixin`` to ensure form
  definition dictionaries are not mangled but copied instead.
- Update the Debian Docker base image from version debian:12.1-slim to
  debian:12.2-slim.
- Update Django from version 3.2.22 to 3.2.23.
- Add missing mailing profile ``default`` field to creation and edit forms.
- Fix Django file based mailer.
- Replace hard coded mailer ``object_name`` with model verbose introspection.
- Support Django series in setup generation script.
- Update translation files.

4.5.7 (2023-10-25)
==================
- Fix select2 widget in the metadata edit workflow action form.
- Remove obsolete example settings from the default ``.env`` file.
- Migrate chapters to Knowledge base:

  - Appearance troubleshooting
  - Authentication troubleshooting
  - Autoadmin troubleshooting
  - Documents troubleshooting
  - Docker troubleshooting
  - Dynamic search syntax
  - File caching troubleshooting
  - Mirroring troubleshooting
  - Platform troubleshooting
  - Tags

- Add note explaining the direct deployment installation method is no longer
  supported.
- Merge version 4.4.9 changes.
- Load test mailers classes by path and not my import.
- Fix authenticated mailers. Add the mailer class method
  ``get_connection_kwargs`` to ensure each mailer prepares the corresponding
  connection arguments. In the case of the Django mailer, it decodes the
  stored credential ID back into a ``StoredCredential`` model instance and
  extract the username and password from the credential before merging the
  values into the super connection arguments.

4.5.6 (2023-10-12)
==================
- Fix editing existing metadata workflow actions.
- Update the Docker image ``entrypoint.sh`` to skip changing the ownership
  of files if ``MAYAN_COMMON_DISABLE_LOCAL_STORAGE`` is set to any truthy
  value (True, true, T, t, Yes, yes, Y, y, 1).

4.5.5 (2023-10-06)
==================
- Move periodic task import checking to the task manager app and condition
  it to the debug or testing environments.
- Update Django from version 3.2.20 to 3.2.22.
- Migrate REST API sections to Knowledge base.
- Migrate the sources chapter to the Knowledge base.
- Migrate metadata chapter to Knowledge base.
- Ensure that no two document versions are set as active at the same time,
  even when bypassing the ``set_active`` method. Close GitLab issue #1158
  thanks to Mathias Behrle (@mbehrle) for the report.

4.5.4 (2023-10-04)
==================
- Docker builder updates. Improve how caches and proxies are calculated.
  Add support for Docker image mirroring.
- Support runtime source action execution logic. Add method
  ``get_allow_action_execute`` to provide each source control to allow or
  ignore action execution.
- Support invalid characters in Docker username. Support invalid CI
  characters like "$" such as those generated by Harbor for robot accounts.
- Improve email testing code.
- Fix dry run value interpretation for periodic sources. Fixes clean up of
  email, watch folder, and watch storage sources.

4.5.3 (2023-09-30)
==================
- Fix periodic task creation used for periodic sources. Add migration to fix
  previously created sources.
- Migrate documentations chapters:

  - OCR
  - Workflows
  - Storage

4.5.2 (2023-09-20)
==================
- Fix sources attempting to uncompress non compressed files.
- Add migrations to fix incorrect source backend paths.

4.5.1 (2023-09-15)
==================
- Fix the default Docker Compose Mayan EDMS image tag for version 3.5.
- Fix migration of existing document sources.
- Fix the ``add_file`` method for the ``TarArchive`` class.
- Fix the workflow template preview issue.

4.5 (2023-09-12)
================
- Increase the size of the document indexing value field from 128 to 255
  characters.
- Rename all uses of "superuser" to "super user" or "super_user".
- Ignore staging folder file image cache error if the image cache is not
  already generated when deleting the staging folder file.
- Update the Debian Docker image from version 11.5-slim to 11.6-slim.
- Ensure the workflow state action column is not shown for the workflow
  state runtime proxies where is does not make sense to show.
- Add escalation list column to workflow states list view.
- Workflow preview updates:

  - Change the symbol to identify transitions, actions, and escalations with
    conditions from the math arrow to a math symbol for function (fn of).
  - Add escalations to the workflow preview.
  - Include escalation hash changes to invalidate workflow previews.

- Add super user column to user list view.
- Simplify and optimize the document indexing feature.
- Ensure deleted documents are removed from indexes even if the index is
  disabled.
- Split HTML widgets modules into HTMl and column widget modules.
- Extract the workflow state action model into its own model module.
- Separate workflow state action model data and business logic code.
- Update the type of the document file size field to a
  ``PositiveBigIntegerField`` to allow tracking document files bigger than
  2GB in quota queries.
- Add the ``multi_container`` profile. Allows easy switching from a single
  all-in-one container Docker Compose deployment to a multi container
  deployment.
- Improve template initialization to support custom tag loading. Closes
  GitLab issue #1135. Thanks to Alexander Schlüter (@alexschlueter) for the
  request and implementation suggestion.
- Update the cache and cache partition purge loop to continue executing even
  when there are files that cannot be purged. Cache partition files will be
  skipped and retried on the next purge execution.
- Update the stale shared uploaded file and download file deletion loop to
  continue executing even when there are files that cannot be deleted.
  Remaining skipped files will be retried on the next iteration.
- Setting updates:

  - Add a setting named ``CONFIGURATION_FILE_IGNORE`` which cause the setting
    system to not load settings from the ``config.yml`` file or save the
    current configuration to the ``config_backup.yml`` file.
  - Custom cache implementation removed in favor of Python's
    ``functools.cache``.
  - Add a ``set_value`` method to allow overriding a bootstrap setting's
    value.
  - Support passing a ``global_symbol_table`` argument when updating the
    setting namespace global symbol table.

- Create a temporary ``MEDIA_ROOT`` folder when running tests. This change
  allows further isolation of testing artifacts.
- Add support for document download message templating. This allows
  customizing the message users receive when their document or document
  bundle is ready for download.
- Add download file area API views. This API allows listing, deleting, and
  download actions.
- Support local versions. Added explicit support for pep-0440 local version
  labels for custom builds.
- Add support for per document type document stub pruning. This change adds
  the document type fields ``document_stub_pruning_enabled``,
  ``document_stub_expiration_interval``, and removes the setting
  ``DOCUMENTS_STUB_EXPIRATION_INTERVAL`` which is now configured per
  document type. All references of document type deletion policies are
  renamed to document type retention policies. By default pruning of document
  stubs is enabled to preserve the existing behavior. Disabling document
  stub pruning can be used to support document archiving where the
  document files are deleted but the document database information is kept
  for reference. Thanks to forum user @legosiv for the request and use case.
- Update the file cache ``maximum_size`` field from a ``BigIntegerField`` to
  a ``PositiveBigIntegerField``.
- Workflow app updates:

  - Show the transition in the workflow template state escalation list view.
  - Ensure only correct transitions can be select for the workflow template
    state escalation in the user interface and the API.
  - Speed up tests.
  - Split test modules.
  - Rename test mixin classes to comply with naming conventions.
  - Add missing workflow template state escalation view tests.

- On small screens, close main menu when clicking on links. Closes GitLab
  issue #1113. Thanks to BW (@bwakkie) for the report.
- Improve version checking:

  - Add support for comparing versions.
  - Display version numbers when reporting version mismatches.
  - Add a new exception when the local version is more recent than the
    upstream one. Closes Gitlab issue #1037. Thanks to Bw (@bwakkie) for
    the request.

- Sources refactor:

  - Split sources app into separate apps per source type.
  - Add staging storage and watch storage sources.
  - Consolidate specific source backend functionality into reusable mixins.
  - Add fieldsets to the source backend setup forms.
  - Add support for single or multiple document API uploads.
  - Refactor source dynamic backend form system.
  - Merge ``SourceBackend`` and ``SourceMixin`` classes.
  - Split dynamic backend form code into ``DynamicFormBackendMixin``
    class.
  - Add ``setup_form`` prefix to the dynamic field methods to specify
    that these act on the setup and not the upload form.

- Improve task manager app.

  - Add worker, queue, and task type list views.
  - Add source column help texts.
  - Remove unused `sources_fast` queue.
  - Increase default maximum worker tasks by 10x.

- Add check named ``check_app_tests`` to ensure Mayan apps tests flag matches
  the actual state of the app's tests.
- Replace local version parsing code with wrapper for the Python ``packaging``
  library. Add support to extract and manipulate more parts of the version
  string like the pre-release and post release parts.
- Update the active version and latest file attributes of documents to be
  stored fields instead of computed values.
- Release exporter updates:

  - Use pathlib for internal path computations.
  - Remove bbcode support.
  - Simplify code to not require Mayan or Django.
  - Support configurate release directory location.

- Add icon class support to layers.
- Add credentials app. This app provides a centralized location to store and
  protect external authentication credentials. By default two credential
  backends are provided: token, username and password. The credential
  backend system is extensible and other credential systems can be added.

  Apps that use external authentication, like the mailer and sources, were
  updated to use credentials in their setup forms. In the case of features
  that use optional external credentials or where the credentials are the
  result of a template, like the HTTP workflow action, staging storage
  source, and watch storage source, the credential is selected and passed
  as a variable to the template.
- Mark cache model field ``maximum_size`` as a database index to speed up
  cache calculations.
- Add file caching dashboard administrator widgets.
- Add container dependency to ensure containers are started only after the
  ``setup_or_upgrade`` containers finishes.
- Move ``EventManager`` classes to their own module.
- Update event system to work in asynchronous mode.
- Add the ``EVENTS_DISABLE_ASYNCHRONOUS_MODE`` settings to revert the events
  system back to synchronous mode.
- Split events queue into two queues for fast and slow tasks.
- Create document file pages and document version pages in bulk.
- Increase the default maximum memory per Celery worker child from 300000
  to 400000.
- Add new worker E and devote it for search tasks.
- Eliminate the shared "Tools" queue. Each app is now responsible of defining
  its own queue for slow tasks.
- Re-balance tasks queues.
- Remove the unused signal ``signal_post_document_created``.
- Remove the options ``--without-gossip`` and ``--without-heartbeat`` from
  the ``run_worker`` script.
- Add support for changing the worker log level via the new environment
  variable ``MAYAN_WORKER_LOG_LEVEL`` which defaults to ``ERROR``.
- Replace PyPDF2 with the original pypdf package.
- Remove search many document level fields from document files, document file
  pages, document version, and document version pages.
- Support Django's ``CONN_MAX_AGE`` in Docker via the new environment
  variable ``MAYAN_DATABASE_CONN_MAX_AGE``.
- Support setting the RabbitMQ Docker hostname via the environment variable
  ``MAYAN_DOCKER_RABBITMQ_HOSTNAME``. Defaults to ``rabbitmq``.
- Update the document file deletion operation to be a background task.
- Move Debian base image to 12.1 "Bookworm",
- Update Docker image versions:

  - mysql from 8.0.32 to 8.0.34
  - debian from 11.7-slim to 12.1-slim
  - docker from version 20.10.21-dind to 23.10.6-dind
  - postgresql from 13.10-alpine to 13.11-alpine
  - python 3.10.11-slim to 3.11.4-slim
  - rabbitmq from 3.11.13-alpine to 3.12.2-alpine
  - redis from 7.0.10-alpine 7.0.12-alpine

- Update Python dependencies versions:

  - PIP from 22.2 to 23.2.1
  - Redis from 4.2.0 to 4.6.0
  - Wheel from 0.37.0 to 0.41.0
  - Bleach from 4.1.0 to 6.0.0
  - django-auth-ldap from 4.0.0 to 4.4.0
  - PyYAML from 6.0 to 6.0.1
  - importlib-metadata from 5.0.0 to 6.8.0
  - requests from 1.14.3 to 2.0.4
  - django-extensions from 3.1.5 to 3.2.3
  - django-rosetta from 0.9.8 to 0.9.9
  - django-silk from 4.3.0 to 5.0.3
  - flake8 from 4.0.1 to 6.1.0
  - ipython from 7.32.0 to .8.14.0
  - twine from 3.8.0 to 4.0.2
  - Pillow from 9.4.0 to 10.0.0
  - dateparser from 1.1.1 to 1.1.8
  - elasticsearch from 7.17.1 to 7.17.9
  - elasticsearch-dsl from 7.4.0 to 7.4.1
  - python-magic from 0.4.26 to 0.4.27
  - gunicorn from 20.1.0 to 21.2.0
  - sentry-sdk from 1.12.1 to 1.29.0
  - whitenoise from 6.2.0 to 6.5.0
  - django-cors-headers from 3.10.0 to 4.2.0
  - drf-yasg from 1.21.4 to 1.21.7
  - jsonschema from 4.4.0 to 4.18.0
  - swagger-spec-validator from 2.7.4 to 3.0.3
  - boto3 from 1.24.70 to 1.28.16
  - django-storages from 1.13.1 to 1.13.2
  - extract-msg from 0.36.4 to 0.37.1
  - pycryptodome from 3.10.4 to 3.18.0
  - celery from 5.2.7 to 5.3.1
  - django-celery-beat from 2.2.1 to 2.3.0
  - django-formtools from 2.3 to 2.4.1
  - psycopg2 from 2.9.3 to 2.9.6

- Update duplicate bulk creation to work in batches of 100 entries.
- Sources actions refactor:

  - Unify the sources action with new action, action
    interfaces and action interfaces argument classes.
  - The source action refactor converts source actions
    into reusable mixins.
  - Each action is responsible of supporting multiple
    interface types and the arguments for each
    interface.
  - Add watch storage source.
  - New API endpoints to inspect and execute the
    source actions.
  - Removal of the email metadata attachment support.
  - Removal of the email message attribute to metada
    support.
  - Update document and document file creation to
    happen in smaller units.
  - Update the SANE scanner source to perform the
    scan as a background task.
  - Update staging folder initial file copy to
    be a background task.

- Tweak the PostgreSQL container command arguments.
- Add a maximum Docker logging size for all Mayan EDMS containers.
- Split documents queue into more smaller queues.
- Move the duplicates queue to the C worker.
- Move document downloads and document exports to their own queues.
- Move the storage queue to the B worker.
- Improve how dependencies copyright and license information is extracted.
- Convert Dropzone.js to a Django widget for cleaner integration.
- Search form updates:

  - Add fieldsets to the search form to group search fields by model.
  - Hide the ``ID`` search fields.
  - Sort search fields by their translatable label.

- Show AJAX loading spinner in mobile devices. Closes GitLab issue #1140.
  Thanks to Arya Senna (@aryasenna) for the request.
- Update how the project title setting works. The code was updated to
  reflect the actual purpose of the setting which is to identify an
  installation and not to do rebranding.
- Ensure Tools and Setup view buttons are rendered with consistent heights.
- Docker Compose file updates:

  - Use the variable ``MAYAN_DOCKER_RABBITMQ_HOSTNAME`` as the default host
    for the Celery broker URL.
  - Make the Redis Celery result database configurable via
    ``MAYAN_REDIS_RESULT_DATABASE`` which default to ``1``.
  - Make the Mayan EDMS Redis lock database configurable via
    ``MAYAN_REDIS_LOCK_MANAGER_DATABASE`` which defaults to ``2``.
  - Add note regarding opening up RabbitMQ data port.

- Add ``ContentType`` API detail view.
- Add message warning that it is not possible to change password of
  staff or super user accounts.
- Add return links to the "Tools" and "Setup" areas to speed up navigation.
- Add improved test case tag inheritance.
- Sources metadata refactor:

  - Add source metadata support. The information about the
    creation of the document is now stored per source.
    To access this information a view and a property were
    added, ``{{ document.source_metadata_value_of.source_id }}``.
    By default all upload store the ID of the source used.
    Other backends like store more information like the sender,
    receiver, subject, message ID.
  - Refactor the document tasks callback interface. The tasks
    now accept a dictionary of all the callback and their
    information.
  - Move immediate mode into its own mixin.
  - Import all test sources by path.
  - Support running for a test label/tag from the make file
    with ``make test TAG=``.
  - Reduce the size of the secondary icon on
    ``FontAwesomeDualClassesDriver`` to make the source metadata
    icon more readable.

- Update source backend's ``get_upload_form_class`` to be an instance method
  and allow backends to dynamically change the form fields.
- Fix the compressed label still showing up when the uncompress choice
  is never or always.

- ``PropertyHelper`` updates:

  - Move all ``PropertyHelper`` usage to their own modules.
  - Add property helper ``file_metadata_value_of`` to document files.
  - Formalize ``PropertyHelper`` behaviors and testing. Closes GitLab
    issue #664. Thanks to Light Templar (@LightTemplar) for the report.
  - Tag all ``PropertyHelper`` with ``classes_property_helper``.

- Add document file introspection link and view. This view re-scans the
  document file and populates the size, checksum, and mimetype files. It also
  updates the document file page count and creates a new document version
  linking all discovered file pages. This view replaces the document file
  page count update view.
- Deleting a document file page will now also delete any document version
  page linked to it.
- New document versions create manually will not become active by default.
  Only new document versions created as a result of a document file upload
  will become active by default.
- Pass the source backend action to ``get_upload_form_class`` to allow more
  dynamic field changes based on the action too.
- Disable compressed document file uploads which are not longer supported.
- Ensure the Keycloak database name is the same as the Keycloak PostreSQL
  one.
- Rename all environment variables containing ``POSTGRES`` to use the full
  name ``POSTGRESQL``. These are: ``MAYAN_DOCKER_KEYCLOAK_POSTGRES_TAG``,
  ``MAYAN_KEYCLOAK_POSTGRES_VOLUME``, ``MAYAN_DOCKER_POSTGRES_IMAGE``,
  ``MAYAN_POSTGRES_VOLUME``.
- Upload wizard updates:

  - Support filtering of cabinet, metadata and tags during upload
    based on the access of the logged user.
  - Add support to disable the wizard next button when a required
    metadata type is not available to the user.
  - Split metadata test mixins.
  - Test improvements.
  - Preserve document creation user to allow quota tests to
    access the user uploading the document.

4.4.14 (2024-03-27)
===================
- Fix the document file and the user API list view ordering fields. The
  fields were ``mime_type`` to ``mimetype`` and remove
  ``has_usable_password`` which is a method and not a field.
- Restore the root logging handlers after every test.
- Allow the ``JavaScriptCatalogPublic`` sub class to bypass authentication
  and avoid JavaScript errors for non authenticated users.
- Update dependency versions:

  - Django from 3.2.23 to 3.2.25.
  - pytz from 2022.1 to 2024.1

4.4.13 (2024-03-01)
===================
- Update PIP from version 23.3.2 to 24.0.
- Fix source class and JavaScript ``MayanImage`` class ``.initialize()``
  method name.
- Fix typos and text formatting.
- Encapsulate MPTT exceptions as validation errors when users attempt
  to perform invalid index template node tree manipulations.
- Update ``DEFAULT_SEARCH_QUERY_RESULTS_LIMIT`` from 100000 to 10000 to
  workaround conflicting with ElasticSearch non scroll search limit.
- Minor code style fixes.
- Add an extra line to ``COMMON_EXTRA_APPS`` help text to clarify the apps
  inclusion order.
- Changed the internal variable name of ``COMMON_EXTRA_APPS_PRE`` to avoid
  possible conflicts.
- Add extra logging to report storage errors when deleting trashed documents
  as part of the retention policies.
- Minor test fixes.
- Fix workflow icon variable name.
- Replace distutils with setuptool.

  - Add setuptool as an explicit dependency.
  - Replace distutils with setuptools following the deprecation
    of distutils.
    https://docs.python.org/3.10/whatsnew/3.10.html#distutils-deprecated
  - Remove distutils from the Docker image.

- Update dependency versions:

  - sphinx from 4.5.0 to 5.3.0.
  - sphinx_rtd_theme from 0.5.2 to 2.0.0.

- Remove diagram generator markup. The library used to generate diagrams is
  not longer maintained and breaks after the last Pillow upgrade. Removed
  all diagram markup until a replacement can be found.
- Update the Debian Docker image from 11.8-slim to 11.9-slim.
- Separate code/template translation and JavaScript translation handling.
  Rename the app flag ``has_translations`` to ``has_app_translations``.
  Add the app flag ``has_javascript_translations`` which defaults to False.

4.4.12 (2024-02-03)
===================
- Translation file updates.
- Fix logging issue when unexpected cache file access problems are
  encountered.
- Backport minor query optimizations.
- Update dependency versions:

  - wheel from 0.37.0 to 0.42.0 due to CVE-2022-40898.
  - sentry-sdk from 1.12.1 to 1.40.0 due to CVE-2023-28117.
  - redis from 4.2.2 to 4.6.0 due to CVE-2023-28858.
  - pycryptodome from 3.10.4 to 3.20.0 due to PVE-2021-42084.
  - pip from 23.2.1 to 23.3.2 due to CVE-2023-5752.
  - dateparser from 1.1.1 to 1.2.0 due to PVE-2023-62361.
  - extract-msg from 0.36.4 to 0.47.0.
  - PyPDF2 from 1.28.4 to 1.28.6.
  - Pillow from 9.4.0 to 10.2.0 due to CVE-2023-44271.
  - twine from 3.8.0 to 4.0.2.
  - Update CairoSVG from 2.5.2 to 2.7.1 due to CVE-2023-27586.
  - ipython from 8.21.0 to 7.32.0 due to CVE-2023-24816.
  - amqp from 5.1.0 to 5.2.0.
  - flake8 from 4.0.1 to 7.0.0.

- Update the deprecated/removed Pillow constants:
  https://pillow.readthedocs.io/en/stable/deprecations.html#constants
  Replace ANTIALIASING with LANCZOS.

4.4.11 (2023-12-10)
===================
- Fix test asserts. Fix test that were asserting for True values instead of
  asserting for equality.
- Fix document file page search content field label.
- Continue purge loops even during errors. Update the cache and cache
  partition purge loop to continue executing even when there are files that
  cannot be purged. Cache partition files will be skipped and retried on the
  next purge execution.
- Code style fixes.

4.4.10 (2023-12-07)
===================
- Support Django series in setup generation script.
- Add missing mailing profile ``default`` field to creation and edit forms.
- Update dependencies:

  - Update Django from version 3.2.22 to 3.2.23.
  - ``redis`` from version 4.2.0 to 4.2.2.
  - ``drf-yasg`` from version 1.21.4 to 1.21.7.

- Code style fixes.
- Fix typos in comments, help texts, transformations labels.
- Use right field when sorting document file pages
- Generate markup for GitHub issues
- Tweak main view horizontal margins to avoid sidebar issue in recent
  Firefox versions.

4.4.9 (2023-10-15)
==================
- Fix the ``add_file`` method for the ``TarArchive`` class.
- Docker builder updates. Improve how caches and proxies are calculated.
  Add support for Docker image mirroring.
- Update Django from version 3.2.20 to 3.2.22.
- Fix editing existing metadata workflow actions.
- Update the Docker image ``entrypoint.sh`` to skip changing the ownership
  of files if ``MAYAN_COMMON_DISABLE_LOCAL_STORAGE`` is set to any truthy
  value (``True``, ``true``, ``T``, ``t``, ``Yes``, ``yes``, ``Y``, ``y``,
  ``1``).
- Backport periodic task import checking.
- Backport source periodic task changes.
- Update PyYAML from version 6.0 to 6.0.1.
- Update the Docker builder image from version 20.10.21-dind to 23.0.6-dind.
- Update the base Debian image from version debian:11.7-slim to
  debian:11.8-slim.
- Update PIP from version 22.2 to 23.2.1.
- Update the GitLab CI deployment stage to not install the Docker runtime.
- Remove obsolete example settings from the default ``.env`` file.

4.4.8 (2023-07-15)
==================
- Fixes and improvements from versions 4.3.10 and 4.2.17.

4.4.7 (2023-06-03)
==================
- Fix sitemap URL scheme format.
- CI documentation jobs improvements:

  - Install wheel to use modern Python package versions.
  - Don't install or build the Mayan EDMS Python package and
    instead use the development code to build the documentation.
  - Ensure APT proxy quotes are escaped.

- Fixes and improvements from versions 4.3.9, 4.2.16 and 4.2.17dev0.

4.4.6 (2023-04-16)
==================
- Update Docker image versions:

  - Debian from 11.5-slim to 11.6-slim
  - Docker from 20-dind to 20.10.21-dind
  - Elasticsearch from 7.17.0 to 7.17.9
  - MySQL from 8.0 to 8.0.32
  - PostgreSQL from 13.8 to 13.10
  - Python from 3.10-slim to 3.10.11-slim
  - RabbitMQ from 3.11.2-alpine to 3.11.13-alpine
  - Redis from 7.0.5-alpine to 7.0.10-alpine

- Merged changes from version 4.3.8:

  - Fix sources app migration 0027 backend mapping path.
  - Don't include local config values in app settings. Local config values
    are meant to override CI/CD and test settings, and not meant to be
    committed as permanent to the repository.
  - Improve deployment stages:

    - Use long setting versions.
    - Clean up volumes using the official method.
    - Pull images to ensure the latest copy is used even if the image
      has the same tag as the remote.

- Ensure the workflow state action column is not shown for the workflow
  state runtime proxies where is does not make sense to show.
- Ignore staging folder file image cache error if the image cache is not
  already generated when deleting the staging folder file.
- Update Docker Compose file to work backward incompatible bug introduced
  in version 2.17.0 YAML processor
  (https://github.com/docker/compose/issues/10411).

4.4.5 (2023-03-11)
==================
- Merge version 4.3.6 documents app migration 80 workaround.
  Update migration 80 of the documents app to ensure the stored size of the
  converted document file size does not exceed the ``PositiveIntegerField``
  database field maximum value of 2147483647
  (https://docs.djangoproject.com/en/4.1/ref/models/fields/#positiveintegerfield).
- Merges from version 4.3.7:

  - GitOps improvements.
  - Move the helper module ``version.py`` to the dependencies app.
  - Add OCI metadata annotations.

4.4.4 (2023-02-14)
==================
- Update image interface when generating QRCode image. Fixes OTP QRCode
  rendering. Thanks to forum user Ken Robinson (@DocCyblade) for the report.
- Simplify OTP QRCode generation to lower the chances of future regressions.
- Add a custom REST API exception handler to workaround inconsistent
  validation exception behavior in Django REST framework
  (https://github.com/encode/django-rest-framework/issues/2145). Closes
  GitLab issue #1128. Thanks to Jan Przychodniak (@janprzychodniak) for the
  report and debug information.
- Ensure correct index instance nodes are deleted. Don't delete all excluded
  index instances nodes. Instead delete all the index instance nodes where
  the document being processed is found but exclude the nodes recently
  updated. Closes GitLab issue #1134. Thanks to Nicholas Buttigieg
  (@nicholasbuttigieg) and Kyle Pullicino (@KPull) for the report and test
  scenario.
- Remove the Python Transifex client. The new Go based client is required
  to be installed manually when working with translations
  (https://github.com/transifex/cli).

4.4.3 (2023-02-11)
==================
- Improve transformation views to always pass the object
  having the transformation applied.
- Add support to the ``Link`` class for dynamic view keyword arguments, icon,
  resolved object, and permissions.
- Update the transformation, decorations, and redactions links to use
  dynamic view keyword arguments, icons, resolved objects, and permissions.
- Move transformation and redactions links to either their own ``links.py``
  module. In the case of the ``documents`` app, the module is named
  ``miscellaneous_links.py``.
- Improve permissions handling of the transformation, decorations, and
  redactions links.
- Improve transformation and redaction link testing.
- Sanitize tag labels to avoid XSS abuse (CVE-2022-47419: Mayan EDMS Tag XSS).
  This is a limited scope weakness of the tagging system markup that can be
  used to display an arbitrary text when selecting a tag for attachment to
  or removal from a document.

  It is not possible to circumvent Mayan EDMS access control system or
  expose arbitrary information with this weakness.

  Attempting to exploit this weakness requires a privileged account and
  is not possible to enable from a guest or an anonymous account. Visitors
  to a Mayan EDMS installation cannot exploit this weakness.

  It is also being incorrectly reported that this weakness can be used to
  steal the session cookie and impersonate users. Since version 1.4
  (March 23, 2012) Django has included the ``httponly``
  attribute for the session cookie. This means that the session cookie data,
  including ``sessionid``, is no longer accessible from JavaScript.
  https://docs.djangoproject.com/en/4.1/releases/1.4/

  Mayan EDMS currently uses Django 3.2. Under this version of Django
  The ``SESSION_COOKIE_HTTPONLY`` defaults to ``True``, which enables the
  ``httponly`` for the session cookie making it inaccessible to JavaScript
  and therefore not available for impersonation via session hijacking.
  https://docs.djangoproject.com/en/3.2/ref/settings/#session-cookie-httponly

  Django's ``SESSION_COOKIE_HTTPONLY`` setting is not currently exposed by
  Mayan EDMS' setting system, therefore it is not possible to disable this
  protection by conventional means.

  Any usage of this weakness remains logged in the event system making
  it easy to track down any bad actors.

  Due to all these factors, the surface of attack of this weakness is
  very limited, if any.

  There are no known actual or theoretical attacks exploiting this
  weakness to expose or destroy data.
- Drop support for Python 3.7 and Python 3.8. Python 3.9 is now the minimum
  version supported. This change happened in version 4.4 but was not
  documented. Closes GitLab issue #1137. Thanks to joh-ku (@joh-ku)
  for the report and research.

4.4.2 (2023-01-23)
==================
- Merge request !106. Do not show server communication modal
  for interrupted AJAX requests. Thanks to
  Nicholas Buttigieg (@nicholasbuttigieg) and
  Kyle Pullicino (@KPull) for the patch.

4.4.1 (2023-01-19)
==================
- Fix list filtering template issue caused by caching.
- GitOps updates:

  - Add makefile targets to trigger standalone builds.
  - Increase artifact expiration.
  - Add PIP and APT caching to documentation and python build stages.
  - Add GitLab CI job dependencies.
  - Reuse Python build in stages.
  - Convert branches into literals.
  - Remove duplicated code in jobs.

- Simplify installation documentation.

4.4 (2023-01-16)
================
- Update Docker image tags:

  - Docker from 20-dind to 20.10.21-dind
  - Elasticsearch from 7.17.0 to 7.17.7
  - PostgreSQL from 12.11-alpine to 13.11.2-alpine
  - Redis from 6.2-alpine to 7.0.5-alpine

- Update dependencies versions:

  - Celery from 5.1.2 to 5.2.7.
  - extract msg from 0.34.3 to 0.36.4.
  - djangorestframework from 3.13.1 to 3.14.0.
  - drf-yasg from 1.20.0 to 1.21.4.
  - sentry-sdk from 1.5.8 to 1.21.1.
  - Pillow from 9.2.0 to 9.4.0.

- Increase compatibility of the file caching storage usage with more S3
  object storage implementations.
- Add support for OpenID Connect (OIDC) authentication. Adds the new
  ``authentication_oidc`` app.
- Add the parent cabinet as the action object to the cabinet creation event
  when a child cabinet is created.
- Add the cabinet deleted event. This event is committed when a child cabinet
  is deleted. The parent cabinet is recorded as the action object for the
  event.
- Fix the function interfaces when calling ``get_mayan_object_permissions``
  to ``get_mayan_view_permissions`` to override an API view permission
  layout.
- Update navigation permission check to short circuit check when the
  current user has not logged in yet.
- Cabinet updates:

  - Use the same permission layout to create parent and child cabinets from
    the API as from the HTTP views.
  - The create permission is now required to create parent as well as child
    cabinets. This change replaces requiring the edit permission to create
    child cabinets via the HTTP views.

- Data from file and download content creation or examination now defaults
  to byte format instead of unicode.
- Include Django Storages and boto3 Python libraries by default.
- Use the optimized version (``+=``) of the ``+`` operator.
- Moved the document version export code to its own app called
  ``document_exports``. Existing export events and permissions are
  migrated automatically.
- Improved invalid permission error handling. Instead of returning an error
  that stop execution when an invalid permission identifier is requested,
  the permission model will return a one line text indicating that the
  permission name is invalid. This error message will be displayed in place
  of the intended permission label.

  This behavior was also extended to cover invalid permission
  namespace requests.

  A troubleshooting section is added explaining the possible
  reasons for the and the solution.
- Search refactor:

  - Added search syntax pre processor and convert all backend to work with
    it.
  - Simplify scoped search syntax.
  - Allow more than two operands per operator.
  - Implement NOT operator.
  - Improve AND and OR operators.
  - Split search classes into separate modules.
  - Add search field subclasses.
  - Move instance value retrieval to search fields.
  - Add virtual fields.
  - Add an "ANY field" virtual field.
  - All search is now conducted using an internal scope system.
  - Move search syntax decoding to its own class and subclasses named
    ``SearchInterpreter``.
  - Move the search bar to the main menu top bar.
  - Add support for data typing.
  - Normalize data during index and search.

- Testing improvement. Track test document IDs. Keep a list of the test
  document IDs in number and string format.
- New reusable view mixin, ``MultipleExternalObjectViewMixin``.
- Add Hebrew to the default list of document languages.
- Enable Docker BuildKit.
- Add dedicated Docker build RUN cache.
- Docker Compose file changes:

  - Configurable frontend HTTP port via the .env file.
  - Unify frontend and all_in_one profiles HTTP and Traefik configuration.
  - Support Let's Entry TLS termination for all_in_one profile.
  - Configurable RabbitMQ administration HTTP port via the .env file.
  - Configurable Traefik dashboard, HTTP and HTTPS entrypoints ports via
    the .env file.
  - Configurable Traefik Let's Encrypt certificate volume location.
  - Support Let's Encrypt DNS challenge.

- Isolate compressed file MIME type matching exception catching to the
  pertinent code.
- Download file updates:

  - Associate download files to a specific users.
  - Add delete, download, and view permissions.
  - Add download file size column.

- Support bulk document file downloads.
- Move document file download code to the new document downloads app. Migrate
  existing document file download permission and events.

- Permission updates:

  - Improve permission caching. Remove custom caching code and
    use upstream Django caching utilities.
  - Rename variables for clarity.
  - Update dependent code to match class interface changes.

- Short circuit the source column source object resolution code to support
  the list template showing columns even on empty lists. Unlike models and
  queryset, empty lists of class instances won't display any columns.
- Download GPG keys in binary mode.
- Show more details when a bootstrap setting parsing error occurs.
- Add libfuse2, libsasl2-dev, and libldap2-dev to the development setup
  makefile target.
- Convert pagination template into a partial.
- Add .msg file metadata drivers.
- Convert the metadata value and the file metadata value fields from
  character fields with a maximum length of 255 characters to text fields.
- Improve the settings apps navigation.
- Collapse action menus by default.
- Split links in the list items template into action links and view (facet)
  links.
- Remove Docker mirror configuration from the GitLab CI file. This is up to
  the runner to configure.
- Show cache partitions and partition file totals. This helps determine how
  effective is a cache maximum size value by showing how many objects and
  files the cache size limit is able to yield.
- Statistics updates:

  - Improve statistics navigation.
  - Add doughnut chart type statistic.
  - Add pie chart type statistic.
  - Add column displaying the chart type per statistic.
  - Update chartjs from version 2.8.0 to 3.9.1.
  - Unify chart templates.
  - Autoload statistics modules.
  - Unify ChartJS templates.
  - Support passing full chart context not just plot data.
  - Fix app URL layout.
  - Fix app URL typo.
  - Fix statistic queue view navigation context.

- Add three document pie chart statistics: document count per document type,
  document file count per document type, document file page count per
  document type.
- Add documentation directives to insert setting or setting namespace
  instances.
- Improve search and object storage documentation by adding automated
  setting references.
- Add third state to column sorting. The sorting states are now: ascending,
  descending, none.
- Support sorting multiple columns.
- Add a permission count column to ACLs.
- Add support for setting choices.
- Add an HTML to better format setting values.
- Fix search again view redirect. Retain the query from the previous view.
- Rename the "Search" facet link to "Basic search".
- Fix "Match All" behavior when using the "Search again" link.
- Replace "Match All" field with a radio box to allow supporting search
  again persistence and also the default state of the field.
- Convert the "Match All" field name into a literal.
- Split the document file creation method into smaller units. This reduces
  the complexity of the several conditional statements.
- Ensure the document file is created even if there are errors during the
  uploaded file introspection.
- Encapsulate mozilla-django-oidc settings as Mayan authentication backend
  arguments.
- Add support for OpenID Connect Discovery (https://openid.net/specs/openid-connect-discovery-1_0.html).
- Add Keycloak Docker Compose service.
- Make Docker Compose service image name configurable.
- User interface updates:

  - Collapse views and actions by default.
  - Add collapsed views and actions icons.
  - Move views and actions markup to their own respective partial templates.
    This reduces duplication and improves usability of the markup.
  - Lower the z-index of the sidebar to avoid menus to display behind it.
  - Add simulated horizontal rulers to the body of tables.
  - Support slim dropdown menus.
  - Move navigation to the card footer.
  - Fix click events passing through views and action dropdown caret icons.
  - Make the words "Actions" and "Views" translatable.
  - Add two new table columns. One columns for views and another the actions.
  - Unroll single action menus to a button.
  - Reduce table padding to increase data area.
  - Minor spacing and margin tweaks.

- Code style refactor and cleanup:

  - Strip trailing commas.
  - Sort arguments, dictionary keys and class methods.
  - Unroll nested contexts.
  - Separate model data and business logic code.
  - Move add or remove code to models. Directly and as added methods to
    external models.
  - Pass the user to action methods instead of injecting the user as the
    event actor. Injecting the user as the event actor will be done only
    on immediate methods that do not allow arguments or data layer model
    methods with well defined upstream arguments.
  - Add keyword arguments.
  - Rename mixins modules to be more explicit.
  - Normalize the ``UploadWizard`` class ``step_post_upload_process`` method
    arguments.
  - Remove many instances of ``force_text``.
  - Move several ``upload_to`` functions to their corresponding app's
    ``utils`` module.
  - Promote private ``_user`` argument to an official argument.

- API views refactor:

  - Remove injected objects on API views. Each API view needs to query the
    object explicitly. This is change is less efficient but was made to
    mirror how upstream DRF works.
  - Pass the view object to the action object API view.
  - Add labels to serializer fields.

- Track the user when purging caches and cache partitions.
- Create a new permission to change the type of a document.
  When support for changing the type of a document was added, it was
  considered a property and controlled via the document property edit
  permission.

  Since changing the type of a documents now causes a cascade of other
  changes, it was isolated as an individual class of event along
  with its own permission.

  The new document change type permission is required for the document being
  changed and for the document type to which the document will be changed
  into.
- Update the file metadata model ``verbose_name`` attribute to be the
  ``help_text`` attribute.
- Update the document parsing ``verbose_name`` attribute to be the
  ``help_text`` attribute.
- Update the document version OCR ``verbose_name`` attribute to be the
  ``help_text`` attribute.
- Update the search API to provide a dummy model serializer during Swagger
  introspection.
- Update the sources actions API to provide a dummy serializer during Swagger
  introspection.
- Fix Swagger schema model definition introspection. Updated REST API views
  to behave like user interface views and returning querysets either via
  the ``source_queryset`` property or the ``get_source_queryset`` method.
  This prevents API views from overriding the queryset return methods and
  allows the ``SchemaInspectionAPIViewMixin`` mixin to work in all
  instances.
- Add support for platform client backends to register tool links.
- Lower the default Sentry client sample rate from 0.05 to 0.01.
- Add new setting to disable automatic upload after dragging files to the
  DropZone widget. The setting is named ``VIEWS_SHOW_DROPZONE_SUBMIT_BUTTON``
  and defaults to ``False``.
- Raise an ``ImproperlyConfigured`` exception when a model is registered for
  error logging more than once.
- Move error logging registration of document models to the documents app.
- OCR updates:

  - Move error logging from the document version to the document version
    page.
  - Add OCR backend ``_execute`` to avoid subclasses from calling the super
    class.
  - The base class now prepares the image to be processed and passes the
    file object to the subclass.
  - Move OCR finished event commit from the task to the manager.

- Restore object event attributes when the event is ignored.
- Error log registration now register error log permissions too by default.
- Improve base settings initialization:

  - Replace ``os.path`` with ``pathlib.Path`` to do path manipulation.
  - Use the default secret key value only if the secret key file is not
    found.
  - Don't obscure errors when reading the secret key file.

- Remove the ``home_view`` setting from the default Template context.
  Template instances need to include their own context using the new
  ``context`` argument.
- Add templating support to bootstrap settings. Template names are the same
  as the bootstrap setting but include the ``SETTING_TEMPLATE_`` prefix.
  Environment variables, Python global and config file values are available
  to the template.
- Remove deprecated management commands:

  - ``checkdependencies`` replaced by ``dependencies_check``.
  - ``checkversion`` replaced by ``dependencies_check_version``.
  - ``createautoadmin`` replaced by ``autoadmin_create``.
  - ``generaterequirements`` replaced by ``dependencies_generate_requirements``.
  - ``initialsetup`` replaced by ``common_initial_setup``.
  - ``installdependencies`` replaced by ``dependencies_install``.
  - ``mountindex`` replaced by ``mirroring_mount_index``.
  - ``performupgrade`` replaced by ``common_perform_upgrade``.
  - ``platformtemplate`` replaced by ``platform_template``.
  - ``preparestatic`` replaced by ``appearance_prepare_static``.
  - ``purgelocks`` replaced by ``lock_manager_purge_locks``.
  - ``purgepermissions`` replaced by ``permissions_purge``.
  - ``purgeperiodictasks`` replaced by ``task_manager_purge_periodic_tasks``.
  - ``purgestatistics`` replaced by ``statistics_purge``.
  - ``revertsettings`` replaced by ``settings_revert``.
  - ``savesettings`` replaced by ``settings_save``.
  - ``showsettings`` replaced by ``settings_show``.
  - ``showversion`` replaced by ``dependencies_show_version``.

- Update the makefile to enable the Sentry client if the ``SENTRY_DSN``
  value is passed to the ``runserver``, ``runserver-plus``, or
  ``staging-frontend`` targets.
- Add new setting to disable logging message ANSI color codes. The setting
  is named ``LOGGING_DISABLE_COLOR_FORMATTER`` and defaults to ``False``.
- Standardize management command testing.
- Move management command names to the ``literals`` module of each app.
- GitOps updates:

  - Add configurable remote branch for GitOps.
  - Support a local environment config file names ``config-local.env``.
    This file is ignored by Git and meant to override values of ``config.env``.

4.3.12 (2023-12-10)
===================
- Don't install Docker when deploying. Update the GitLab CI deployment
  stage to not install the Docker runtime.
- Fix document file page search content field label.
- Fix test asserts. Fix test that were asserting for True values instead of
  asserting for equality.
- Continue purge loops even during errors. Update the cache and cache
  partition purge loop to continue executing even when there are files that
  cannot be purged. Cache partition files will be skipped and retried on the
  next purge execution.
- Add event asserts in tests.
- Fix the workflow metadata action ``select2`` widget.
- Code style fixes.
- Use long form for the command options in the Dockerfile.
- Skip Docker volume ownership code. Update the Docker image
  ``entrypoint.sh`` to skip changing the ownership of files if
  ``MAYAN_COMMON_DISABLE_LOCAL_STORAGE`` is set to any truthy value
  (``True``, ``true``, ``T``, ``t``, ``Yes``, ``yes``, ``Y``, ``y``, ``1``).
- Backport source periodic task changes. Use a constant instead of a literal
  to track the name of the source action execute task.
- Fix the `add_file` method of ``TarArchive``.

4.3.11 (2023-12-08)
===================
- Use correct field when sorting document file pages.
- Fix typos in comments and transformations labels.
- Code style fixes.
- Fix code style warning E713.
- Update dependencies:

  - Update Django from version 3.2.20 to 3.2.23.
  - ``redis`` from version 4.2.0 to 4.2.2.
  - ``drf-yasg`` from version 1.20.0 to 1.21.7.
  - ``PyYAML`` from version 6.0 to 6.0.1.

- Add missing mailing profile ``default`` field to creation and edit forms.
- Support Django series in setup generation script.
- Use Mayan CLI full path in DockerFile.
- Generate markup for GitHub issues.
- Workaround Cython and PyYAML dependency bug from unpinned requirement
  version.

4.3.10 (2023-07-14)
===================
- Fixes from version 4.2.17.
- Add new translation languages:

  - ar-eg: Arabic (Egypt)
  - ca: Catalan
  - de-at: German (Austria)
  - de-de: German (Germany)
  - es-mx: Spanish (Mexico)
  - he-il: Hebrew (Israel)
  - hr: Croatian
  - mn-mn: Mongolian (Mongolia)
  - ro-ro: Romanian (Romania)
  - sq: Albanian
  - th: Thai
  - tr-tr: Turkish (Turkey)
  - uk: Ukrainian
  - zh-cn: Chinese (China)
  - zh-hans: Chinese (Simplified)
  - zh-tw: Chinese (Taiwan)

- Move language and timezone choice generation to ``locales.utils``.
- Sort language dropdown selection by language name and by language code.
- Update dependency versions:

  - Django from 3.2.19 to 3.2.20.
  - django-model-utils from 4.2.0 to 4.3.1
  - django-mptt from 0.13.4 to 0.14.0
  - requests from 2.27.1 to 2.29
  - sh from 1.14.2 to 1.14.3
  - safety from 1.10.3 to 2.3.5
  - sentry-sdk from 1.5.8 to 1.5.12
  - whitenoise from 6.0.0 to 6.2.0

4.3.9 (2023-06-02)
==================
- Fix document parsing error logging. Use the correct argument name when
  creating new error log entries.
- Fixes and improvements from versions 4.2.16 and 4.2.17dev0.

4.3.8 (2023-04-15)
==================
- Merged changes from version 4.2.15:

  - Fix sources app migration 0027 backend mapping path.
  - Include bug fixes and updates from version 4.0.24.
  - Don't include local config values in app settings. Local config values
    are meant to override CI/CD and test settings, and not meant to be
    committed as permanent to the repository.
  - Improve deployment stages:

    - Use long setting versions.
    - Clean up volumes using the official method.
    - Pull images to ensure the latest copy is used even if the image
      has the same tag as the remote.

- Update Docker image versions:

  - Elasticsearch from 7.17.0 to 7.17.9
  - Debian from 11.4-slim to 11.6-slim
  - MySQL from 8.0 to 8.0.32
  - PostgreSQL from 12.11-alpine to 12.14-alpine
  - Python from 3.10-slim to 3.10.11-slim
  - Redis from 6.2-alpine to 6.2.11-alpine
  - RabbitMQ from 3.10-alpine to 3.10.20-alpine

- Ensure the workflow state action column is not shown for the workflow
  state runtime proxies where is does not make sense to show.
- Ignore staging folder file image cache error if the image cache is not
  already generated when deleting the staging folder file.

4.3.7 (2023-09-10)
==================
- Merge changes from version 4.2.14:

  - GitOps improvements.
  - Support a local environment config file names ``config-local.env``.
  - Split GitLab CI targets into their own makefile.
  - Move the helper module ``version.py`` to the dependencies app.
  - Convert branches into literals.
  - Add OCI metadata annotations

- OCI metadata change. Don't remove the 'T' from the image date label.

4.3.6 (2023-02-19)
==================
- Update migration 80 of the documents app to ensure the stored size of the
  converted document file size does not exceed the ``PositiveIntegerField``
  database field maximum value of 2147483647
  (https://docs.djangoproject.com/en/4.1/ref/models/fields/#positiveintegerfield).
- Sanitize tag labels to avoid XSS abuse (CVE-2022-47419: Mayan EDMS Tag XSS).
  This is a limited scope weakness of the tagging system markup that can be
  used to display an arbitrary text when selecting a tag for attachment to
  or removal from a document.

  It is not possible to circumvent Mayan EDMS access control system or
  expose arbitrary information with this weakness.

  Attempting to exploit this weakness requires a privileged account and
  is not possible to enable from a guest or an anonymous account. Visitors
  to a Mayan EDMS installation cannot exploit this weakness.

  It is also being incorrectly reported that this weakness can be used to
  steal the session cookie and impersonate users. Since version 1.4
  (March 23, 2012) Django has included the ``httponly``
  attribute for the session cookie. This means that the session cookie data,
  including ``sessionid``, is no longer accessible from JavaScript.
  https://docs.djangoproject.com/en/4.1/releases/1.4/

  Mayan EDMS currently uses Django 3.2. Under this version of Django
  The ``SESSION_COOKIE_HTTPONLY`` defaults to ``True``, which enables the
  ``httponly`` for the session cookie making it inaccessible to JavaScript
  and therefore not available for impersonation via session hijacking.
  https://docs.djangoproject.com/en/3.2/ref/settings/#session-cookie-httponly

  Django's ``SESSION_COOKIE_HTTPONLY`` setting is not currently exposed by
  Mayan EDMS' setting system, therefore it is not possible to disable this
  protection by conventional means.

  Any usage of this weakness remains logged in the event system making
  it easy to track down any bad actors.

  Due to all these factors, the surface of attack of this weakness is
  very limited, if any.

  There are no known actual or theoretical attacks exploiting this
  weakness to expose or destroy data.
- Simplify OTP QRCode generation to lower the chances of future regressions.
- Remove the Python Transifex client. The new Go based client is required
  to be installed manually when working with translations
  (https://github.com/transifex/cli).
- Add Makefile target to allow testing individual migration tests against
  PostgreSQL.
- Add a custom REST API exception handler to workaround inconsistent
  validation exception behavior in Django REST framework
  (https://github.com/encode/django-rest-framework/issues/2145). Closes
  GitLab issue #1128. Thanks to Jan Przychodniak (@janprzychodniak) for the
  report and debug information.

4.3.5 (2023-01-10)
==================
- Fix error when deleting a user form the user interface. Closes GitLab
  issue #1125. Thanks to friki67 (@friki67) for the report and
  Jan Przychodniak (@janprzychodniak) for the additional debug information.

4.3.4 (2022-12-19)
==================
- Merge fixes from version 4.2.13.
- Fix reference to ``ocr_errors`` in
  ``mayan.apps.ocr.tasks.task_document_version_ocr_finished``. Closes GitLab
  issue #1131. Thanks to  Olivier D. (@odelseth) for the report and debug
  information.
- Fix click events passing through views and action dropdown caret icons.
  Activating the dropdown menu by clicking on the menu's caret no longer
  select the document file or version card.

4.3.3 (2022-11-15)
==================
- Fixes from version 4.2.12.
- Add a patch for Python's CVE-2007-4559
  (https://nvd.nist.gov/vuln/detail/CVE-2007-4559).

  This is a language level vulnerability which exposed older versions
  of Mayan EDMS only when downloading JavaScript dependencies from the NPM
  registry.

  Exploiting this vulnerability requires compromising an existing package
  hosted on the NPM registry and adding Python code specifically targeting
  Mayan EDMS. As part of the project's design philosophies, dependencies
  are only downloaded from authoritative locations and each dependency is
  pinned to a specific version to guarantee immutable releases.

  Due to all these factors, surface of attack of this vulnerability is
  very limited for older versions of Mayan EDMS, it is also very improbable,
  very difficulty to accomplish and very difficult to remain undetected.

  There are no known actual or theoretical attacks for Mayan EDMS
  exploiting this vulnerability.

  Thanks to the TrellixVulnTeam for the pull request which lead to this
  Mayan EDMS specific patch.

4.3.2 (2022-11-12)
==================
- Use the correct icon for the document type file metadata
  setup link.
- Merge bugfix version 4.2.11 and 4.2.12.
- Update translation files.
- Fix response structure of the search model API view.
  Ensure the search fields are displayed.
- Fix hardcoded list mode argument.

4.3.1 (2022-08-21)
==================
- Fixes and improvements merged from version 4.2.9 and 4.2.10.
- Fix the function interfaces when calling ``get_mayan_object_permissions``
  to ``get_mayan_view_permissions`` to override an API view permission
  layout.

4.3 (2022-07-27)
================
- Partials navigation updates:

  - Streamline JavaScript partials navigation code.
  - Make the AJAX response redirect code configurable. New setting
    ``APPEARANCE_AJAX_REDIRECTION_CODE`` added.
  - Remove repeated AJAX redirection middleware.

- Add white outline to favicon.
- Add support for optional ``get_mayan_object_permissions`` and
  ``get_mayan_view_permissions`` methods to allow API views to customize
  how required permissions are calculated.
- Added support for form fieldsets.
- Added fieldsets to the following forms:

    - document file properties
    - document type deletion policies
    - metadata type
    - user

- Remove usage of flat ``values_list`` queryset in metadata managers module.
- Prefix all test objects with an underscore to avoid clashes with test
  methods.
- ``PartialNavigation.js`` improvements.

  - Clean URL query on form submit and use form data as the URL query.
  - Remove dead code.
  - Use constants where appropriate.

- Search updates:

  - Add filtering support to list views. All list view that show instances of
    models with a corresponding defined search model, will show a text box
    for filtering the list. The syntax is the same as the standard simple
    search.
  - Empty list views now show the toolbar for cases where the list is empty
    due to a filtering term.
  - Define the ``q`` URL query key as an internal literal named
    ``QUERY_PARAMETER_ANY_FIELD``.

- Support AJAX request cancellation. This avoid the user interface from
  appearing to unresponsive when the backend is overloaded.
- Support AJAX request throttling. Prevents users from requesting too many
  consecutive page loads. Defaults to a maximum of 10 requests in 5 seconds
  of less. This applies only to the user interface. The AJAX throttling
  resets when a pending request is completed. Added the settings
  ``APPEARANCE_THROTTLING_MAXIMUM_REQUESTS`` and
  ``APPEARANCE_THROTTLING_TIMEOUT``. Display a message notifying users when
  throttling is in effect.
- ``BaseBackend`` class improvements.

  - Selectable identifier via the ``_backend_identifier`` property. Defaults
    to ``backend_class_path`` for compatibility.
  - Update ``.get_all`` to return a list and not a dictionary.
  - Add property ``backend_id`` that returns the value of the class
    ``_backend_identifier`` property.

- Convert document file actions from hardcoded logic to an extensible class
  using the ``BaseBackend`` class. Available classes will be loaded from the
  ``document_file_actions`` module. The id of the class defaults to the
  existing literal values for compatibility.
- Add API endpoint called ``document_file_actions`` to list the available
  actions and their properties. API endpoint URL: /api/v4/document_file_actions/
- Add document version modification backend. Convert the document version
  page reset and append functions into document version modification backends.
  Update document version views and API endpoints to use document version
  modification backends.
  Adds new API endpoints:

    - /api/v4/documents/{ ID }/versions/{ ID }/modify/
    - /api/v4/document_version_modification_backends/

- Add workflow action to send user messages.
- Update ``WorkflowAction`` to use ``common.classes.BaseBackend``.
- Pagination refactor:

  - Remove ``django-pure-pagination`` package.
  - Use Django's 3.2 new ``get_proper_elided_page_range`` for paging.
  - Remove duplicate URL query string manipulation.
  - Remove duplicated pagination template.
  - Make pagination argument configurable. Added the setting
    ``VIEWS_PAGING_ARGUMENT``. Defaults to ``page`` for compatibility.

- Update the default pagination size from 40 items to 30.
- Support hyphenated text when using the Elasticsearch backend.
- Add support for supplying files to source backend via the API. Add the
  ``accept_files`` property to ``SourceBackendAction`` which dynamically add
  a ``file`` serializer field for the corresponding action.
- Add an ``upload`` action to the web form source. This allows using web form
  sources to upload documents from the API.
- Support REST API list filtering. Filtering is done using similar logic
  to that of the user interface list filtering. However, the API list
  filtering also support filtering by any field and not just using the
  special "any field" ``q`` query key.
- Merge fixes from version 4.2.2.
- Move the ``purgeperiodictasks`` command from the common app to the
  task_manager app.
- Drop support for Python 3.6.
- Dependencies update:

  - Elasticsearch from 7.16.0 to 7.17.0.
  - Debian from 11.2-slim to 11.3-slim.
  - PostgreSQL from 12.9-alpine to 12.10-alpine.
  - RabbitMQ from 3.9-alpine to 3.10-alpine.
  - amqp from 5.0.9 to 5.1.0.
  - pip from 21.3.1 to 22.2.
  - psycopg2 from 2.9.2 to 2.9.3.
  - redis from 4.0.2 to 4.2.0.
  - FontAwesome from 5.6.3 to 5.15.4.
  - urijs from 1.19.7 to 1.19.10.
  - bleach from 4.0.0 to 4.1.0.
  - django-solo from 1.1.5 to 2.0.0.
  - jstree from 3.3.11 to 3.3.12.
  - PyYAML from 5.4.1 to 6.0.
  - django-model-utils from 4.1.1 to 4.2.0.
  - django-mptt from 0.12.0 to 0.13.4.
  - pycountry from 20.7.3 to 22.3.5.
  - requests from 2.26.0 to 2.27.0.
  - devpi-server from 6.2.0 to 6.5.0.
  - django-debug-toolbar from 3.2.2 to 3.2.4.
  - django-extensions from 3.1.3 to 3.1.5.
  - django-rosetta from 0.9.7 to 0.9.8.
  - django-silk from 4.1.0 to 4.3.0.
  - flake8 from 3.9.2 to 4.0.1.
  - ipython from 7.26.0 to 7.32.0.
  - transifex-client from 0.14.3 to 0.14.4.
  - twine from 3.4.2 to 3.8.0.
  - wheel from 0.37.0 to 0.37.1.
  - Pillow from 8.3.1 to 9.2.0.
  - node-semver from 0.8.0 to 0.8.1.
  - packaging from 21.0 to 21.3.
  - python_gnupg from 0.4.7 to 0.4.8.
  - elasticsearch from 7.16.0 to 7.17.1.
  - django-activity-stream from 0.10.0 to 1.4.0.
  - chart.js from 2.7.3 to 2.8.0.
  - python-magic from 0.4.24 to 0.4.26.
  - gevent from 21.8.0 to 21.12.0.
  - sentry-sdk from 1.4.1 to 1.5.8.
  - whitenoise from 5.3.0 to 6.0.0.
  - cropperjs from 1.5.2 to 1.5.12.
  - django-cors-headers from 3.8.0 to 3.10.0.
  - djangorestframework from 3.12.4 to 3.13.1.
  - jsonschema from 3.2.0 to 4.4.0.
  - swagger-spec-validator from 2.7.3 to 2.7.4.
  - dropzone from 5.9.2 to 5.9.3.
  - pycryptodome from 3.10.1 to 3.10.4.
  - celery from 5.1.2 to 5.2.3.
  - django-formtools from 2.2 to 2.3.
  - django-widget-tweaks from 1.4.9 to 1.4.12.
  - furl from 2.1.2 to 2.1.3.
  - Sphinx from 3.5.4 to 4.5.0.

- Silence warning about unordered object pagination for:

  - Announcements
  - Document index instance nodes
  - Workflow transition triggers
  - File caches
  - Quotas

- Convert API search model names to lowercase to revert backward incompatible
  change in version 4.2. Search model names via the API can now be specified
  in either lowercase (version 4.2) or hybrid case (version <4.2).
- ``mkdtemp`` now accepts a ``dir`` argument like the upstream version.
  However the ``dir`` value is appended to the system wide value of
  ``STORAGE_TEMPORARY_DIRECTORY``.
- Staging folder updates:

  - Support inclusion regular expression.
  - Support exclusion regular expression.
  - Support subfolders.
  - Update scan code to use ``pathlib.Path``.
  - Support pagination.

- Add support for workflow escalation. This feature allows moving a workflow
  forward after the workflow has remained in a certain state after a
  pre-determined amount of time. Multiple escalations are supported for
  each state. Conditions using the templating language are supported.
- Move model based classes to the databases app. Move the classes:

  - ``ModelQueryFields``
  - ``ModelAttribute``
  - ``ModelProperty``
  - ``ModelField``
  - ``ModelFieldRelated``
  - ``ModelReverseField``
  - ``QuerysetParametersSerializer``

- Convert the OCR app to the new error log system. The permission
  "View error log" is now required to view the document version OCR error
  log.
- Convert the document parsing app to the new error log system. The
  permission "View error log" is now required to view the document file
  parsing error log.
- Remove the Python package ``mock``. This package is now available as
  unittest.mock in Python 3.3 onward.
- Unify and remove repeated workflow API views code using parent resolution
  mixins.
- Support adding help text to search model fields. By default the help text
  from the model fields will be used.
- Increase the document type label size from 96 characters to 196.
- Update the document type label field help text.
- Search updates:

  - Rename search model instances from "...search" to "search_model...".
  - Add support for removing search fields from third party apps. The method
    is called ``.remove_search_field(search_field=)`` and requires the
    search field instance obtained from the method ``.get_search_fields()``.
  - Remove the ``search_fields`` list and use the ``search_fields_dict``
    instead for both purposes. The canonical method to obtain the search
    field of a search model is now using the method ``.get_search_fields()``.

- Update the Elasticsearch backend default settings to match those of the
  official Python client.
- Don't introspect document file MIME type at download. Instead pass the
  stored values.
- Support empty ranges for ``parse_range``.
- Add ``group_iterator`` to group iterators in to lists of tuples.
- Refactor bulk object search indexing:

  - Rename ``mayan.apps.dynamic_search.tasks.task_index_search_model`` to
    ``mayan.apps.dynamic_search.tasks.task_index_instances``.
  - Index only objects that exists instead of using blind ranges.
  - Update ``search_index_objects`` management command to trigger multiple
    ``task_index_instances`` tasks instead of just one.

- Add date manipulation template tags. The new tags are ``date_parse`` to
  convert a string into a datetime object and ``timedelta`` to apply time
  transformations to a datetime object.
- Add a ``size`` field to the document file model. Since this value is not
  expected to change, it is now a persistent model field and not calculated
  on demand by querying the storage layer. This change also improves document
  mirroring performance by removing one disk access per document and using
  the database stored size value which is immutable.
- Support searching messages. Make the ``subject``, ``body``, ``date_time``
  fields searchable.
- Error logging updates:

  - Add error log entry delete permission.
  - Add support deleting individual error log entries or the complete error
    log of an object.
  - Add the error log entry delete event.
  - Support subscribing to the error log entry delete event of an object.
  - Add API views. Support added to view the error log of objects.

- Migrations code style cleanup.

  - Rename code migrations functions prefix from ``operation_`` to ``code_``.
  - Add keyword arguments.
  - PEP8 code style cleanups.

- Add support for cabinet mirroring.
- Remove ``django-colorful``. Use HTML5 color field instead.
- Add support to randomize the tag color.
- Document parsing updates. Closes GitLab issue #957. Thanks to
  LeVon Smoker (@lsmoker) for the report and initial suggestions.

  - Pass the original document file to parsers instead of attempting to
    pre-processing the document file to PDF.
  - Add parsing support for office document files and text files.

- Rename test file literals for uniformity.
- Rename management commands to include the app name where they are defined.
  Add a stub command for backwards compatibility.

  - ``checkdependencies`` replaced by ``dependencies_check``.
  - ``checkversion`` replaced by ``dependencies_check_version``.
  - ``createautoadmin`` replaced by ``autoadmin_create``.
  - ``generaterequirements`` replaced by ``dependencies_generate_requirements``.
  - ``initialsetup`` replaced by ``common_initial_setup``.
  - ``installdependencies`` replaced by ``dependencies_install``.
  - ``mountindex`` replaced by ``mirroring_mount_index``.
  - ``performupgrade`` replaced by ``common_perform_upgrade``.
  - ``platformtemplate`` replaced by ``platform_template``.
  - ``preparestatic`` replaced by ``appearance_prepare_static``.
  - ``purgelocks`` replaced by ``lock_manager_purge_locks``.
  - ``purgepermissions`` replaced by ``permissions_purge``.
  - ``purgeperiodictasks`` replaced by ``task_manager_purge_periodic_tasks``.
  - ``purgestatistics`` replaced by ``statistics_purge``.
  - ``revertsettings`` replaced by ``settings_revert``.
  - ``savesettings`` replaced by ``settings_save``.
  - ``showsettings`` replaced by ``settings_show``.
  - ``showversion`` replaced by ``dependencies_show_version``.

- Split the document indexing models module. Module is split into index
  template and instance models.
- Show item count even if the list is empty. This change prevents the list
  toolbar from "jumping" visually when there are no results.
- Simplify how the view title is copied to the window title. Escaping is now
  performed by jQuery.
- Add icons to all views. Every view now has a corresponding icon to be
  displayed with the title.
- Normalize icon, link and view names. Follow the pattern
  object_sub_object_action.
- Add warning message when user attempting to delete their own accounts.
- Add support for Whoosh bulk indexing using the ``BufferedWriter`` class.
  When reindexing the search indexes, for every lock obtained, a group of
  object will be written as a single operation. The number of objects
  written concurrently is controlled by the settings
  ``SEARCH_INDEXING_CHUNK_SIZE``.
- Split converter app views into separate modules.
- Add support for transformation argument forms.
- Improve transformation argument column display.
- Fix argument handling for the transformation
  ``TransformationDrawRectangle``.
- Check and reject negative percent values for the zoom transformation.
- Fix asset transformations hash calculation.
- Use a lower layer that the redaction layer to allow seeing the entire
  document when editing redactions. This is more natural as it gives the
  impression the redaction is actually being edited by being moved instead
  of showing two redactions (old in the image plus the interactive one).
- Add transparency support to the ``TransformationDrawRectanglePercent``
  transformation.
- Unify the ``TransformationDrawRectangle`` and
  ``TransformationDrawRectanglePercent`` transformations.
- Move transformation mixins to their own module.
- Allow classes using ``APIImageViewMixin`` to specify the stream MIME type
  via ``get_stream_mime_type``.
- Fix repeated model manager definition in the ``DocumentFilePage`` model.
- Support easier test document stub creation via the new
  ``auto_create_test_document_stub``. It is mutually exclusive with
  ``auto_create_test_document_stub`` and requires settings
  ``auto_upload_test_document`` to False.
- Add first name and last name fields to the test case user.
- Generalize image transformations into reusable mixins:
  ``ImagePasteCoordinatesAbsoluteTransformationMixin``,
  ``ImagePasteCoordinatesPercentTransformationMixin``,
  ``ImageWatermarkPercentTransformationMixin``.
- Add support for signature capture. The signature capture app allows
  capture of handwritten signatures. The original point data as well as
  an SVG version of the signature is store. The point data represents the
  raw signature primitives that allows reloading them into the signature
  pad library. The SVG version allows for rendering as an image for preview.
  A transformation is added to allow pasting a signature as a page image.
- Remove trailing new lines from the MIME type and encoding returned by the
  ``MIMETypeBackendFileCommand``.
- Make ``MIMETypeBackendFileCommand`` the default MIME backend.
- Fix sorting and grouping of permissions in the workflow action to grant
  or revoke document access.
- Remove ``SearchModel`` unused class method and improve result sorting.
- Navigation updates:

  - Add support for extra HTML attributes.
  - Improve HTML data by allowing the entries to be resolved against the
    context.
  - Support empty URL values. When empty, the link is rendered without a
    href attribute.

- Add link to make staging folder file selection easier. Closes GitLab
  issue #341. Thanks to Leroy Förster (@gersilex) for the report and
  initial idea.
- Modernize Python syntax:

  - Pass generators instead of lists to ``sorted``.
  - Update string formatting to use ``.format``.
  - Remove creating of sets using the set factory and use instead the set
    literal.

- New workflow events: ``workflow instance created`` committed when a new
  workflow is launched for a document and
  ``workflow instance transitioned`` committed when a workflow instance is
  transitioned to a new state, either manually or automatically.
- Track the user when a new workflow instance is created or transitioned.
- Optimize the document indexing by reusing the index instance node if it
  already exists.
- Add support for document index event triggers. Historically document
  indexes used hard coded signals to trigger an index update. The indexing
  app was updated to now use events to trigger these updates. This has the
  additional benefits of allowing runtime configuration of the index event
  triggers, disabling the ones not relevant for an index to improve
  performance. New document indexes default to update on all available
  document events. Existing indexes will me automatically migrated and
  updated to update on all available document events. Index updates now
  support more events like adding or removal from cabinets.
  Closes GitLab issue #631. Thanks to Tobias Huhn (@twhuhn) for the request.
- Convert the staging folder file selection input to a Select2 widget
  supporting text filtering.
- Move the transformations ``TransformationDrawRectangle`` and
  ``TransformationDrawRectanglePercent`` to the decorations layer.
- Add retry backoff maximum delay to the search tasks.
- Add per user object event subscription view.
- Add support for permission filtering to the notification views. This moves
  the access filtering of notification from the class to the view. The
  advantage of this change is that notifications are restricted when the
  access control is modified, even if the notification already exists.
- Normalize how the search "Match all" parameter is evaluated.
- Fix evaluation of "Match all" when using a single level scoped search.
- Discard non supported images contained in MPO images files.
- Use the Elasticsearch count API (https://www.elastic.co/guide/en/elasticsearch/reference/current/cat-count.html)
  to obtain accurate search model status information.
- Delete existing indexes when calling the Elasticsearch backend initialize
  method.
- Wrap search backend errors into a general exception with a short
  explanation.
- Documentation updates:

  - Set the Docker Compose installation method as the main method.
  - Add warning notes for the deprecated installation methods.
  - Expand the requirements section.
  - Move the requirements to their on chapter.
  - Update the features part.

- Add management command ``common_generate_random_secret_key`` to provide
  random values suitable for use as ``SECRET_KEY``.
- Refactor initial setup and upgrade commands:

  - Consolidate management command code.
  - Move command code to a separate class.
  - Convert code to use pathlib.

- Add support for disabling use of the media folder. Add the bootstrap
  setting ``COMMON_DISABLE_LOCAL_STORAGE`` to disable use of the local
  ``media`` folder. When using this setting, all apps must be also configured
  via their respective storage backend settings to use alternate persistence
  methods.
- When serving images using ``APIImageViewMixin``, detect the MIME type of
  the data before sending the stream. This ensures the image will load
  correctly in all browsers that require a MIME type value in the header of
  the stream.
- Change the ``UUID`` field to Elasticsearch field mapping, from ``Keyword``
  to ``Text`` to avoid search indexing error when processing document
  containers with more than 910 documents. Elasticsearch's ``Keyword`` field
  is limited to 32766 bytes and attempting to index a container with more
  than 910 documents would exceed this limit.
- Update the Elasticsearch backend search query configuration to be more
  strict and lower the number of hits matched. Change the ``match`` query to
  ``match_phrase`` and remove the ``fuzzy`` query.
- Ensure document version pages point to an existing content object when
  exporting. Otherwise they are skipped.
- Improve document version export code to skip invalid pages. The page loop
  will skip pages with no content object and regard the first page found
  with a content object as the first exported page.
- Don't assume all storages have a preset mode attribute. Such is the case
  with the ``S3Boto3Storage`` when used for shared uploaded files. Instead
  introspect the mode and fallback to a safe default valur of ``'rb'``.
- Disable the settings edit link when local storage is disabled.
- Display a warning message in the setting edit view when local storage is
  disabled.

4.2.18 (2023-12-09)
===================
- Update the cache and cache partition purge loop to continue executing even
  when there are files that cannot be purged. Cache partition files will be
  skipped and retried on the next purge execution.
- Fix document file page search content field label.
- Upgrade Django from version 3.2.19 to 3.2.23.
- Generate markup for GitHub issues.
- Fix a setting help text typo.
- Add missing mailing profile ``default`` field to creation and edit forms.
- Support Django series in setup generation script.
- Use Mayan CLI full path in DockerFile.
- Update the GitLab CI deployment stage to not install the Docker runtime.
- Backport source periodic task changes.
- Update the Docker image ``entrypoint.sh`` to skip changing the ownership
  of files if ``MAYAN_COMMON_DISABLE_LOCAL_STORAGE`` is set to any truthy
  value (True, true, T, t, Yes, yes, Y, y, 1).
- Fix the ``add_file`` method of the ``TarArchive`` class.
- Fix ``select2`` widget in the metadata edit workflow action form.
- Update ``PyYAML`` from version 5.4.1 to 6.0.1.
- Update ``drf-yasg`` from version 1.20.0 to 1.21.7.
- Fix test that were asserting for True values instead of
  asserting for equality.

4.2.17 (2023-07-10)
===================
- Ensure only the filename of the uploaded file is used as the document
  label, omitting all path content.
- Backport MIME type file command backend improvements to make it more
  usable in series 4.2.
- Only clear the source error log if the source is enabled or was
  being tested.
- Fix the POP3 source uncompress choices. The choice asking users is
  not valid for a non interactive source.
- Include the `file` command in the Docker image to allow using it for
  MIME type detection.
- Reference the valid document as the event target when restoring a trashed
  document to allow the event to be accessible.

4.2.16 (2023-05-31)
===================
- Fix error in staging target Docker credential variable names. Closes
  GitLab issue #1143. Thanks to Matthias Löblich(@startmat) for the report.
- Fix workflow action test. Test was using the incorrect assertion type.
- Remove extra punctuation in help text. Text being concatenated already has
  punctuation.
- Fix document type change action form widget. The widget definition was
  incorrect causing the document type selector to use the regular HTML
  select widget.
- Split the Whoosh backend search object deletion and addition into separate
  try and exception blocks.
- CI documentation jobs improvements:

  - Install wheel to use modern Python package versions.
  - Don't install or build the Mayan EDMS Python package and
    instead use the development code to build the documentation.
  - Ensure APT proxy quotes are escaped.
  - Move Wheel dependency version to top level config file.

- Fix sitemap URL scheme format.
- Add release step flake8 command.
- Update the Docker Debian image from version 11.4-slim to 11.7-slim.
- Update the Redis Docker image from version 6.2.11-alpine to 6.2.12-alpine.
- Create a separate CSS class to handle unwanted second scrollbar on forms
  with an embedded carousel on Firefox. Closes issue #1144. Thanks to
  Rodrigo EvilNet Olguin (@evilnet1), @qra, @vintager for report and
  Matthias Löblich (@startmat) for the research.
- Split ``DocumentTestMixin`` into ``DocumentTypeTestMixin`` and
  ``DocumentTestMixin``.
- Retry trashed document deletion on database OperationalError.
  On large number of documents or document with many pages, the level
  of deletions exceed the database capacity to fulfill them. This
  causes a query deadlock where one database process waits for a
  ShareLock on a transaction which itself is blocked by another
  ShareLock on the previous transaction.

  After a timeout period of this circular transaction dependency
  an OperationalError exception will be raised and the trashed
  document deletion can be retried.

  Closes GitLab issue #1146, thanks to DS (@dshah01) for the report.
- Disable announcements app login template caching. Fixes announcement edits
  not showing up. Thanks to forum user @jwolfe for the report and debug
  information.
- Add documents app task testing module.
- Add events assertion to the document models test module.
- Django was updated from version 3.2.16 to 3.2.19.
- Reduce the amount of search update tasks during many to many model
  additions.

4.2.15 (2023-04-14)
===================
- Merged changes from version 4.1.12:

  - Fix sources app migration 0027 backend mapping path.
  - Include bug fixes and updates from version 4.0.24.
  - Don't include local config values in app settings. Local config values are
    meant to override CI/CD and test settings, and not meant to be committed
    as permanent to the repository.
  - Improve deployment stages:

    - Use long setting versions.
    - Clean up volumes using the official method.
    - Pull images to ensure the latest copy is used even if the image
      has the same tag as the remote.

4.2.14 (2023-03-09)
===================
- Merged changes from version 4.1.11:

  - Removal of the Transifex Python client.
  - Support a local environment config file names ``config-local.env``.
  - Support multi `psycopg2` versions for testing. Upgrade testing now uses
    ``PYTHON_PSYCOPG2_VERSION_PREVIOUS`` for the previous version when testing
    against PostgreSQL.
  - Move the helper module ``version.py`` to the dependencies app.

- GitOps improvements and backports:

  - Add configurable remote branch for GitOps.
  - Add makefile targets to trigger standalone builds.
  - Reuse Python build in stages.
  - Convert branches into literals.
  - Remove duplicated code in jobs.
  - Split GitLab CI targets into their own makefile.
  - Increase artifact expiration.
  - Add PIP and APT caching to documentation and python build
    stages.
  - Add GitLab CI job dependencies.
  - Enable Buildkit builds.
  - Use APT proxy and cache in more places.
  - Cache Alpine APK packages.
  - Clean up cache directory definitions.
  - Update APT cache to be at ``.cache/apt``.
  - Add multi cache support.
  - Add GitLab CI cache template tags.
  - Update deployment stages.
  - Don't push to the master branch on nightly or testing releases.
  - Load config.env in all jobs.
  - Move common SSH initialization to its own template tags.
  - Convert YAML triple ''' quotes to a single quote.

- Sanitize tag labels to avoid XSS abuse (CVE-2022-47419: Mayan EDMS Tag XSS).
  This is a limited scope weakness of the tagging system markup that can be
  used to display an arbitrary text when selecting a tag for attachment to
  or removal from a document.

  It is not possible to circumvent Mayan EDMS access control system or
  expose arbitrary information with this weakness.

  Attempting to exploit this weakness requires a privileged account and
  is not possible to enable from a guest or an anonymous account. Visitors
  to a Mayan EDMS installation cannot exploit this weakness.

  It is also being incorrectly reported that this weakness can be used to
  steal the session cookie and impersonate users. Since version 1.4
  (March 23, 2012) Django has included the ``httponly``
  attribute for the session cookie. This means that the session cookie data,
  including ``sessionid``, is no longer accessible from JavaScript.
  https://docs.djangoproject.com/en/4.1/releases/1.4/

  Mayan EDMS currently uses Django 3.2. Under this version of Django
  The ``SESSION_COOKIE_HTTPONLY`` defaults to ``True``, which enables the
  ``httponly`` for the session cookie making it inaccessible to JavaScript
  and therefore not available for impersonation via session hijacking.
  https://docs.djangoproject.com/en/3.2/ref/settings/#session-cookie-httponly

  Django's ``SESSION_COOKIE_HTTPONLY`` setting is not currently exposed by
  Mayan EDMS' setting system, therefore it is not possible to disable this
  protection by conventional means.

  Any usage of this weakness remains logged in the event system making
  it easy to track down any bad actors.

  Due to all these factors, the surface of attack of this weakness is
  very limited, if any.

  There are no known actual or theoretical attacks exploiting this
  weakness to expose or destroy data.
- Add a custom REST API exception handler to workaround inconsistent
  validation exception behavior in Django REST framework
  (https://github.com/encode/django-rest-framework/issues/2145).
- Add OCI metadata annotations

4.2.13 (2022-12-18)
===================
- Fix document file and document version print form submit button.
- Fix tagged document list view permission filtering. The permission
  layout remains the same. Only the method in which the permissions is
  checked was updated.
- Fix metadata add action actor assignment. This assignment is not
  currently used by either the view or the API which assign the actor
  directly themselves.
- Silence Docker Compose warning "MAYAN_WORKER_CUSTOM_QUEUE_LIST variable
  is not set". Closes GitLab issue #1129. Thanks to GR Buck (@graybuck)
  for the report.

4.2.12 (2022-11-13)
===================
- Fixes from version 4.1.10.
- Add a subclass of ``Path`` that adds the method ``is_relative_to`` for
  Python versions lower than 3.9.
- Add a patch for Python's CVE-2007-4559
  (https://nvd.nist.gov/vuln/detail/CVE-2007-4559).

  This is a language level vulnerability which exposed older versions
  of Mayan EDMS only when downloading JavaScript dependencies from the NPM
  registry.

  Exploiting this vulnerability requires compromising an existing package
  hosted on the NPM registry and adding Python code specifically targeting
  Mayan EDMS. As part of the project's design philosophies, dependencies
  are only downloaded from authoritative locations and each dependency is
  pinned to a specific version to guarantee immutable releases.

  Due to all these factors surface of attack of this vulnerability is
  very limited for older versions of Mayan EDMS, it is also very improbable,
  very difficulty to accomplish and very difficult to remain undetected.

  There are no known actual or theoretical attacks for Mayan EDMS
  exploiting this vulnerability.

  Thanks to the TrellixVulnTeam for the pull request which lead to this
  Mayan EDMS specific patch.

4.2.11 (2022-11-05)
===================
- Update Django from version 3.2.14 to 3.2.16.

4.2.10 (2022-08-20)
===================
- Make file improvements. Don't require a local ``psql`` client to
  launch the PostgreSQL development container. Don't require a local
  Redis client to launch the Redis development container. Fix the
  staging targets.
- Display exception errors to console when Celery fails to initialize.
- Use the ``DownloadFile`` filename attribute if available when performing
  the actual download action. Fall back to the previous logic of the
  string representation of the download file if the filename attribute
  is not set.
- Ensure cabinet document is added using the correct method when using the
  upload wizard. Closes GitLab issue #1118. Thanks to
  haithoum (@haithembenammar) for the report.
- Improve cabinet, metadata, and tag app tests.
- Ensure document tag is attached using the correct method when using the
  upload wizard. Same issue to GitLab issue #1118. Thanks to
  haithoum (@haithembenammar) for the initial report.

4.2.9 (2022-08-04)
==================
- Add permission filtering to the source switch links. The permission
  filtering will be the same as the views: document create permission for the
  source links during document uploads and document file new permissions
  for the source links in the new document file upload view.
- Don't cache the impersonation and the settings app templates. This ensures
  the impersonation banner and settings change banner are triggered
  correctly in all edge cases where multiple frontend processes or load
  balancers are used.
- Add make file development targets ``setup-dev-operating-system-packages``
  and ``setup-dev-python-libraries``.

4.2.8 (2022-07-22)
==================
- Fix the permission requirement of the recently created documents dashboard
  widget. The widget should filter by document view and not document type
  view permission. Thanks to forum user LeVon Smoker (@lsmoker) for
  the report.
- Update Django from version 3.2.13 to 3.2.14.
  https://docs.djangoproject.com/en/4.0/releases/3.2.14/
- Update Pillow from version 8.3.1 to 8.3.2.
- Update cryptodome from version 3.10.1 to 3.10.4.
- Remove the package ``firefox-geckdriver`` from the make file target
  ``setup-dev-environment`` as it is no longer available in recent OS LTS
  releases.
- Update the GitLab CI file to support releasing testing build of the
  Python library and the Docker image separately.
- Update Docker Debian base image from debian:11.3-slim to to
  debian:11.4-slim. https://www.debian.org/News/2022/20220709
- Update PyPDF2 from version 1.26.0 to 1.28.4. Closes GitLab issue #1106.
  Thanks to Stefan Denker (@denkerszaf) for the report and investigation.
- Update Sphinx from version 3.5.4 to 4.5.0 to avoid bug #9038.

4.2.7 (2022-07-01)
==================
- Intercept document file and document version page transformation errors
  and show a corresponding error template. This allows accessing the page
  to fix the transformation error. Closes GitLab issue #1101. Thanks to
  Munzir Taha (@munzirtaha) for the report.
- Backport search fixes from 4.3:

  - Normalize how the search "Match all" parameter is evaluated.
  - Fix evaluation of "Match all" when using a single level scoped search.
  - Improve extraction of URL search query parameters.

4.2.6 (2022-06-25)
==================
- Backport document content parsing template method. This fix
  allows accessing the parsed content of a document directly
  in a template.
- Backport permission form widget choice grouping and sorting improvements.

4.2.5 (2022-05-21)
==================
- Remove unused authentication view.
- Task manager app updates:

  - Add backend Celery queue deduplication to the ``CeleryQueue``.
  - Enable app tests.
  - Add and improve tests.
  - Add support for runtime removal of queues.

- Remove unused event link.
- Make document version OCR submit view messages translatable.
- Make file caching purge view messages translatable.
- Make document file metadata submit view messages translatable.
- Fix asset transformations hash calculation.
- Fix asset image API view docstring.
- Fix repeated model manager definition in ``DocumentFilePage``
  models.
- Transformation improvements:

  - Fix wrong parameter in the ``ImageDraw.Draw`` usage of the
    ``TransformationDrawRectangle`` transformation.
  - Add sanity check to reject negative zoom values for the
    ``TransformationZoom`` transformation.

- Add warning message when users attempting to delete their own accounts.
- Convert the signal handler that triggers search indexing on many to many
  fields changes into a background task. Solves user interface blocking
  when changing the document type to index template association on large
  installations.
- Update Django from version 3.2.12 to 3.2.13.
- Retry search indexing task when the object is not found. There are
  situations where the broker will route the message to the workers faster
  than the database can commit the data.
- Fix favorite document links reacting to favorite documents beyond the
  active user. Closes GitLab issue #1104. Thanks to
  Biel Frontera (@bielfrontera) for the report and initial implementation.

4.2.4 (2022-04-29)
==================
- Fix the documentation paths to the OTP backends. Closes GitLab
  issue #1099. Thanks to Matthias Löblich (@startmat) for the
  report.
- Fix Docker pull counter.
- Remove repeated Whoosh backend line of code from merge.
- Add portainer installation files and documentation.
- Remove hardcoded search model variable name from ``search_box.html``
  template.
- Fix the search model API URL reference. Closes GitLab issue #1098. Thanks
  to Bastian (@Basti-Fantasti) for the report.
- Use the ``SEARCH_MODEL_NAME_KWARG`` instead of hard coding the search model
  API URL reference.
- Filter trashed documents from the tag document count column.
- Filter trashed documents from the cabinet document retrieval method. This
  brings code parity with tags which work in a very similar way.
- Improve Python 3.10 compatibility. Add a compatibility module to
  encapsulate import of the ``Iterable`` class. Improves GitLab issue #1083.
  Thanks to Bw (@bwakkie) for the report and code samples.
- Type cast LUT values when masking an asset for pasting via Pillow's
  ``point()``.
- Document metadata edit form validation updates:

  - Remove ``disabled`` attribute from the metadata type label field to
    avoid having its value removed when there is a validation error.
  - Remove the ``required`` flag from the value field when there is a
    required metadata for a document. The previous behavior cause the tabular
    form to display "(required)" in column title confusing users and causing
    them to think that all metadata type fields were required.
  - Raise validation error for specific required metadata entries and no for
    the entire form. This help users better understand which metadata field
    needs to be corrected.
  - Improve the required metadata validation logic to take into account
    existing values and empty forms when data was entered into the field
    but the update checkbox was left unchecked.

- Bulk object search indexing updates:

  - Retry failed bulk indexing tasks.
  - Add max retry value to ``task_index_search_models``.
  - Improve tasks error logging.

- Update the Debian Docker image from version 11.2-slim to 11.3-slim.
- Downgrade the Python Docker image from version 3.11-slim to 3.10-slim.
- Pin Jinja2 version to workaround Sphinx bug. Sphinx Jinja2 dependency is
  not pinned or immutable, and causes the installation of an incompatible
  version breaking builds.

4.2.3 (2022-04-01)
==================
- Add restart policy to the Traefik container definition.
- Remove duplicated ``Document.get_label`` method.
- Fix an issue where a staging folder would not tag uploaded
  documents.

4.2.2 (2022-03-21)
==================
- Ensure the object copy permission is required for the object copy link.
- Migrate old workflow ``EmailAction`` instances instead of sub-classing
  for backwards compatibility. Improves commit
  ``b522dac80f7f6cfb8c5db8a74d6d2d22bc8b281a`` and avoids a double entry in
  the workflow state action selection downdown list.
- Ensure new document and file links access works like their respective
  views. The links will be active when the access is granted for the source
  as well as the document/document type.
- Filter unread message count badge by message read permission.
- Update document metadata model field label from "Metadata type value"
  to "Metadata value".
- Fix document file signature serializer label.

4.2.1 (2022-02-16)
==================
- Merge improvements from version 4.1.6.

  - Append the text "signed" to the label of a signed document file instead
    of using the temporary filename used during signing.
  - Ensure the signed document file is used when the file downloaded is
    requested and when calculating the signed document file checksum.
    Solves issue in forum post 6149. Thanks to forum user @qra for the report
    and debug information.
  - Update IMAP source ``store commands`` to be optional.
  - Update email sources ``SSL`` checkbox to be optional.
  - Undo POP3 source context manager changes from commit
    c19040491e20c9a783ae6191613bc8c5f7acb038. It seems Python's email libraries
    do not have feature parity. ``imaplib`` was updated to support context
    managers but ``poplib`` was not.

- Update requirements to specify Python version 3.6 to 3.9.
- Update Django version 3.2.11 to 3.2.12.

4.2 (2022-02-12)
================
- Update Django to version 3.2.11.
- Update django-widget-tweaks from version 1.4.8 to 1.4.9.
- File staging sources updates:

  - Use ``StreamingHttpResponse`` to serve previews.
  - Support office document files for preview.
  - Fix extra brackets in the encoded and cached filenames.
  - Simplify image generation.
  - Use context manager to ensure preview images are always closed.

- Hide all links that depend on users being authenticated.
- Add support for return binary content in batch API requests as a base64
  string.
- Add support for dynamic field API serialization. This feature adds the
  URL query keys ``_fields_only`` and ``_fields_exclude``. Nested serializers
  are supported using the double underscore (``__``) separator.
- Refactor ``ResolverRelatedManager``.
- Move Docker templates to their own folder.
- Move the ``docker-dockerfile-update`` target to the Docker makefile.
- Update Docker image tags:

  - PostgreSQL from 10.18-alpine to 12.9-alpine.
  - Python from 3.8-slim to 3.11-slim.

- Update psycopg2 from version 2.8.6 to 2.9.2.
- Update redis client from version 3.5.3 to 4.0.2.
- Reduce the Sentry client default ``traces_sample_rate`` from 0.25 to 0.05.
- Add the ``run_initialsetup_or_performupgrade`` command to the Docker
  entrypoint.
- Docker Compose updates:

  - Add a Redis profile.
  - Default to RabbitMQ a broker.
  - Change default RabbitMQ image from 3.9-alpine to 3.9-management-alpine.
  - Improve Traefik configuration.
  - Add a dedicated network for Traefik.

- Completed the Whoosh backend and made it the default search backend.

    - Ensure all test models are deleted, including intermediate many
      to many models created automatically.
    - Update ``DetailForm`` usage for the new interface.
    - Move `flatten_list` to the common app.
    - ResolverPipeline updates:

      - Support ``resolver_extra_kwargs``.
      - Add queryset exclusion support to ``ResolverRelatedManager``.

    - Update related field resolution using pure Django
    - Solve all search indexing edge cases.
    - Models are indexed using smaller tasks to improve scalability.
    - Refactor ``ResolverRelatedManager``. Use Django's internal
      ``get_fields_from_path`` for related field introspection.
      Support more related field cases.
    - Trigger indexing on related model changes
    - Fix lock manager management command test.
    - Don't index `None` values in lists.
    - Unify the search test mixins.
    - Use ``TemporaryDirectory`` for test search backend. Do automatic
      clean up of the temporary index directory.
    - Remove the separate related model index signal handlers.
    - Make Whoosh the default search backend.
    - Support reverse many to many indexing.
    - Add indexing optimizations.
    - Rename methods for clarity.
    - Move the ``any_to_bool`` function to the common app.

- Update base image from Debian 10.10-slim to 11.1-slim.
- Move the ``parse_range`` utility from the documents app to the common app.
- Retry Whoosh LockErrors by encapsulating then in the general app exception
  ``DynamicSearchRetry``.
- Added the ``search_index_objects`` management command to trigger the
  queuing of search models from the CLI.
- Added the ``search_status`` management command to show indexing status of
  the search backend.
- Move SQLite check to the databases app.
- Add support for inclusion and exclusion regular expressions for watch
  folders. Closes GitLab issue #965. Thanks to Sven Gaechter (@sgaechter)
  for the request.
- MIME type app updates:

  - Add support for MIME type detection backends.
  - Add PERL ``mimetype`` backend.
  - Add Linux ``file`` command backend.
  - Rename ``mimetype`` app to ``mime_types``.

- Add a search backend for Elastic Search.
- Search app updates:

  - Support initializing the search backends.
  - Add method to reset backends.
  - Moved ``get_resolved_field_map`` and ``get_search_model_fields`` to the
    ``SearchBackend`` class.
  - Normalize true values for scope 0 ``match_all``.
  - Added a new task ``task_reindex_backend`` to abstract backend reindexing.
  - Add constant maximum retries value to the ``task_deindex_instance`` and
    ``task_index_instance`` tasks.
  - Add ranged search model indexing.
  - Add the ``search_slow`` queue for long running search tasks.
  - Support backend initialization, reset, and tear down.
  - Automatically add the ``id`` field as a search field for all search
    models.
  - Separate backend initialization from app initialization.

- Add Elasticsearch test container makefile targets.
- Unify the files ``.env`` and ``env_file``.
- Switch all standalone containers to use a ``prefetch-multiplier`` of ``1``.
- Change the Docker Compose network name from ``bridge`` to ``mayan``.
- Add the ``search_initialize`` and ``search_upgrade`` management commands.
  These are called automatically after the initial setup and after upgrades.
- Add new search settings called ``SEARCH_INDEXING_CHUNK_SIZE`` to set the
  number of objects to prepare when performing bulk indexing.
- Metadata validation and parsing updates:

  - Expand the parser and validator path fields to 224 characters.
  - Add automatic registration of parsers and validators.
  - Add support for passing arguments to parsers and validators.
  - Add a regular expression parser to replace values and a regular
    expression validator.

- Authentication refactor:

  - Subclass Django's authentication views to add multi form and multi factor
    authentication.
  - Add support for authentication backends. Authentication backends are
    able to control and customize the entire login process, including
    the forms presented to the user. Authentication backends can use mixins
    and can be subclassed to mix and expand their capabilities.
    Included authentication mixins: ``AuthenticationBackendRememberMeMixin``
    Included authentication backends:
    ``AuthenticationBackendModelDjangoDefault``,
    ``AuthenticationBackendModelEmailPassword``,
    ``AuthenticationBackendModelUsernamePassword``.
    Apps define authentication backends in the module
    ``authentication_backends.py``.
  - Removed the now unused ``EmailAuthBackend`` class.
  - New settings:

    - ``AUTHENTICATION_BACKEND`` which must be the dotted path
      to the backend used to process user authentication.
    - ``AUTHENTICATION_BACKEND_ARGUMENTS`` which is an optional YAML
      structure to pass to the authentication backend.

- Add Time based One Time Password (TOTP) support. To enable set the
  setting ``AUTHENTICATION_BACKEND`` to
  ``mayan.apps.authentication_otp.authentication_backends.AuthenticationBackendModelUsernamePasswordTOTP``
  for username and TOTP login. For email and TOTP logins use
  ``mayan.apps.authentication_otp.authentication_backends.AuthenticationBackendModelEmailPasswordTOTP``.
  New management commands to support OTP:

    - ``authentication_otp_disable``: disables OTP for a user
    - ``authentication_otp_initialize``: initializes the OTP state data for
      all users. This command is for debugging and maintenance in case the
      database migration does not correctly initialize the OTP state data
      for existing users.
    - ``authentication_otp_status``: display the OTP status for a user

- Add URL links to the document file and document version first pages
  to the document serializer in the API.
- Convert the download file deletion interval into a setting named
  ``DOWNLOAD_FILE_EXPIRATION_INTERVAL`` which defaults to 2 days.
- Convert the shared uploaded file deletion interval into a setting named
  ``SHARED_UPLOADED_FILE_EXPIRATION_INTERVAL`` which defaults to 7 days.
- Don't display API URL links to indexing instance and template parents that
  are also root nodes as these are not accessible.
- Register more models using ``DynamicSerializerField`` to display the
  canonical serializer of the model when referenced by other objects.
- For object that have children objects or that support nesting, the parent
  object ID is now added to the serializer. The layout is
  ``{parent object name}_id``. A few objects already provided the parent ID
  but with a different schema. These objects also now have the parent ID
  field with the new schema even if it displays a duplicate value. The old
  ID field is now deprecated and will be removed in version 5.0.
- Added a workflow state column displaying all created actions labels
  separated by a comma.
- Added the mailing profile created and edited events.
- User menu and views updates:

  - Reorganize all user links under a single "User details" link.
  - Allow editing the locale profile of users.
  - Allow editing the theme settings of users.
  - Unify user data related views.
  - Add "User theme edited" and "User locale profile edited" events.

- Update the Django debug view CSS and layout to match Django's original
  appearance.
- Support Django debug JavaScript code.
- Minor CSS optimization to the Django debug view.
- Add Docker Compose password randomizer.
- Include LDAP libraries and Python modules.
- Events app updates:

  - Use the correct attribute for fetching event types. Use ``id`` instead of
    ``name``.
  - Cache the event type instance in the StoredEvent model.
  - An incorrect event type ID will now return a KeyError instead of masking
    the exception and returning an error message. It is now up to the calling
    code which action to take when the event type ID is not correct.
  - The previous unknown event error message is now available as a literal
    named ``literals.TEXT_UNKNOWN_EVENT_ID``.

- Add workflow template transition trigger API. Closes GitLab
  issue #1044. Thanks to Ludovic Anterieur (@lanterieur) for
  the request and research.
- Fine tune workflow template permissions to require the view permission
  instead of the edit permission when applicable.
- Error log updates:

    - Added a global error log list to the tools menu.
    - Error log partitions now link to their underline object via content type
      too.
    - Error log partitions are now retrieve or created on demand.
    - Added cascade permission support to error log partitions and entries.

- Update the ``ObjectActionAPIView`` view to allow passing extra context to
  serializers.
- Add support for launching workflows from the API.
- Refactor language activation to work with Django 3.2.
- Added the mailing profile created and edited events.
- Remove workflow instance exception usage. Current state property is now
  inspected.
- Remove menu proxy inclusions. Model proxies are now included by default.
- Add menu proxy exclusions.
- Update the subject and body fields of the document email workflow action
  to be optional.
- Redirect to current user to user detail view after password change.
- Support two different ``psycopg2`` versions for upgrade testing.

4.1.12 (2023-04-14)
===================
- Fix sources app migration 0027 backend mapping path.
- Include bug fixes and updates from version 4.0.24.
- Don't include local config values in app settings. Local config values are
  meant to override CI/CD and test settings, and not meant to be committed
  as permanent to the repository.
- Improve deployment stages:

  - Use long setting versions.
  - Clean up volumes using the official method.
  - Pull images to ensure the latest copy is used even if the image
    has the same tag as the remote.

4.1.11 (2023-03-08)
===================
- Install OS and Python dependencies as separate makefile targets.
- Remove the Python Transifex client. The new Go based client is required to
  be installed manually when working with translations
  (https://github.com/transifex/cli).
- Sanitize tag labels to avoid XSS abuse (CVE-2022-47419: Mayan EDMS Tag XSS).
  This is a limited scope weakness of the tagging system markup that can be
  used to display an arbitrary text when selecting a tag for attachment to
  or removal from a document.

  It is not possible to circumvent Mayan EDMS access control system or
  expose arbitrary information with this weakness.

  Attempting to exploit this weakness requires a privileged account and
  is not possible to enable from a guest or an anonymous account. Visitors
  to a Mayan EDMS installation cannot exploit this weakness.

  It is also being incorrectly reported that this weakness can be used to
  steal the session cookie and impersonate users. Since version 1.4
  (March 23, 2012) Django has included the ``httponly``
  attribute for the session cookie. This means that the session cookie data,
  including ``sessionid``, is no longer accessible from JavaScript.
  https://docs.djangoproject.com/en/4.1/releases/1.4/

  Mayan EDMS currently uses Django 3.2. Under this version of Django
  The ``SESSION_COOKIE_HTTPONLY`` defaults to ``True``, which enables the
  ``httponly`` for the session cookie making it inaccessible to JavaScript
  and therefore not available for impersonation via session hijacking.
  https://docs.djangoproject.com/en/3.2/ref/settings/#session-cookie-httponly

  Django's ``SESSION_COOKIE_HTTPONLY`` setting is not currently exposed by
  Mayan EDMS' setting system, therefore it is not possible to disable this
  protection by conventional means.

  Any usage of this weakness remains logged in the event system making
  it easy to track down any bad actors.

  Due to all these factors, the surface of attack of this weakness is
  very limited, if any.

  There are no known actual or theoretical attacks exploiting this
  weakness to expose or destroy data.
- Pin Jinja2 version to workaround Sphinx bug. Sphinx Jinja2 dependency is
  not pinned or immutable, and causes the installation of an incompatible
  version breaking builds.
- Support a local environment config file names ``config-local.env``.
  This file is ignored by Git and meant to override values of ``config.env``.
- Support multi `psycopg2` versions for testing. Upgrade testing now uses
  ``PYTHON_PSYCOPG2_VERSION_PREVIOUS`` for the previous version when testing
  against PostgreSQL.
- Improve Python 3.10 compatibility. Add a compatibility module to
  encapsulate import of the ``Iterable`` class.
- Move ``SearchModel.flatten_list`` to the common app ``utils.py`` module.
- Move the helper module ``version.py`` to the dependencies app.
- GitOps improvements and backports:

  - Add configurable remote branch for GitOps.
  - Add makefile targets to trigger standalone builds.
  - Reuse Python build in stages.
  - Convert branches into literals.
  - Remove duplicated code in jobs.
  - Split GitLab CI targets into their own makefile.
  - Increase artifact expiration.
  - Add PIP and APT caching to documentation and python build
    stages.
  - Add GitLab CI job dependencies.
  - Enable Buildkit builds.
  - Use APT proxy and cache in more places.
  - Cache Alpine APK packages.
  - Clean up cache directory definitions.
  - Update APT cache to be at ``.cache/apt``.
  - Add multi cache support.
  - Add GitLab CI cache template tags.
  - Update deployment stages.
  - Don't push to the master branch on nightly or testing releases.

- Add a custom REST API exception handler to workaround inconsistent
  validation exception behavior in Django REST framework
  (https://github.com/encode/django-rest-framework/issues/2145).

4.1.10 (2022-11-13)
===================
- Fixes from version 4.0.23.

4.1.9 (2022-04-24)
==================
- Remove hardcoded search model variable name from ``search_box.html``
  template.

4.1.8 (2022-04-23)
==================
- Fix the search model API URL reference. Closes GitLab issue #1098. Thanks
  to Bastian (@Basti-Fantasti) for the report.
- Use the ``SEARCH_MODEL_NAME_KWARG`` instead of hard coding the search model
  API URL reference.
- Merged changes from version 4.0.22:

  - Remove usage of flat values list in document checkout manager.
  - Remove usage of flat ``values_list`` queryset in metadata managers module.
  - Cleanup markup of the confirmation form.
  - Remove redundant modal close button.
  - Fix search proxies method decorator.
  - Reorganize converter office MIME type list.
  - Improve metadata validation error message.
  - Don't display API URL links to indexing instance and template parents that
    are also root nodes as these are not accessible.
  - Remove repeated partition file close call.
  - Update Django version 2.2.24 to 2.2.28.

- Reduce the Sentry client default ``traces_sample_rate`` from 0.25 to 0.05.
- Add keyword argument to ``self.stderr`` and ``self.stdout`` usage.
- In ``FilteredRelatedFieldMixin``, split retrieval of the queryset to
  avoid the exception handler from capturing an ``AttributeError`` that it
  shouldn't.
- Updated the ``subject`` and ``body`` fields of the document email
  workflow action to be optional.
- Migrate old workflow ``EmailAction`` instances instead of sub-classing
  for backwards compatibility. Improves commit
  ``b522dac80f7f6cfb8c5db8a74d6d2d22bc8b281a`` and avoids a double entry in
  the workflow state action selection dropbox.
- Partials navigation updates:

  - Streamline JavaScript partials navigation code.
  - Make the AJAX response redirect code configurable. New setting
    ``APPEARANCE_AJAX_REDIRECTION_CODE`` added.
  - Remove repeated AJAX redirection middleware.

- Add keyword arguments to zip file calls.
- ``PartialNavigation.js`` improvements.

  - Clean URL query on form submit and use form data as the URL query.
  - Remove dead code.
  - Use constants where appropriate.

- Backport new document link condition logic. Ensure new document and file
  links access works like their respective views. The links will be active
  when the access is granted for the source as well as the document/document
  type. Closes GitLab issue #1102. Thanks to Julian Marié (@Angelfs) for the
  report and debug information.
- Improve logic of the new document file link

  - Access the view user in a more reliable way.
  - Test the new file permission of the document and not
    of the document type.
  - If no document is present in the view exit fast.
  - Update tests.

4.1.7 (2022-04-01)
==================
- Backport fixes from version 4.2.3

  - Add restart policy to the Traefik container definition.
  - Remove duplicated ``Document.get_label`` method.
  - Fix an issue where a staging folder would not tag uploaded
    documents.
  - Fix document file signature serializer label.
  - Update document metadata model field label from "Metadata type value"
    to "Metadata value".
  - Filter unread message count badge by message read permission.
  - Update signature view permission label from
    "View details of document signatures" to "View document signature".
  - Ensure the object copy permission is required for the object copy link.
  - Fix ``GUNICORN_REQUESTS_JITTER`` documentation setting name reference.

4.1.6 (2022-02-15)
==================
- Append the text "signed" to the label of a signed document file instead
  of using the temporary filename used during signing.
- Ensure the signed document file is used when the file downloaded is
  requested and when calculating the signed document file checksum.
  Solves issue in forum post 6149. Thanks to forum user @qra for the report
  and debug information.
- Update IMAP source ``store commands`` to be optional.
- Update email sources ``SSL`` checkbox to be optional.
- Undo POP3 source context manager changes from commit
  c19040491e20c9a783ae6191613bc8c5f7acb038. It seems Python's email libraries
  do not have feature parity. ``imaplib`` was updated to support context
  managers but ``poplib`` was not.
- Update requirements to specify Python version 3.5 to 3.9.
- Update Django version 2.2.24 to 2.2.27.

4.1.5 (2022-02-03)
==================
- Fix CAA document links. Closes GitLab issue #1068. Thanks to
  Matthias Löblich (@startmat) for the report.
- Remove superfluous apostrophe character in sort heading markup.
- Fix email sources processing a single message but performing cleanup on
  multiple messages. The intended behavior is restore which processed one
  message and cleans up the processed message only.
- Fix reference to ``shared_uploaded_files`` before the variable being
  available.
- Use context managers for the IMAP and POP3 sources to remove the
  possibility of orphaned descriptors.
- Create error log entries for objects that existed before the last error
  log changes. Fix GitLab issue #1069. Thanks to Will Wright (@fireatwill)
  for the report.
- Expose the workflow template ``auto_launch`` field via the REST API.
  Thanks to forum user @qra for the request.
- Add ``EmailAction`` subclass for backwards compatibility with existing
  workflow state actions.
- Expose the checkout datetime, expiration datetime and user fields via the
  REST API. Thanks to forum user @qra for the request.
- Print configuration path value when failing to access error is raised.
- Fix references to the ``SourceBackendSANEScanner`` source backend class.
- Reorganize the testing setting modules.
- Remove unused MySQL testing setting module.

4.1.4 (2021-12-01)
==================
- Changes merged from versions 4.0.20 and 4.0.21.

  - Perform more strict cleanup of test models.
  - Clean up the test model app config cache after the test
    end not before the test model is created.
  - Improve lock manager test cases.
  - Add standalone Celery beat container.

- Fix document version first page thumbnail image resolution.
  Closes GitLab issue #1063. Thanks to Will Wright (@fireatwill)
  for the report and the patch.
- Add libjpeg and libpng to the dev setup target.
- Fix editing OCR content via the API.
- Fix the ``AdvancedSearchViewTestCaseMixin`` class. It had
  ``GenericViewTestCase`` as a base class when it is supposed to be a mixin
  and not have any.
- Add ``AutoHelpTextLabelFieldMixin``. This mixin tries to extract the
  label and help text from the model field when the serializer field does
  not specify any.
- Add filtering to the ``parent`` field of the index template node
  serializers. Restrict options to the current index template and allows
  removing the now redundant validation.
- Add ``index_template_root_node_id`` field to the index template
  serializer. Closes GitLab issue #1061. Thanks to
  Ludovic Anterieur(@lanterieur) for the report and initial implementation.
- Fix responsive menu close button triggering home navigation. Closes
  GitLab issue #1057. Thanks to Raimar Sandner (@PiQuer) for the report and
  debug information.
- JavaScript optimizations:

  - Cache argument length when in ``.fn.hasAnyClass``.
  - Configure fancybox just once.
  - Set converter image functions as ``async``.
  - Remove jQuery's ``one`` usage.

- Remove the error logger model locking and cache the model value instead
  at the time of registration. Closes GitLab issue #1065. Thanks to
  Will Wright (@fireatwill) for the report and debug information.
- Rename ``ErrorLog`` model to ``StoredErrorLog``. This change follow the
  normal paradigm when a service is provided by a model and a runtime class.
- Make the ``StoredErrorLog`` name field unique to ensure ``get_or_create``
  works in an atomic way.
- Create the error log partition when the model instance is created.
- Normalize the error log partition name format using a static method.
- Delete the error log partition on model instance deletion and not just the
  error log partition entries.
- Ensure a memory database is used when running the tests.

4.1.3 (2021-11-02)
==================
- Vagrant updates

  - Load installation value from ``config.env`` file.
  - Update supervisord during installation.
  - Setup the APT proxy during installation.
  - Change how APT and PIP proxies are defined to match the Docker build
    target.
  - Add makefile for vagrant.
  - Move devpi targets to the main makefile.

- Sentry client backend updates:

  - Add more SDK options.
  - Add typecasting to options.
  - Add debug logging.
  - Add Celery integration.
  - Add Redis Integration.
  - Lower the default value of ``traces_sample_rate`` from 1 to 0.25.
    This value is better suited for production deployments. Increase to 1
    for full debug information capture during development or testing.

- File staging sources updates:

  - Use ``StreamingHttpResponse`` to serve previews.
  - Support previews for office document files.
  - Fix extra brackets in the encoded and cached filenames.
  - Simplify image generation.
  - Use context manager to ensure preview images are always closed.

- Sources app updates:

  - Don't assume all source backends provide an upload form.
  - Improve SANE scanner error handling.
  - Fix logging of non interactive source errors.
  - Show interactive source processing as a message.

- Fix the copying of the bootstrap alert style.
- Optimize the copying of the Bootstrap alert style by executing it only
  in the root template. This runs the code just once instead of running it
  on each page refresh. The element ``#div-javascript-dynamic-content`` was
  also remove and it is now created and destroyed dynamically once just.
- Ensure that the ``resolved_object`` is injected into the context before
  passing the context to the link's ``check_condition`` method. Suspected
  cause of the GitLab issue #1052 and #1049. Thanks to Ludovic Anterieur
  (@lanterieur) and Johannes Bornhold (@joh5) for the reports and debug
  information.
- Converter updates:

  - Fix duplicate asset display. Closes GitLab issue #1053. Thanks to
    Ryan Showalter (@ryanshow) for the report.
  - Split the transformation ``cache_hash`` method to allow subclasses to
    modify how the cache hash is calculated.
  - Include the asset image hash into the asset transformation hash
    calculation. This change invalidates all cached page images that
    use an asset if the asset image is modified.
  - Improve the way the absolute coordinates of the percentage asset paste
    transformation are calculated.

- Use redirection instead of the ``output_file`` argument to allow the SANE
  scanner source to work with more SANE scanner versions.

4.1.2 (2021-10-27)
==================
- Don't insert the value ``ORGANIZATIONS_URL_BASE_PATH`` in the path
  then it is ``None``.
- Fix ``ModelTemplateField`` not displaying the ``initial_help_text``
  for the specific usage instance. The ``initial_help_text`` was
  being removed from the ``kwargs`` in the ``ModelTemplateField``
  as well as the super class.
- Workflows improvements.

  - Use the templating widget for the workflow document properties
    modification and the HTTP request actions.
  - Consolidate the workflow action help text.

- Fix issue when attempting to create a Document version page OCR update
  workflow action. Instead of the model class, the template form field now
  passes the ``app_label`` and the ``model_name`` of the model via the
  widget attributes to avoid Django's attribute template to attempt
  getting a string representation of the model.

4.1.1 (2021-10-26)
==================
- Move Docker Compose variables to the correct file. Move
  ``COMPOSE_PROJECT_NAME`` and ``COMPOSE_PROFILES`` to the
  .env file.
- Fix asset image generation. Closes GitLab issue #1047 for series 4.1.
  Thanks to Ryan Showalter (@ryanshow) for the report and debug information.
- Improve sidebar menu heading display logic.
- Fix leftover HTML markup in the server error dialog window.
- Remove redundant close button for the server error dialog window.
- Merged fixes and improvements from versions 4.0.17 and 4.0.18.
- Update PIP from version 21.2.4 to 21.3.1.
- Remove MySQL upgrade CD/CI testing pipeline stage until support is properly
  re-implemented for version 8.0.
- Add CD/CI triggers for local testing.
- Exclude all migration tests by tagging automatically at the
  ``MayanMigratorTestCase`` subclass definition.
- Support multiple environments per dependency.
- Update the ``wheel`` library to be a dependency of the ``build`` and the
  ``documentation`` environments to workaround a bug in PIP that causes
  ``"error: invalid command 'bdist_wheel'"``.

4.1 (2021-10-10)
================
- Add support for editing the document version page OCR content.
  Closes GitLab issue #592. Thanks for Martin (@efelon) for the
  request.
- Refactor sources app.

  - Add object permission support to source views.
  - Remove locking support from staging folder uploads.
  - Update staging preview to use new preview generation
    code.
  - Use streaming response to serve staging folder images.
  - Convert the sources from models into backend classes.
    The sources are now decoupled from the app. Each source
    backend can defined its own callbacks and use an unified
    background task.
  - Perform code reduction. Remove PseudoFile and SourceUploaded
    classes. Each source backend is now responsible for providing
    a list of shared uploaded files.

- Multiform improvements:

  - Support multi form extra kwargs.
  - Move the dynamic part of the multi form method to the end
    of the name.
  - Add a white horizontal ruler to separate the form
    instances.

- Consolidate the image generation task:

  - Remove document file, version, converter asset, and workflow template
    preview image generation.
  - Remove converter literal `TASK_ASSET_IMAGE_GENERATE_RETRY_DELAY`.
  - Remove workflow literals `TASK_GENERATE_WORKFLOW_IMAGE_RETRY_DELAY`.
  - Remove `document_states_fast` queue.
  - Remove documents literals
    `DEFAULT_TASK_GENERATE_DOCUMENT_FILE_PAGE_IMAGE_RETRY_DELAY` and
    `DEFAULT_TASK_GENERATE_DOCUMENT_VERSION_PAGE_IMAGE_RETRY_DELAY`.
  - Remove settings
    `DOCUMENT_TASK_GENERATE_DOCUMENT_FILE_PAGE_IMAGE_RETRY_DELAY` and
    `DOCUMENT_TASK_GENERATE_DOCUMENT_VERSION_PAGE_IMAGE_RETRY_DELAY`.

- Search updates

  - Remove `TASK_RETRY_DELAY` and use `retry_backoff`.
  - Add the tag color as a search field
  - Improve and simplify query cleaning up by doing so after the
    scopes are decoded.
  - Fix Whoosh reindexing after m2m fields perform a remove.
  - Fix Whoosh search for related m2m fields with multiple
    values.
  - Improve tests for edge cases.
  - Fix document version API tests module.
  - Variables renamed for clarity and to specify their purpose.
  - Process the 'q' parameter at the class and not in the
    backend.
  - Ignore invalid query fields.
  - Index for search on m2m signal.
  - Return empty results on an empty query.
  - Produce an empty scope 0 on an empty query.
  - Improve tests.
  - Add UUID field for all document child objects.

- Add detail view for groups.
- Show total permission when running the `purgepermissions` command.
- Add detail for file partitions.
- Add placeholder absolute links for announcements, workflow templates, quotas.
- Add detail view for stored permissions.
- Rename role setup views.
- Load user management first to allow patching
- Register ACL events when enabling ACLs. Objects that are registered to
  support ACLs will also be registered for ACL events to allow subscribing to
  ACL changes of the object.
- Allow bind either the events links, the subscription link, both or none.
- Improve workflow app navigation.
- Improve sidebar navigation.
- Improve clarity of the action dropdown sections.
- Make the index instance node value field an unique field among its own tree
  level. This prevents tree corruption under heavy load.
- Update dependencies:

  - Docker Compose from 1.29.1 to 1.29.2
  - PostgreSQL Docker image from 10.15-alpine to 10.18-alpine
  - RabbitMQ Docker image from 3.8-alpine to 3.9-alpine
  - Redis Docker images from 6.0-alpine to 6.2-alpine
  - psycopg2 from 2.8.6 to 2.9.1
  - psutil from 5.7.2 to 5.8.0
  - jQuery from 3.5.1 to 3.6.0
  - jquery-form from 4.2.2 to 4.3.0
  - jquery-lazyload from 1.9.3 to 1.9.7
  - urijs from 1.19.1 to 1.19.7
  - bleach from 3.1.5 to 4.0.0
  - jstree from 3.3.3 to 3.3.11
  - PyYAML from 5.3.1 to 5.4.1
  - django-model-utils from 4.0.0 to 4.1.1
  - requests from 2.25.1 to 2.26.0
  - sh from 1.14.1 to 1.14.2
  - devpi-server from 5.5.1 to 6.2.0
  - django-debug-toolbar from 3.1.2 to 3.1.4
  - django-extensions from 3.1.2 to 3.1.4
  - django-rosetta from 0.9.4 to 0.9.7
  - flake8 from 3.9.0 to 3.9.2
  - ipython from 7.22.0 to 7.26.0
  - safety from 1.9.0 to 1.10.3
  - transifex-client from 0.14.2 to 0.14.3
  - twine from 3.4.1 to 3.4.2
  - wheel from 0.36.2 to 0.37.0
  - Pillow from 7.1.2 to 8.3.1
  - packaging from 20.3 to 21.0
  - python_gnupg from 0.4.6 to 0.4.7
  - graphviz from 0.14 to 0.17
  - django-activity-stream from 0.8.0 to 0.10.0
  - pytz from 2020.1 to 2021.1
  - python-dateutil from 2.8.1 to 2.8.2
  - python-magic from 0.4.22 to 0.4.24
  - gevent from 20.4.0 to 21.8.0
  - gunicorn from 20.0.4 to 20.1.0
  - whitenoise from 5.0.1 to 5.3.0
  - cropperjs from 1.4.1 to 1.5.2
  - jquery-cropper from 1.0.0 to 1.0.1
  - django-cors-headers from 3.2.1 to 3.8.0
  - djangorestframework from 3.11.2 to 3.12.4
  - drf-yasg from 1.17.1 to 1.20.0
  - swagger-spec-validator from 2.5.0 to 2.7.3
  - dropzone from 5.7.2 to 5.9.2
  - extract-msg from 0.23.3 to 0.34.3
  - pycryptodome from 3.9.7 to 3.10.1
  - celery from 4.4.7 to 5.1.2
  - django-celery-beat from 2.0.0 to 2.2.1
  - coveralls from 2.0.0 to 3.2.0
  - django-test-migrations from 0.2.0 to 0.3.0
  - mock from 4.0.2 to 4.0.3
  - tox from 3.23.1 to 3.24.3
  - psutil from 5.7.0 to 5.80
  - furl from 2.1.0 to 2.1.2
  - django-test-migrations from 0.3.0 to 1.1.0

- Launch workflows when the type of the document is changed. Closes GitLab
  issue #863 "Start workflows when changing document type", thanks to
  Dennis Ploeger (@dploeger) for the request.
- Add support for deleting multiple metadata types in a single action.
- Tags app updates:

  - Use MultipleObjectDeleteView class.
  - Replace edit icon.
  - Code style updates.

- Move theme stylesheet sanitization to the save method.
- Remove final uses of .six library.
- Add support for clearing the event list.
- Events app updates:

  - Load all events at startup. Does not rely anymore of importing an event
    for it to become recognized.
  - Allow loading events by their name. Avoid doing direct imports when
    there circular dependencies.
  - Move the events app to the top of the installed apps to allow it to
    preload all events.
  - Only show the event clear and export links for object whose events
    that can be cleared and exported.

- ACLs apps updates:

  - The ACL edited event is now triggered only once when all permissions are
    changed.
  - The action object of the ACL edited event is now the content object and
    not the permission.

- Enable event subscriptions for workflow states, workflow state actions,
  and workflow transitions.
- Support deleting multiple roles in a single action.
- OCR app updates:

  - Use ``MultipleObjectDeleteView`` for the delete view.
  - Rename single and multiple delete view names.
  - Improve tests.

- Document comments app API updates:

  - Modernize code to use latest internal interfaces.
  - Exclude trashed documents.
  - Reduce serializers.
  - Return error 404 on insufficient access.

- Document indexing API updates:

  - Exclude trashed documents.
  - Split tests.
  - Add event checking to remaining tests.

- Events app API updates:

  - Return error 404 on insufficient permissions.
  - Modernize `APIObjectEventListView` to use latest interfaces
    and mixins.

- Document parsing app updates:

  - Update API to latest internal interfaces.
  - Add testing for multiple document file content delete views.
  - Speed up tests.
  - Add event checking to tests.
  - Use `MultipleObjectDeleteView` for the file content delete view.
  - Improve text string of the `DocumentFileContentDeleteView` view.

- Document signatures app updates:

  - Exclude trashed documents from the API.
  - Add event checking to tests.
  - Track user when uploading signature files.

- Workflows app updates:

  - Split API views.
  - Add trashed document test.
  - Code style updates.

- Smart link app refactor:

  - Exclude trashed documents from API.
  - Improve existing tests.
  - Add additional tests.
  - Rebuild the resolved smart link API and serializer.
  - Add a new permission to view resolved smart links. This permission needs
    to be granted for the smart link and for the document/document type.
  - Update API to return error 404 on insufficient access.
  - Remove unused test mixins.
  - Split view and API test modules.

- Documents app updates:

  - Exclude trashed documents from all API views.
  - New `valid` model managers for recently accessed, recently created, and
    favorite documents. These managers exclude trashed documents at the model
    level. The 'objects' manager for these model returns the unfiltered
    queryset.
  - Trashed document delete API now returns a 202 code instead of 204. The
    delete method now runs in the background in the same way as the trashed
    document delete view works in the UI. The return code was updated to
    reflect this internal change.
  - Track the user for the trashed document delete, restore and for the
    trash can empty methods.
  - Add event checking for some remaining tests.
  - Add additional tests.

- Add ``BackendDynamicForm``, a dynamic form for interacting with backends.
- Add a reusable backend class named ``mayan.apps.databases.classes.BaseBackend``.

- Refactor mailer app:

  - Allow sending document files and document versions as attachments.
  - Update the ``UserMailer`` model to work with the ``BackendModelMixin``
    mixin. This allows removing all backend managing code from the model.
  - Generate the dynamic form schema in the base backend class. Removes
    dynamic form schema from the views.
  - Use ``BackendDynamicForm`` and remove dynamic form code from the forms
    module.
  - Generalize document file and document version to support any type of
    object.
  - Update workflow action to send links to documents or attach the active
    versions.
  - Use the reusable ``BaseBackend`` class and remove explicit backend
    scaffolding.

- Improve test open file and descriptor leak detection.
- Close storage model file after inspection as Django creates a new
  file descriptor on inspection.
- Ensure the name and not the path is used. Compressed files can include
  path references, these are now scrubbed and only the filename of the file
  in the compressed archive is used.
- File handling was improved. Context managers are now used for temporary
  files and directories. This ensure file descriptors are closed and freed up
  in all scenarios.
- Add detached signature deleted event.
- Document signature app general improvements. Renamed links, icons and
  view for clarity. Split tests modules.
- Metadata API updates:

  - Unify document type metadata type serializers.
  - Update the permission layout to match the one of the views.
    The edit or view permission is now required for the document
    type as well as the metadata type.

- Add ``CONVERTER_IMAGE_GENERATION_MAX_RETRIES`` to control how many times
  the image regeration task will retry lock errors.
- Add support for appending all document file pages as a single document
  version.
- Moved signals, hooks and events outside of the document file creation
  transaction.
- Capture the user for the document version page reset and remap action
  events.
- Add conditions to the favorite document links.
- Update mailing icons.
- Remove submit button label and submit button icons.
- The ``performupgrade`` command won't try to hide critical errors and
  instead raise any exception to obtain the maximum amount of debug
  information.
- Add support to filter the add/remove choice form.
- Dependencies app updates:

  - Move the link to check for the latest version to the tools
    menu.
  - Checking for updates now required the view dependencies
    permission.

- Unify request resolution for navigation classes.
- Support retrieving a list of ``SourceColumn`` by name.
- Dashboard app updates:

  - Extend dashboard widget interfaces.
  - Add list dashboard widget.
  - Move dashboard CSS from the appearance app to the dashboards app.
  - Add dashboard list and detail views.
  - Add setting to select the default dashboard.
  - Add template tag to display the default dashboard in the home
    view.

- Refactor ``SourceColumn.get_for_source``.
- Add ``RecentlyAccessedDocumentProxy`` to allow adding a column with the
  creation date time.
- Navigation refactor:

  - Rewritten link to source matching code.
  - Rewritten menu resolution.
  - Pass the ``resolved_object`` to link conditions.

- Don't trigger the settings change flag on user language changes.
- Add settings to allow changing the default and the maximums
  REST API page size.
- Add support for service client backends to the platform app.
- Add Sentry.io service client backend.
- Support overriding form buttons.
- Improve metadata type form tab order. Disables metadata type name field
  to skip them during tabbing.
- Support step rewinding for the sources wizard.
- Add support for recoding email Message ID. The email source can now record
  an email Message ID from the header as it is processed into a documents.
  All documents created from the same email will have the same Message ID.
  Thanks to forum user qra (@qra) for the request.

- Improve `BaseBackend` class

  - Add deterministic parent base backend class detection.
  - Register backend class only to their respective parent base
    backend classes.

- Render main menu icons properly. The change in
  bbbb92edb85f192987fdfb4efc574bd79221b6ed removed literal CSS icon
  support. A single reference to the old CSS icon render was left behind
  which cause the icon object Python memory location to be rendered
  inline with the menu HTML. This cause the same menu to have different
  hashes when rendered by the different Gunicorn workers. Solved GitLab
  issue #1038. Thanks to Ludovic Anterieur (@lanterieur) for the report.
- Add setting to change the menu polling interval. Values specified in
  milliseconds. Use `None` to disable.
- Enforce ``CONVERTER_IMAGE_GENERATION_MAX_RETRIES`` setting and add logging
  message when the maximum retires are exhausted.
- Messaging app updates:

  - Add API views.
  - Exclude superusers and staff users from being message recipients.
  - Add dedicated create message form.
  - Use Select2 for the user selection field.
  - Add message edit permission. This permission is required in order to
    change the message read status.

- Add ``get_absolute_api_url`` method to download files, document versions
  and users. These URL are used to determine the message sender's API URL.
- Test view mixin updates:

  - Add a default ordering to the ``TestModel`` to silence warning.
  - Fix ``TestModel.save()`` method.
  - Support multiple test views per test case.
  - Allow subclasses to supply their own ``urlpatterns``.
  - Support passing arguments to ``add_test_view``.

- Add batch API request support.
- Adjust event registrations:

  - Register cabinet document add and remove events to the Document model too.
  - Register document file parsing events to the Document model too.
  - Rename label of the document parsed content deleted event.
  - Replace the ``DownloadFile`` content object registration from the
    ``Document`` model to the ``DocumentVersion`` model.
  - Register the document file created, edited events to the ``Document``
    model too.
  - Register the document version created, edited events to the ``Document``
    model too.
  - Register the document trashed event to the ``Document`` model too.
  - Remove the document file created event from the ``DocumentFile`` model.
  - Remove the document version created event from the ``DocumentVersion``
    model.
  - Register the document version page deleted event to the
    ``DocumentVersion`` model.
  - Remove the document version page deleted event from the
    ``DocumentVersionPage`` model.
  - Register the tag attached, removed events to the ``Document`` model too.
  - Register the web link navigated event to the ``Document`` model too.
  - Remove the document version page OCR edited event from the ``Document``
    model.
  - Register the document version OCR submitted, finished, content deleted
    events to the ``DocumentVersion`` model.

- Sort object and list facet links when using the list item view.
- Rename environment variable ``MAYAN_GUNICORN_JITTER`` to
  ``MAYAN_GUNICORN_REQUESTS_JITTER``.
- Support changing the operating system user when creating the supervisord
  file using the environment variable ``MAYAN_OS_USERNAME``.
- Reorder the Gunicorn arguments.
- Make the ``DJANGO_SETTINGS_MODULE`` environment variable an alias of
  ``MAYAN_SETTINGS_MODULE`` in the supervisord file.
- Add ``MAYAN_GUNICORN_TEMPORARY_DIRECTORY`` to the gunicorn invocation in
  the ``run_frontend.sh`` batch file.
- Frontend updates:

  - Ensure list groups use <ul> and <li> instead of plain <div>.
  - Move ``mayan_image.js`` to the converter app.
  - Update ``afterBaseLoad`` to work by defining a list of callbacks. This
    allows defining callbacks from different apps.
  - Set JavaScript callbacks and setup method to run in async mode.
  - Move static inline app CSS to individual CSS files.
- Fix workflow template API description text. Closes GitLab issue #1042.
  Thanks to Ludovic Anterieur (@lanterieur) for the report.
- Add document template state action API endpoints. Closes GitLab issue #1043
  Thanks to Ludovic Anterieur (@lanterieur) for the request.
- Pin jsonschema to version 3.2.0 to avoid errors with

4.0.24 (2023-04-14)
===================
- Split dev environment makefile target into OS and Python dependencies.
- Remove duplicated makefile target keys.
- Pin containers to specific bug fix versions.
- Enable organization app testing.
- Add check named ``check_app_tests`` to ensure Mayan apps tests
  flag matches the actual state of the app's tests.
- Backport ``CeleryQueue`` class improvements. Enable task manager app tests.

4.0.23 (2022-11-13)
===================
- Add help text to the ``SEARCH_BACKEND_ARGUMENTS`` setting.
- Backport an object storage documentation chapter fix
  from version 4.4dev0.
- Don't tag Docker images as ``latest`` for minor releases. As per Docker's
  specifications, the ``latest`` tag is applied to the latest image built
  if no tag is specified. It is not meant to represent the latest version
  of an project, just the last image that has been built. However users
  commonly (and mistakenly) have come to expect the ``latest`` tag to
  represent the latest version of the project. The GitLab CI file is
  updated to fulfill this expectation.
- Fixes from version 3.5.12.
- Pin ``importlib-metadata`` to version 4.13.0 to workaround a dependency
  bug in Kombu.
- Update tox from version 3.14.6 to 3.27.0.
- Update Debian container from tag 10.10-slim to 10.13-slim

4.0.22 (2022-04-22)
===================
- Filter unread message count badge by message read permission.
- Remove usage of flat values list in document checkout manager.
- Remove usage of flat ``values_list`` queryset in metadata managers module.
- Ensure the object copy permission is required for the object copy link.
- Update signature view permission label from
  "View details of document signature" to "View document signatures".
- Update document metadata model field label from "Metadata type value"
  to "Metadata value".
- Fix document file signature serializer label.
- Add restart policy to the Traefik container definition.
- Remove duplicated ``Document.get_label`` method.
- Add Docker Compose file port comment to remove when using Traefik.
- Print the path when failing to access the configuration file.
- Expose the workflow template ``auto_launch`` field via the REST API.
  Thanks to forum user @qra for the request.
- Cleanup markup of the confirmation form.
- Remove redundant modal close button.
- Fix search proxies method decorator.
- Reorganize converter office MIME type list.
- Improve metadata validation error message.
- Don't display API URL links to indexing instance and template parents that
  are also root nodes as these are not accessible.
- Remove repeated partition file close call.
- Update Django version 2.2.24 to 2.2.28.

4.0.21 (2021-11-29)
===================
- Perform more strict cleanup of test models.
- Clean up the test model app config cache after the test
  end not before the test model is created.
- Improve lock manager test cases.
- Add standalone Celery beat container.
- Backport transformation ``cache_hash`` method split.
  Moved to two functions to allow subclasses to modify
  how the cache hash is calculated.
- Backport asset image cache invalidation.
- Backport asset duplication fix.
- Backport asset percentage position calculation fix.
- Add an explicit default value for ``MEDIA_URL``. Ensures forward
  compatibility with future login dependency versions.
- Move meta tags to their own partial template.
- Add libjpeg and libpng to the dev setup target.

4.0.20 (2021-11-08)
===================
- Use overlay2 driver when using Docker in Docker
  in the GitLab CD/CI stages.
- Update gevent from version 20.4.0 to 21.8.0.
- Update gunicorn from version 20.0.4 to 20.1.0.
- Add more explicit serializer read only fields.

4.0.19 (2021-10-27)
===================
- Backported fixes from version 4.1.2:

  - ``ORGANIZATIONS_URL_BASE_PATH`` null value fix.
  - Fix ``ModelTemplateField`` not displaying the ``initial_help_text``.

4.0.18 (2021-10-21)
===================
- Add settings to allow changing the default and the maximum
  REST API page size.
- Ensure ``ORGANIZATIONS_URL_BASE_PATH`` is applied to properly
  trigger the root SPA template. Closes merge request !91. Thanks
  to Foo Bar(@stuxxn) for the original patch.
- Add support for setting validation.
- Validate the format of the ``ORGANIZATIONS_URL_BASE_PATH``
  setting.
- Smart setting test updates:

  - Add smart setting validation tests.
  - Add setting view tests.
  - Separate namespace and setting tests and mixins.

- Add MySQL workaround for unique document version activation added to
  migration documents 0067 in version 4.0.17.

4.0.17 (2021-10-18)
===================
- Backport workaround for swagger-spec-validator dependency
  bug. Pin jsonschema to version 3.2.0 to avoid errors with
  swagger-spec-validator 2.7.3. swagger-spec-validator does not specify a
  version for jsonschema
  (https://github.com/Yelp/swagger_spec_validator/blob/master/setup.py#L17),
  which installs the latest version 4.0.1. This version removes
  ``jsonschema.compat`` still used by swagger-spec-validator.
- Add ``project_url`` to the Python setup file.
- Add support for ``COMMON_EXTRA_APPS_PRE``. This setting works
  like ``COMMON_EXTRA_APPS`` but installs the new apps before the default
  apps. This allows the extra apps to override templates and other system
  data.
- Fix usage of ``.user.has_usable_password``. Use as a method not a flag.
  Fixes the `Change Password` link appearing even when using external
  authentication.
- Support blank app URL namespaces. These are used to register the
  ``urlpatterns`` of encapsulated libraries as top level named URLs.
- Add a stacked Font Awesome icon class.
- Ensure ``MAYAN_GUNICORN_TEMPORARY_DIRECTORY`` is exported and available to
  ``supervisord``.
- Always change the owner of ``/var/lib/mayan/``. Ensure that the ``mayan``
  operating system user can always read and write from and to the mounted
  volume.
- Fix asset image caching. Closes GitLab issue #1047 for series 4.0.
  Thanks to Ryan Showalter (@ryanshow) for the report and debug information.
- Expand help text of ``ORGANIZATIONS_INSTALLATION_URL`` and
  ``ORGANIZATIONS_URL_BASE_PATH`` settings. GitLab issue #1045. Thanks to
  bw (@bwakkie) for the report.
- Create the ``user_settings`` folder on upgrades too.
- Improve initial setup folder creation error logic. Add keyword arguments.
  Use storages app ``touch`` function.
- Ensure only one document version is active when migrating from version 3.5.
  Forum topic 9430. Thanks to forum user @woec for the report.

4.0.16 (2021-09-29)
===================
- Minor fixes merged from version 3.5.11.
- Remove duplicated makefile targets.
- Add keyword arguments to PIL methods.
- Quote parameters of remaining migration query.
- Track user when setting a version active.
- Fix menus randomly closing on refresh.
- Don't trigger the settings change flag on user language changes.
- Backport setting `CONVERTER_IMAGE_GENERATION_MAX_RETRIES`.
  This setting allows changing the image generation task maximum
  retry count. Celery's built in default value is 3, this setting
  increases that default to 7.

4.0.15 (2021-08-07)
===================
- Improve the document version export API endpoint.

  - Enable tracking the user and persisting the value for the events.
  - Change the view class form a custom mixin to be a subclass of
    `generics.ObjectActionAPIView` one.
  - Improve test to check for message creation after export.
  - Avoid returning an error when using the `GET` method for the view.

- Improve the `generics.ObjectActionAPIView` class.

  - Merge with `ActionAPIViewMixin`.
  - Add `action_response_status` for predetermined status codes.
  - Add message when the `.object_action` method is missing.

- Fix the view to mark all messages as read.
- Track the user when marking messages as read or unread.
- Fix action messages.

4.0.14 (2021-08-05)
===================
- Fix a regression in the document version page image cache maximum size
  setting callback.
- Fix converter layer priority exclusion for layers with a priority of 0.
  This fixes the preview layer priority when editing the redactions of pages
  that also contain transformations in other layers.

4.0.13 (2021-08-02)
===================
- Checkout test updates.

  - Silence debug output of tests.
  - Speed up tests using document stubs.

- Improve organization URL and host settings. Closes GitLab issues
  #966 and #1002. Thanks to None Given (@nastodon) and
  Bw (@bwakkie) for the reports.

  - Patch Django's HttpRequest object to override scheme
    and host.
  - Fix organization setting used to set the REST API URL
    base path.

- Track user for event when submitting a document version for OCR.
- Fix OCR version event texts.
- Update the document index list and document cabinet list links to require
  the same permission scheme as the views they reference.
- Add the document creation date time as a search field.

4.0.12 (2021-07-19)
===================
- Fix main menu active entry handling.
- Fix ID number in ``document_url`` attribute of the ``DocumentFile``
  and ``DocumentVersion`` serializers. Thanks to forum user @qra for the
  report. Topic 5794.
- Add API endpoint to display the list of valid transition options for a
  workflow instance. Thanks to forum user @qra for the report. Topic 5795.
- Add the workflow template content to the workflow instance API schema.
  Thanks to forum user @qra for the request. Topic 5795.
- Clarify purpose of project settings.
- Minor API serializer cleanups.
- Add explicit cabinet serializer read only fields.
- Fix multi scope search result initialization. Closes GitLab issue #1018.
  Thanks to Ryan Showalter (@ryanshow) for the report.
- Detect and report when a search scope does not specify a query.

4.0.11 (2021-07-06)
===================
- Update date time copy code from migration document:0063 to work with
  database that store time zone information and those that don't.
- Switch deployment instructions to use ``venv`` instead of ``virtualenv``.
- Add support for using local PIP cache to build Docker images.
- Add a Vagrant setup for testing. Integrates project
  https://gitlab.com/mayan-edms/mayan-edms-vagrant. Closes GitLab issue
  #937. Thanks to Max Kornyev (@mkornyev) for the report.
- Improve ``user_settings_folder`` variable creation. Works with
  ``MEDIA_ROOT`` paths with and without a trailing slash.
- The GitLab CI upgrade tests now update a test document to populate the
  older version install and trigger more migration code paths.
- Update all shell usage from ``bash`` to ``sh``. ``sh`` symlinks to ``dash``
  in the Docker image. This also expands the usability of the supervisor
  file for direct deployments in more operating systems. Closes GitLab
  issue #1013. Thanks to joh-ku (@joh-ku) for the report.
- Replace the ``wait.sh`` file with a Python alternative that can wait on
  network ports or PostgreSQL directly as a client.
- Upgrade ``supervisord`` from Debian buster version 3.3.5-1 to Debian
  bullseye version 4.2.2-2. This version uses Python3 and was the last
  dependency that required installing Python2 in the Docker image.
- Add the ``id`` field as sortable field in all the API that have ordering
  enabled.

4.0.10 (2021-07-02)
===================
- Simplify code block to delete OCR content of a document version.
- Make document version timestamp time zone aware before copying them over
  during migration.
- Split duplicates migration query into two separate queries to increase
  compatibility with database managers.
- Add support to the GitLab CI for local apt proxies.

4.0.9 (2021-06-29)
==================
- Improve scope search.

  - Support more than two source scopes per operator.
  - Support ``match_all`` logic per scope.
  - Support returning a single scope without using the operator output.
  - Disable search limits when multiple scopes are specified.
  - Add separate query decoding method.

- Increase the padding of the main menu panel anchors. Closes GitLab issue
  #1004. Thanks to Bw (@bwakkie) for the report.
- Rotate the main menu accordion indicator when opened or closed.
- Optimize jQuery usage of the $(this) object. Remove some unused jQuery
  code from the document card update methods.
- Add more uses of ``update_fields`` to ``.save()`` methods.
- Simplify logic using the document parser content update using
  ``update_or_create``.
- Raise document list errors on debug or testing.

4.0.8 (2021-06-23)
==================
- Update PIP to version 21.1.2.
- Use longer version of the Celery worker option.
- Make optional the `user_id` argument of
  `task_document_file_page_image_generate`.
- Another round of worker queue assignments tuning.
- Simplify the GPG temporary home preparation. A temporary directory context
  manager is now used that also guarantees that the temporary folder will be
  removed even on failures.
- Don't assume all signatures provide a ``date_time`` field.
- Optimize file and version page image API. Load the page object only once
  per request.
- Unify the supervisord templates. The direct deployment and the Docker image
  now use the same supervisord template.
- Email the active document version. Instead of emailing the latest updated
  document file, the document emailing with attachment will now export the
  active version and email that as an attachments. This mimics more closely
  the existing behavior of this feature before the document version were
  separated into versions and files.
- Update Django version 2.2.23 to 2.2.24.
- Improve Docker Compose installation and upgrade instructions.
- Fix the document type button not appearing. Update the cascade condition
  of the document type setup link to display when there are not document
  types created.
- Don't cache the missing items template to allow it to be removed when
  the missing items are fixed.
- Event testing improvements for several apps.
- The date and time of document version timestamps are now carried over
  during the upgrade from version 3.5.x to 4.0.x.
- Update the file metadata submit actions to keep track of the user and apply
  it to the events.
- Update the document parsing submit actions to keep track of the user and
  apply it to the events.
- Apply small optimization to ``MultipleObjectViewMixin``
  ``.get_object_list()`` method. The method now reuses the existing
  ``pk_list`` variable.
- Fixed an issue with the document metadata add and edit actions which
  prevented the user value to be ignored at the event commit.
- Convert the GitLab CI and Dockerfile into platform templates.
- Update Docker base image from Debian:10.8-slim to Debian:10.10-slim.
- Add config entry ``DEFAULT_USER_SETTINGS_MODULE``.
- Add serializer explicit read only fields.
- Optimize documents app saves with `update_fields`.

4.0.7 (2021-06-11)
==================
- Fix typo in the CELERY_MAX_TASKS_PER_CHILD_ARGUMENT environment
  variable.

4.0.6 (2021-06-10)
==================
- Fix celery argument names in supervisord template. Set correct attribute
  names max-tasks-per-child and max-memory-per-child when starting celery
  workers. Closes #998. Thanks to joh-ku (@joh-ku) for the report and patch.
- Use different environment when composing the child limits arguments.
  Update CELERY_MAX_MEMORY_PER_CHILD and CELERY_TASKS_MEMORY_PER_CHILD
  to use a separate argument variable, like CELERY_CONCURRENCY.

4.0.5 (2021-06-08)
==================
- Turn the release notes upgrade instructions into a partial template.
- Add support for Celery's max memory and tasks. Support
  ``--max-memory-per-child`` and ``--max-tasks-per-child`` using
  the environment variables ``MAYAN_WORKER_X_MAX_MEMORY_PER_CHILD``
  and ``MAYAN_WORKER_X_MAX_TASKS_PER_CHILD``.
- Add commented Docker compose database port entry.
- Support Gunicorn's ``--limit-request-line`` via the
  ``MAYAN_GUNICORN_LIMIT_REQUEST_LINE`` environment variable.
- Improve the Docker image environment variables chapter. Include missing
  variables and automate displaying the default values of several.
  Organize variables by topic.
- Exclude trashed documents from the workflow runtime proxy document count.
- Fix metadata form ``KeyError`` exception when required metadata is missing.
  Closes GitLab issue #997. Thanks to Raimar Sandner (@PiQuer) for the report
  and debug information.
- Document file and version page image updates:

  - Improve document version page base image cache invalidation on source
    image transformation updates.
  - Optimize transformation list generation by replacing several loops with
    list extensions.
  - Avoid using the source content transformations when calculating the
    document version transformation list hash. This cause duplicated document
    version page transformation in some cases. Closes GitLab issue #996.
    Thanks to Reinhard Ernst (@reinhardernst) for the report and debug
    information.
  - Improve document version page image API URL hash uniqueness generation.
    Ensure browsers do not use a cached document version page image when
    the transformations of the source object of the version are updated.

4.0.4 (2021-06-05)
==================
- Merge updates from version 3.5.10

  - Remove event decorator database transaction
    Solves workflows not being launched on document creation. Closes
    GitLab issue #976 and issue #990, thanks to users Megamorf (@megamorf),
    A F (@adzzzz) for the reports and debug information.

4.0.3 (2021-06-03)
==================
- Merge updates from version 3.5.9

  - Fix user model theme related field error after deleting a theme already
    assigned to a user. Closes GitLab issue #972. Thanks to Niklas Maurer
    (@nmaurer) for the report.
  - Add duplicate document tool tests.
  - Speed up some OCR view tests.
  - Add explicit Docker logout repository in CD/CI jobs.
  - Fix permission required for the document content error list link to match
    the permission required for the document parsed content error list view.
    GitLab issue #954. Thanks to Ilya Pavlov (@spirkaa) for the report.
  - Fix permission required for the OCR content delete link to match the
    permission required for the OCR content delete view. GitLab issue #954.
    Thanks to Ilya Pavlov (@spirkaa) for the report.

- Update dependency versions:

  - django-solo from version 1.1.3 to 1.1.5.
  - python-magic from version 0.4.15 to 0.4.22

- Makefile updates

  - Unify Docker test with staging targets.
  - Replace underscore in target names with hyphen for uniformity.
  - Add Redis Docker test targets.

- Lock manager updates

  - Rename get_instance() method to get_backend(). This method
    returns a class and not an instance.
  - Add management command tests.
  - Add optional _initialization method for backends.
  - Update the RedisLock backend to use a connection pool.

- Update Docker entrypoint template to support default worker
  concurrency values. Now correctly passes the default concurrency
  value of the D class worker.
- Updated REST API examples for version 4 of the API.

4.0.2 (2021-05-25)
==================
- Messaging app updates:

    - Add links to set messages as unread.
    - Automatically set messages as read upon accessing them. GitLab issue
      #981, thanks to Ilya Pavlov (@spirkaa) for the report.
    - Disable links to mark messages as read or unread based on the state of
      the message.

- Clarify Redis and Lock manager upgrade steps.
- Action dropdown template updates:

  - Move dropdown template partial to the navigation app.
  - Remove unused {{ link_extra_classes }}.
  - Remove obsolete dropdown HTML markup.

- Fix action menu disabled link appearance.
- Correct user_settings folder creation step. Closes GitLab issue #984.
  Thanks to Matthias Löblich (@startmat) for the report.
- Ensure the API authentication has completed before doing initial filtering.
  Fixes API views returning 404 errors when using token authentication.
- Minor source string fixes.
- Update Django REST framework from version 3.11.0 to 3.11.2.
- Update PIP from version 21.0.1 to 21.1.1.
- Update django-mptt from version 0.11.0 to 0.12.0.
- Add ordering to cabinets. Closes GitLab issue #986. Thanks to Hanno Zulla
  (@hzulla) for the report.

4.0.1 (2021-05-20)
==================
- Fix group and user setup link conditional disable not working as
  expected.
- Fix Docker environment variables documentation chapter regarding
  worker concurrency.
- Add troubleshooting section regarding document file access after upgrade
  to version 4.0.
- Allow migration of the settings ``DOCUMENTS_STORAGE_BACKEND`` and
  ``DOCUMENTS_STORAGE_BACKEND_ARGUMENTS`` for more situations.

4.0 (2021-05-19)
================
- Add document version page list reset.
- Add document version page delete.
- Add document version hash from content object.
- Improve file and version page max page calculation.
- Add version page navigation.
- Support document file deletion.
- Move document download code to document file.
- Add document file permissions.
- Move page count update to document file.
- Several renames for consistency. Use the major, minor, verb order
  for variable names in more places.
- Point document to latest document version. This removes the document page
  views and makes them aliases of the document version pages views.
- Add document version deletion.
- Add document file properties view.
- Remove page disabling/enabling.
- Add document version page model.
- Add caches, settings and handlers for the document version cache.
- Add document version page image API.
- Rename ``DocumentPage`` model to ``DocumentFilePage``.
- Invert the document and OCR migrations dependency. Makes the OCR migration
  dependent on the documents app migration. This allows disabling the OCR app.
- New event ignore and keep attribute options
- No results template for file list view.
- Fixed version page append
- Convert document model save method to use event decorator.
- Update file hooks to work when there is not previous file.
- Remove all remaining orientation support. Remove rotation test files.
- Add multi document version delete.
- Add a generic multi item delete view.
- Longer document file action texts.
- Document stub recalculation by file save and delete
- Better document version page remap
- Reorganize and split document model tests
- Add file upload mixin method.
- Unify the action dropdown instances into a new partial called
  ``appearance/partials/actions_dropdown.html``.
- Move the ``related`` menu from the "Actions" to the ``facet`` area.
- Add sources to their own menu.
- Add ``mode`` argument to SharedUploadedFile.
- Split document app model tests into separate modules.
- Split document app test mixins into separate modules.
- Fix the appearance of the automatically generated view titles.
- Add a new "Return" menu for secondary object views.
- Use the "Return" menu for the document version, document version page,
  document file, and document file page views.
- Remove the "File..." reference to the document file form fields as these
  are now obvious.
- Add more return links. From document version to version list, from
  document file to document file list, from document version page to
  document, from document file page to document.
- Add document version edit view. Allows editing the document version comment.
- Improve the return links with the chevron as the uniform secondary icon.
- Rename the document view, document version view and document file views to
  document preview, document file preview and document version preview.
- Enable more cabinets, checkouts, document comments, metadata, linking,
  mailer, mirroring, web links apps.
- Allow using staging folders for new document file uploads.
- Add conditional source link highlighting.
- Add document version create view and permission.
- Add validation and test for repeated document version page numbers.
- Improve page remap code and add annotated content object list support.
- Don't display the file upload link on the document file delete view.
- Update shared upload file to allow storing the original filename.
- Upload the new document file upload code path to conserve the original
  filename.
- Rename ``DeletedDocument`` to ``TrashedDocument``, same with the
  corresponding trashed fields and manager methods.
- Add document file download event.
- Update Dropzone from version 5.4.0 to 5.7.2.
- Rename all instances of ``icon_class`` to ``icon`` as only icon instances
  are used now in every app.
- Add icons to the mark notification as seen and mark all notification as
  seen links.
- Switch both view to mark notification as read to use the POST request
  via a confirmation view.
- Return the event type subscription list sorted by namespace label and event
  type label.
- Make the search fields more uniform and add missing ones.
- Add full label for search parent fields.
- Add events for the document type quick label model.
- Add dedicated API endpoints for the document type quick label model.
- Update the file cache partition purge view to be a generic view that can
  be called using the content type of an object. Adds a new file cache
  partition purge permission.
- Added ``ContentTypeTestCaseMixin``.
- Include ``EventTestCaseMixin`` as part of the base test case mixin.
- Rename usage of "recent document" to the more explicit "recently
  accessed document". This was done at the mode, view and API level.
  The recently accessed document API will now require the document view
  permission.
- Rename the document model ``date_added`` field to ``datetime_created`` to
  better reflect the purpose of the field.
- Add a ``RecentlyCreatedDocument`` proxy and associate the recent document
  columns to it.
- Move the recently created document query calculation to its own model
  manager.
- Add the recently created document API.
- Add favorite documents API.
- Rename the ``misc_models.py`` module to ``duplicated_document_models.py``.
- Split the ``document_api_views.py`` modules into ``document_api_views.py``
  and ``trashed_document_api_views.py``.
- Add date time field to the favorite documents models to ensure deterministic
  ordering when deleting the oldest favorites.
- Rename the setting ``DOCUMENTS_RECENT_ACCESS_COUNT`` to
  ``DOCUMENTS_RECENTLY_ACCESSED_COUNT``, and ``DOCUMENTS_RECENT_ADDED_COUNT``
  to ``DOCUMENTS_RECENTLY_CREATED_COUNT``. Config file migrations and
  migration tests were added. Environment and supervisor settings need to be
  manually updated.
- Document stubs without a label will now display their ID as the label.
  This allows documents without files or versions to be accessible via the
  user interface.
- Add the reusable ObjectActionAPIView API view. This is a view that can
  execute an action on an object from a queryset from a POST request.
- Improve proxy model menu link resolution. Proxy model don't need at least
  one bound link anymore to trigger resolution of all the parent model links.
  The inclusion logic is now reverse and defaults to exclusion. Menu need to
  be configured explicitly enable to proxy model link resolution using the new
  ``.add_proxy_inclusions(source)`` method.
- Move the duplicated documents code to its own app.
- Add duplication backend support to the duplicates app.
- Add duplicates app API.
- Add support for search model proxy registration.
- Remove the ``views`` arguments from the SourceColumn class. Use models
  proxies instead to customize the columns of a model based on the view
  displayed.
- Add document type change workflow action.
- Rename WizardStep to DocumentCreateWizardStep. This change better reflects
  its purpose and interface.
- Move DocumentCreateWizardStep to the sources.classes module.
- Add automatic loading support for the ``wizard_step`` modules. It is no
  longer necessary to import these modules inside the App's .ready() method.
- Update API endpoints to use explicit primary key URL keyword arguments.
- Split workflow models module into separate modules.
- Remove usage of Document.save(_user). The event_actor attribute is used
  instead.
- Convert the key creation and expiration fields to date and time fields.
- Add creation and download events for keys.
- Add event subscription for keys.
- Include time of document signatures. Closes GitLab issue #941. Thanks
  to forum user Tomek (@tkwoka) for the report and additional
  information.
- Add document signature tool to refresh the content of existing signatures
  when there are database or backend changes.
- Moved ``ObjectLinkWidget`` to the views app.
- Add global ACL list view.
- ``appearance_app_templates`` now passes the request to the templates being
  rendered.
- Remove the user impersonation fragment form the ``base.html`` template and
  moved it to its own viewport template.
- Enable subscribing to user impersonation events.
- Enable impersonation permission for individual users.
- Allow impersonating users from the user list view.
- Update jQuery from version 3.4.1 to 3.5.1.
- Move user language and timezone code from the `common` app to a new app
  called `locales`.
- Move common and smart settings app `base` template markup to their own
  apps via the `viewport` app template.
- Rename document comment model's `comment` field to `text`.
- Support sorting document comments by user or by date.
- Increase the size of the ``Lock`` lock manager model ``name`` field to a
  255 char field. Closes GitLab issue #939. Thanks to Will Wright
  (@fireatwill) for the report and investigation.
- Add example usage for the ``COMMON_EXTRA_APPS`` and
  ``COMMON_DISABLED_APPS``. Closes GitLab issue #929. Thanks to Francesco
  Musella (@francesco.musella-biztems) for the report.
- Reorganize mixins. Add a suffix to specify the purpose of the mixin and
  move them to different module when appropriate.
- Refactored the notification generation for efficiency, scalability and
  simplicity. Only users subscribed to events are queued for notifications.
  Content types of event targets and action objects is reused from the action
  model instead of gathering from inspection. Nested loop removed and lowered
  to a single loop.
- Optimize SourceColumn resolution. Support column exclusion for all object
  types. Ensure columns are not repeated when resolved even if they were
  defined multiple times. Improve docstring for the resolution logic in each
  level. Remove unused ``context`` parameter. Add SourceColumn tests.
- Support defining the default ``SearchModel``. This allows removing the hard
  coded search model name from the search template and allows third party
  apps to define their own default ``SearchModel``.
- Update MySQL Docker image from version 5.7 to 8.0. PostreSQL image from version
  10.14 to 10.15. Redis image from version 5.0 to 6.0.
- Move time delays from test and into its own test mixin. Remove MySQL test delays.
- Standardize a class for the widgets of the class ``SourceColumn`` named
  ``SourceColumnWidget``.
- The cabinet view permission is now required for a document, to be able to
  view which cabinets contain that document. This change mirrors the
  permission layout of the metadata and tag apps.
- File caching now uses the same lock for all file methods. This ensures that
  a cache file that is being deleted or purge is not open for reading and
  vice versa.
- A method decorator was added to the lock manager app to ease usage of the
  same lock workflow in methods of the same class.
- The error handling of the ``CachePartitionFile`` methods was improved.
  This ensures proper clean up of stray storage files on model file creation
  error. The model now avoids accessing the model file for clean up on model
  file creation error, which would raise a hard to understand and diagnose
  missing file entry error. The model now avoids updating cache size on
  either model or storage file creation error.
- Support disabling form help texts via ``form_hide_help_text``.
- Docker image tagging layout has been updated. Images are tagged by version
  and series. Series have the 's' prefix and versions have the 'v' prefix.
- Added API endpoints for the Assets model.
- Added cached image generation for assets.
- Added asset detail view with image preview.
- Added a detail view for the cache model.
- Added the ``image_url`` field to the Workflow template serializer.
- Added retry support for the workflow preview generation task.
- Updated the autoadmin app to use the login template ``login_content``
  template hook. This allows the autoadmin app to show login information
  without directly modifying the login template.
- Update tags app to improve user event tracking on view and API.
- Support deleting multiple document files.
- Track document file deletion event user in views.
- Rename ``setting_workflowimagecache_storage`` to
  ``setting_workflow_image_cache_storage_backend``.
- Support collapsing the options of the menus "list facet" and "object" when
  in list view mode. This behavior is controlled with the new settings:
  ``COMMON_COLLAPSE_LIST_MENU_LIST_FACET`` and
  ``COMMON_COLLAPSE_LIST_MENU_OBJECT``. Both default to ``False``.
- Added a check to the task manager app to ensure all defined tasks are
  properly configure in their respective ``queues.py`` modules.
- ACL apps updates: Add ACL deleted event, track action actor in API and
  views. Simply API views using REST API mixins. Update API views to return
  404 errors instead of 403, move global ACL list to the setup menu,
  model that are registered for ACLs are now also automatically register
  events in order to receive the ACL deleted event, improve tests and add more
  test cases.
- Update AddRemoveView to only call the underlying add or remove methods only
  if there are objects to act upon instead of calling the method with an
  empty queryset which would trigger unwanted events.
- Add ``ExternalContentTypeObjectAPIViewMixin`` to the REST API app. This
  mixin simplifies working with models that act upon another object via
  their Content Type, such as the ACLs.
- Update the ACL app to support multiple foreign object permission
  inheritance. Support for ``GenericForeignKey`` non default ``ct_field``,
  and ``fk_field`` was also added.
- Added support to export the global events list, object events list and
  user events list.
- Registering a model to receive events will cause it to have the object
  event view and object event subscription links bound too. This can
  be disabled with the `bind_links` argument. The default menu to bind the
  links is the "List facet". This can be changed via the ``menu`` argument.
- Change the format of the ``file_metadata_value_of`` helper. The driver
  and metadata entry are now separated by a double underscore instead of a
  single underscore. This allows supporting drivers and entries that might
  contain an underscore themselves.
- Add ``databases`` app to group data and models related code.
- Add class support for scoped searches. GitLab issue #875.
- Add sorting support to the API.
- Updated how the user interface column sorting works. The code was
  simplified by using a single query variable. The code was expanded
  to support multiple fields in the future. The URL query key used for
  column sorting was changed to match the API sorting.a
- Added the ``databases`` app. This app groups data and models related code.
- Added a patch for Django's ``Migration`` class to display time delta for
  each migration during development.
- Docker Compose updates:

    - Use profiles for extra containers.
    - Converted to use extensions to remove duplicated markup.
    - A new container was added to mount an index.
    - Added support for Traefik.
    - Added sample .env file.
    - Update required Docker Compose to version 1.28.

- Add a third document filename generator that used an UUID plus the original
  filename of the uploaded file. This generator has the advantage of producing
  unique filename while also preserving the original filename for reference.
- Add support for the "Reply To" field for sending documents via email and
  for the mailing workflow actions. Closes GitLab issue #864. Thanks to
  Kevin Pawsey (@kevinpawsey) for the request.
- Allow customization of the error condition when generating document images.
  This allows displaying more icons in addition to the generic document
  image error with additional contextual information and popup messages
  explaining the actual error condition.
- Add key attributes to the document signature serializers. Forum topic 5085.
  Thanks to forum user @qra for the request.
- Added key attributes to the document signature model as calculated
  properties.
- Move detached signature upload from the created endpoint to a
  new /uploaded endpoint.
- Added document signature events.
- Refactored the workflows app.

    - Rebalance permissions needed to transition a workflow instance.
      The workflow instance transition permission is now needed for
      the document and for either the transition or the workflow.
    - Add more tests including trashed document tests.
    - Split API tests into instance and template tests.
    - Add `workflow-instance-log-entry-detail` end point.
    - Add parent URL fields to serializers.
    - Allow passing extra data when transitioning a workflow via the API.
    - Limit state options to workflow when using the API. This matches
      the UI behavior.

- Renamed the AddRemove view ``main_object_method_add`` to
  ``main_object_method_add_name`` and ``main_object_method_remove`` to
  ``main_object_method_add_remove_name``.
- Add ``has_translations`` flag to MayanAppConfig to indicate if the app
  should have its translation files processed or ignored. Defaults to
  ``True``.
- Dependency version upgrades:

  - coverage from 5.1 to 5.5.
  - Django to 2.2.23.
  - django-debug-toolbar to 3.2.
  - django-extensions to 3.1.2.
  - django-rosetta to 0.9.4.
  - django-silk to 4.1.0.
  - flake8 to 3.9.0.
  - ipython to 7.22.0.
  - pycounty to 20.7.3.
  - requests to 2.25.1.
  - Sphinx to 3.5.4.
  - sh to 1.14.1.
  - sphinx-autobuild to 2021.3.14.
  - sphinx-sitemap to 2.2.0.
  - sphinxcontrib-spelling to 7.1.0.
  - tornado to 6.1.
  - tox from 3.14.6 to 3.23.1.
  - transifex-client to 0.14.2.
  - twine to 3.4.1.
  - wheel to 0.36.2.

- Fix sub workflow launch state action.
- Convert the workflow instance creation to a background task.
- File caching app updates

  - Add cache partition purge event.
  - Use new event decorator.
  - Use related object as the cache partition purge event action object.
  - Allow cache prune to retry on LockError.
  - Add maximum cache prune failure counter.
  - Remove possible cache file lock name collision.

- Add locking to the duplicated document scan code to workaround race
  condition in Django bug #19544 when adding duplicated documents via
  the many to many field ``.add()`` method.
- Remove the default queue. All tasks must now be explicitly assigned to an
  app defined queue.
- Update file cache to use and LRU style eviction logic.
- Only prune caches during startup if their maximum size changed.
- Add detection of excessive cache pruning when cache size is too small for
  the workload.
- Detect and avoid duplicated queue names.
- Add a fourth class of worker.
- Re-balance queues.
- Rename workers from ``fast``, ``medium``, and ``slow`` to ``A`` (fast),
  ``B`` (new workers), ``C`` (medium), ``D`` (slow).
- Add support for passing custom nice level to the workers when using the
  Docker image ``run_worker`` command. The value is passed via the
  ``MAYAN_WORKER_NICE_LEVEL`` environment variable. This variable defaults to
  ``0``.
- Avoid adding a transformation to a layer for which it was
  not registered.
- Add LayerError exception.
- Fix redaction ACL support.
- Add support for typecasting the values used to filter the ACL object
  inherited fields.
- Rename the ``mayan_settings`` directory, which is used to allow custom
  setting modules, to the more intuitive ``user_settings``.
