from django.shortcuts import render
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
import json


def login(request):
    if not hasattr(settings, 'REDIRECT_LOGIN_URL'):
        raise ImproperlyConfigured('REDIRECT_LOGIN_URL is missing.')

    login_url = (settings.REDIRECT_LOGIN_URL + 
                 request.build_absolute_uri(reverse('login-redirect')))
    config = {
        'redirect': bool(request.GET.get('redirect', False)),
        'loginUrl': login_url,
    }
    
    context = {'config': json.dumps(config)}
    return render(request, 'redirect/login.html', context)
