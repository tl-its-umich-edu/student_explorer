from django.shortcuts import render, redirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.static import serve
import logging

logger = logging.getLogger(__name__)


def login_or_serve(request, path, document_root):
    if (not hasattr(settings, 'HASHREDIRECT_LOGIN_URL') or
            len(settings.HASHREDIRECT_LOGIN_URL) < 1):
        logger.info(('HASHREDIRECT_LOGIN_URL is missing. Serving content '
                     'without redirecting for login.'))
        return serve(request, path=path, document_root=document_root)

    if request.user.is_authenticated():
        logger.debug('User is authenticated')
        return serve(request, path=path, document_root=document_root)
    else:
        redirect_url = reverse('hashredirect-login-redirect')

        logger.debug('redirect_url = %s' % redirect_url)

        context = {
            'login_url': redirect_url,
        }

        logger.debug('User is not authenticated')
        return render(request, 'hashredirect/login_redirect.html', context)


@login_required
def login_redirect(request):
    if request.user.is_authenticated():
        logger.debug('User is authenticated')

        hash_fragment = request.GET.get('hash_fragment', False)
        base_url = reverse('app-root')

        if hash_fragment:
            logger.debug('URL has hash_frament parameter')
            return redirect('%s#%s' % (base_url, hash_fragment))
        else:
            logger.debug('URL does not have hash_frament parameter')
            return redirect(base_url)
