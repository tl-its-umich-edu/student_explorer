from django.contrib import auth
from django.shortcuts import redirect, render
from django.conf import settings
import os
import logging

logger = logging.getLogger(__name__)


def logout(request):
    logger.info('User %s logging out.' % request.user.username)
    auth.logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


def about(request):
    context = {'build_name': os.getenv('OPENSHIFT_BUILD_NAME'),
                'build_commit': os.getenv('OPENSHIFT_BUILD_COMMIT'),
                'build_reference': os.getenv('OPENSHIFT_BUILD_REFERENCE')}
    return render(request, 'student_explorer/about.html', context)
