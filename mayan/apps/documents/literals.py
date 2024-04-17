import os

from django.conf import settings
from django.utils.translation import gettext_lazy as _

from mayan.apps.common.literals import TIME_DELTA_UNIT_DAYS

CHECK_DELETE_PERIOD_INTERVAL = 60
CHECK_TRASH_PERIOD_INTERVAL = 60

DEFAULT_DELETE_PERIOD = 30
DEFAULT_DELETE_TIME_UNIT = TIME_DELTA_UNIT_DAYS
DEFAULT_DOCUMENT_FILE_ACTION_NAME = 'replace'
DEFAULT_DOCUMENT_TYPE_LABEL = _(message='Default')

# Old defaults (<4.0), used for the setting migrations.
DEFAULT_DOCUMENTS_STORAGE_BACKEND = 'django.core.files.storage.FileSystemStorage'
DEFAULT_DOCUMENTS_STORAGE_BACKEND_ARGUMENTS = {
    'location': os.path.join(settings.MEDIA_ROOT, 'document_storage')
}

DEFAULT_DOCUMENTS_DISPLAY_HEIGHT = ''
DEFAULT_DOCUMENTS_DISPLAY_WIDTH = '3600'
DEFAULT_DOCUMENTS_FAVORITE_COUNT = 400
DEFAULT_DOCUMENTS_FILE_PAGE_IMAGE_CACHE_MAXIMUM_SIZE = 500 * 2 ** 20  # 500 Megabytes
DEFAULT_DOCUMENTS_FILE_STORAGE_BACKEND = 'django.core.files.storage.FileSystemStorage'
DEFAULT_DOCUMENTS_FILE_STORAGE_BACKEND_ARGUMENTS = {
    'location': os.path.join(settings.MEDIA_ROOT, 'document_file_storage')
}
DEFAULT_DOCUMENTS_FILE_PAGE_IMAGE_CACHE_STORAGE_BACKEND = 'django.core.files.storage.FileSystemStorage'
DEFAULT_DOCUMENTS_FILE_PAGE_IMAGE_CACHE_STORAGE_BACKEND_ARGUMENTS = {
    'location': os.path.join(
        settings.MEDIA_ROOT, 'document_file_page_image_cache'
    )
}
DEFAULT_DOCUMENTS_HASH_BLOCK_SIZE = 65535
DEFAULT_DOCUMENTS_LIST_THUMBNAIL_WIDTH = '50'
DEFAULT_DOCUMENTS_PREVIEW_HEIGHT = ''
DEFAULT_DOCUMENTS_PREVIEW_WIDTH = '1600'
DEFAULT_DOCUMENTS_PRINT_HEIGHT = ''
DEFAULT_DOCUMENTS_PRINT_WIDTH = '3600'
DEFAULT_DOCUMENTS_RECENTLY_ACCESSED_COUNT = 400
DEFAULT_DOCUMENTS_RECENTLY_CREATED_COUNT = 400
DEFAULT_DOCUMENTS_ROTATION_STEP = 90
DEFAULT_DOCUMENTS_THUMBNAIL_HEIGHT = ''
DEFAULT_DOCUMENTS_THUMBNAIL_WIDTH = '800'
DEFAULT_DOCUMENTS_VERSION_PAGE_IMAGE_CACHE_MAXIMUM_SIZE = 500 * 2 ** 20  # 500 Megabytes
DEFAULT_DOCUMENTS_VERSION_PAGE_IMAGE_CACHE_STORAGE_BACKEND = 'django.core.files.storage.FileSystemStorage'
DEFAULT_DOCUMENTS_VERSION_PAGE_IMAGE_CACHE_STORAGE_BACKEND_ARGUMENTS = {
    'location': os.path.join(
        settings.MEDIA_ROOT, 'document_version_page_image_cache'
    )
}

