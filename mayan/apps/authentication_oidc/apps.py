from django.conf import settings
from django.utils.translation import gettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import menu_user

from .links import link_current_user_oidc_details, separator_oidc_user


class AuthenticationOIDCApp(MayanAppConfig):
    app_namespace = 'authentication_oidc'
    app_url = ''
    has_rest_api = False
    has_static_media = True
    has_tests = False
    name = 'mayan.apps.authentication_oidc'
    verbose_name = _(message='Authentication OIDC')

    def ready(self):
        super().ready()

        settings.STRONGHOLD_PUBLIC_URLS += (r'^/oidc.*',)

        menu_user.bind_links(
            links=(
                separator_oidc_user, link_current_user_oidc_details
            )
        )
