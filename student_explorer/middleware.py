from datetime import datetime
import logging
from django.http import HttpResponseNotAllowed
from django.template.loader import render_to_string

logger = logging.getLogger('access_logs')


class LoggingMiddleware(object):
    def process_response(self, request, response):
        l = []

        l.append(request.META.get(
            'HTTP_X_FORWARDED_FOR',
            request.META.get('REMOTE_ADDR', '-')
            )
        )

        if hasattr(request, 'user') and request.user.is_authenticated():
            l.append(request.user.username)
        else:
            l.append('-')

        l.append(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))

        l.append('"' + request.META.get('REQUEST_METHOD', '-') + ' ' +
                 request.get_full_path() + '"')

        l.append(str(response.status_code))

        l.append('"' + request.META.get('HTTP_REFERER', '-') + '"')

        l.append('"' + request.META.get('HTTP_USER_AGENT', '-') + '"')

        logger.info(' '.join(l))
        return response

class HttpResourceNotAllowedMiddleware(object):
    def process_response(self, request, response):
        if isinstance(response, HttpResponseNotAllowed):
            response.content = render_to_string("405.html")
        return response