DEFAULT_DOCUMENTS_ZOOM_MAX_LEVEL = 300
DEFAULT_DOCUMENTS_ZOOM_MIN_LEVEL = 25
DEFAULT_DOCUMENTS_ZOOM_PERCENT_STEP = 25
DEFAULT_LANGUAGE = 'eng'
DEFAULT_LANGUAGE_CODES = (
    'ilo', 'run', 'uig', 'hin', 'pan', 'pnb', 'wuu', 'msa', 'kxd', 'ind',
    'zsm', 'jax', 'meo', 'kvr', 'xmm', 'min', 'mui', 'zmi', 'max', 'mfa',
    'cjy', 'nan', 'pus', 'pbu', 'pbt', 'wne', 'hsn', 'hak', 'ful', 'fuc',
    'fuf', 'ffm', 'fue', 'fuh', 'fuq', 'fuv', 'fub', 'fui', 'nep', 'npi',
    'dty', 'sin', 'khm', 'kxm', 'ell', 'grc', 'cpg', 'gmy', 'pnt', 'tsd',
    'yej', 'nya', 'mnp', 'dhd', 'cdo', 'hil', 'bcc', 'bgn', 'bgp', 'cmn',
    'kok', 'spa', 'eng', 'ara', 'por', 'ben', 'rus', 'jpn', 'deu', 'jav',
    'tel', 'vie', 'kor', 'fra', 'mar', 'tam', 'urd', 'tur', 'ita', 'yue',
    'tha', 'guj', 'fas', 'pol', 'kan', 'mal', 'sun', 'hau', 'ory', 'mya',
    'ukr', 'bho', 'tgl', 'yor', 'mai', 'uzb', 'snd', 'amh', 'ron', 'orm',
    'ibo', 'aze', 'awa', 'gan', 'ceb', 'nld', 'kur', 'hbs', 'mlg', 'skr',
    'ctg', 'zha', 'tuk', 'asm', 'mad', 'som', 'mwr', 'mag', 'bgc', 'hun',
    'hne', 'dcc', 'aka', 'kaz', 'syl', 'zul', 'ces', 'kin', 'hat', 'que',
    'swe', 'hmn', 'sna', 'mos', 'xho', 'bel', 'heb'
)
DEFAULT_DOCUMENT_STUB_EXPIRATION_INTERVAL = 60 * 60 * 24  # 24 hours

DOCUMENT_FILE_PAGE_CREATE_BATCH_SIZE = 100
DOCUMENT_VERSION_PAGE_CREATE_BATCH_SIZE = 100

IMAGE_ERROR_NO_ACTIVE_VERSION = 'document_no_active_version'
IMAGE_ERROR_NO_VERSION_PAGES = 'document_no_version_pages'
IMAGE_ERROR_FILE_PAGE_TRANSFORMATION_ERROR = 'document_file_page_transformation_error'
IMAGE_ERROR_VERSION_PAGE_TRANSFORMATION_ERROR = 'document_version_page_transformation_error'

INTERVAL_TASK_STUBS_DELETION = 60 * 10  # 10 minutes

MONTH_NAMES = (
    _(message='January'), _(message='February'), _(message='March'), _(message='April'), _(message='May'),
    _(message='June'), _(message='July'), _(message='August'), _(message='September'), _(message='October'),
    _(message='November'), _(message='December')
)

PAGE_RANGE_ALL = 'all'
PAGE_RANGE_RANGE = 'range'
PAGE_RANGE_CHOICES = (
    (PAGE_RANGE_ALL, _(message='All pages')), (PAGE_RANGE_RANGE, _(message='Page range'))
)

STORAGE_NAME_DOCUMENT_FILE_PAGE_IMAGE_CACHE = 'documents__documentfilepageimagecache'
STORAGE_NAME_DOCUMENT_FILES = 'documents__documentfiles'
STORAGE_NAME_DOCUMENT_VERSION_PAGE_IMAGE_CACHE = 'documents__documentversionpageimagecache'
