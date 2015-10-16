from django.shortcuts import render, redirect
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.http import HttpResponse


def login(request):
    if not hasattr(settings, 'REDIRECT_LOGIN_URL'):
        raise ImproperlyConfigured('REDIRECT_LOGIN_URL is missing.')

    base_url = request.build_absolute_uri(reverse('login-redirect'))

    if request.user.is_authenticated():
        print 'User is authenticated'
        hash_fragment = request.GET.get('hash_fragment', False)
        if hash_fragment:
            print 'URL has hash_frament parameter'
            return redirect('%s#%s' % (base_url, hash_fragment))
            # return HttpResponse('Redirecting to %s#%s' % (base_url, hash_fragment))

        else:
            print 'URL does not have hash_frament parameter'
            return HttpResponse('You\'re logged in. <a href="http://localhost:2080/api/api-auth/logout/?next=/login/">logout</a>.')
    context = {
        'login_url': settings.REDIRECT_LOGIN_URL + base_url,
    }

    return render(request, 'redirect/login.html', context)
