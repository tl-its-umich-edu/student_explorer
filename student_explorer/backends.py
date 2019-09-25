from djangosaml2.backends import Saml2Backend
from django.core.exceptions import PermissionDenied

import logging

logger = logging.getLogger(__name__)


class ActiveUserOnlySAML2Backend(Saml2Backend):
    def authenticate(self, **kwargs):
        user = None
        try:
            user = super(ActiveUserOnlySAML2Backend, self).authenticate(**kwargs)
        except Exception:
            # If there's any exception with this authenticate just return PermisisonDenied
            logger.exception("Exception thrown from authenticate")
            raise PermissionDenied
        # If the user returned is None then we should also give raise PermissionDenied
        if not user:
            raise PermissionDenied
        # The user should be made active if they exist and aren't active
        if not user.is_active:
           user.is_active = True
           user.save()
        return user
            

    def is_authorized(self, attributes, attribute_mapping):
        # If there are any groups that we're a member of, return true
        # These groups are controlled via request to Shibboleth team INC1715416
        if attributes.get('isMemberOf'):
            logger.debug(attributes.get('isMemberOf'))
            return True
        else:
            logger.warn('The user "%s" is not in one of the allowed groups', attributes.get('uid'))
            return False 
