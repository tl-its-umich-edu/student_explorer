from django.shortcuts import render, redirect
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve
from django.views.static import serve
import logging

logger = logging.getLogger(__name__)


def redirect_or_serve(request, path, document_root):
    if not hasattr(settings, 'REDIRECT_LOGIN_URL'):
        raise ImproperlyConfigured('REDIRECT_LOGIN_URL is missing.')

    current_url = resolve(request.path_info).url_name

    base_url = request.build_absolute_uri(reverse(current_url))
    logger.debug('base_url = %s' % base_url)

    if request.user.is_authenticated():
        logger.debug('User is authenticated')
        if 'hash_frament' in request.GET:
            logger.debug('URL has hash_frament parameter')
            hash_fragment = request.GET.get('hash_fragment')

            return redirect('%s#%s' % (base_url, hash_fragment))
        else:
            logger.debug('URL does not have hash_frament parameter')
            return serve(request, path=path, document_root=document_root)
    context = {
        'login_url': settings.REDIRECT_LOGIN_URL + base_url,
    }

    logger.debug('User is not authenticated')
    return render(request, 'hashredirect/login.html', context)
