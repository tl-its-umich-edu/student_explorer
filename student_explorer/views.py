from django.contrib import auth
from django.shortcuts import redirect
from django.conf import settings

import logging

logger = logging.getLogger(__name__)


def logout(request):
    logger.info('User %s logging out.' % request.user.username)
    auth.logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)
