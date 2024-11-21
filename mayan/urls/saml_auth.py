from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, logout
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from django.conf import settings
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from stronghold.decorators import public
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import login, get_user_model, authenticate




@public
def init_saml_auth(request):
    request_data = {
        'https': 'on' if request.is_secure() else 'off',
        'http_host': request.get_host(),
        'script_name': request.path,
        'get_data': request.GET.copy(),
        'post_data': request.POST.copy()
    }
    print("request_data :", request_data)
    auth = OneLogin_Saml2_Auth(request_data, settings.SAML_CONFIG)
    return auth

@public
def saml_login(request):
    auth = init_saml_auth(request)
    print(" SAML Login auth data :" , auth ,auth.login())

    return HttpResponseRedirect(auth.login())


@public
@csrf_exempt
def saml_acs(request):
    auth = init_saml_auth(request)
    auth.process_response()

    errors = auth.get_errors()
    if not errors and auth.is_authenticated():
        attributes = auth.get_attributes()

        # Assuming SAML response includes these attributes
        email = attributes.get('http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress', [None])[0]
        username = attributes.get('http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name', [None])[0]
        first_name = attributes.get('http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname', [None])[0]
        last_name = attributes.get('http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname', [None])[0]

        if not email or not username:
            return HttpResponse("Error: Essential user information missing.", status=400)

        User = get_user_model()
        user, created = User.objects.get_or_create(email=email, defaults={
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
        })

        if created:
            print("User Created:", user.email, user.username)

        # Authenticate the user manually
        user.backend = 'django.contrib.auth.backends.ModelBackend'  # Specify the backend
        login(request, user)  # Log in the user

        print("User authenticated and logged in.")
        return HttpResponseRedirect(reverse('verified_files'))

    return HttpResponseRedirect(reverse('saml_login'))


@public
def saml_logout(request):
    auth = init_saml_auth(request)
    logout(request)
    return HttpResponseRedirect(auth.logout())

@public
def home_view(request):
    print("in home : ",  request.user.is_authenticated )

    if request.user.is_authenticated:
        context = {
            'username': request.user.username,
            'email': request.user.email
        }
        print(context)
    else:
        context = {
            'message': 'User is not logged in'
        }
    return render(request, 'home.html', context)
