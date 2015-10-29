from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404

import logging

logger = logging.getLogger(__name__)


class MultipleFieldLookupMixin(object):
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_params` attribute, instead of the default single field
    filtering.
    """
    def get_queryset(self):
        queryset = self.queryset

        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()

        # apply filters from backends
        queryset = self.filter_queryset(queryset)

        filter_kwargs = {}
        for lookup_field, url_field in self.lookup_params.iteritems():
            filter_kwargs[lookup_field] = self.kwargs[url_field]

        return queryset.filter(**filter_kwargs)

    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        return get_object_or_404(queryset)  # Lookup the object
