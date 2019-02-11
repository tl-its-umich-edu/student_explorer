# Some utility functions used by other classes in this project

import django
import logging
from datetime import datetime
from dateutil.parser import parse
from seumich.models import (LearningAnalyticsStats,)

logger = logging.getLogger(__name__)

def get_data_date():
    try:
        c = LearningAnalyticsStats.objects.get(dw_data_nm='UDW Daily Tables')
        return {'data_time': c.load_dt,
                'data_schema': c.dw_ownr_nm}
    except LearningAnalyticsStats.DoesNotExist:
        return {'data_time': datetime.min,
            'data_schema': 'N/A'}
    