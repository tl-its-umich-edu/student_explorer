from functools import wraps

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model
from django.utils.decorators import available_attrs
from django.http import HttpResponseBadRequest, HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

from tracking.models import Event, event_logged
from tracking.eventnames import EventNames

def create_event(name, request=None, user=None, note=None, related_object=None):
    """Make an event record for a given set of parameters. If request is
    given, the user is pulled from the request, and in the absence of a note,
    the note is set to the request path."""
    if request is not None:        
        if user is None and hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user
        if note is None:
            note = request.path
    e = Event(name=name)
    if user is not None and user.is_authenticated:
        e.user = user
    if related_object is not None:
        e.related_object = related_object
    if note is not None:
        e.note = note
    # the following attribute is not stored in the database, but it's useful
    # for the logger function in tracking.models.
    e.request = request
    e.save()
    return e


def user_log_page_view(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        user = request.user if request.user.is_authenticated else None
        response = f(request, *args, **kwargs)
        if response.status_code != 200:
            if response.status_code == 302:
                create_event(EventNames.Redirected, request, user=user,
                             note='From: %s \tTo: %s' % (request.path, response['Location']))
            else:
                create_event(EventNames.PageError, request, user=user,
                             note='\n'.join([request.path, 'Response Code: %d' % response.status_code,]))
        else:
            create_event(EventNames.PageViewed, request, user=user)
        return response
    return wrapper

class UserLogPageViewMixin(object):
    """A simple mix-in class to write an event on every request to the view.
    events are written using the `user_log_page_view` decorator.
    """
    @method_decorator(user_log_page_view)
    def dispatch(self, request, *args, **kwargs):
        return super(UserLogPageViewMixin, self).dispatch(request, *args, **kwargs)
    
class LogEventTypeMixin(object):
    eventname = None

    def log_event(self, note=None):
        create_event(name=self.eventname, request=self.request, 
                     user=self.request.user, note=note)