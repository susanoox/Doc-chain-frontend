from django.urls import include, path, re_path

from .views import MayanOIDCAuthenticationCallbackView

passthru_urlpatterns = [
    re_path(
        r'^oidc/', include('mozilla_django_oidc.urls')
    )
]

urlpatterns = [
    # Directly override oidc/callback as ``OIDC_CALLBACK_CLASS`` is read
    # before the app loads therefore setting it in the .ready() method has
    # no effect.
    path(
        'oidc/callback/', MayanOIDCAuthenticationCallbackView.as_view(),
        name='oidc_authentication_callback'
    )
]
