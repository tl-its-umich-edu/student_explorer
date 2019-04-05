from djangosaml2.backends import Saml2Backend
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
import logging

logger = logging.getLogger(__name__)


class ActiveUserOnlySAML2Backend(Saml2Backend):
    def authenticate(self, **kwargs):
        user = super(ActiveUserOnlySAML2Backend, self).authenticate(**kwargs)
        if user.is_active:
           return user
        else:
            logger.error(
                'The user "%s" exists but is set inactive', user.username)
            raise PermissionDenied
