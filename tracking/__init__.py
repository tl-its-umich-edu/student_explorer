import sys

from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out

from tracking.eventnames import EventNames

def _get_user(kwargs):
    user = kwargs.get('user')
    if user is None:
        user = getattr(kwargs.get('request'), 'user', None)
    return user

@receiver(user_logged_in)
def user_logged_in_callback(sender, **kwargs):
    from tracking.utils import create_event
    user = _get_user(kwargs)
    if user is not None:
        create_event(EventNames.UserLoggedIn, user=user,
            request=kwargs.get('request'))

@receiver(user_logged_out)
def user_logged_out_callback(sender, **kwargs):
    from tracking.utils import create_event
    user = _get_user(kwargs)
    if user is not None:
        create_event(EventNames.UserLoggedOut, user=user,
            request=kwargs.get('request'))
