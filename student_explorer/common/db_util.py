# Some utility functions used by other classes in this project

import django
import logging
from datetime import datetime
from dateutil.parser import parse

from seumich.models import (LearningAnalyticsStats,)

logger = logging.getLogger(__name__)

def get_data_date():

    try:
        c = LearningAnalyticsStats.objects.filter(dw_data_nm='Student Explorer Daily Tables')
        logger.info(c)
        return c.load_dt
    except LearningAnalyticsStats.DoesNotExist:
        return datetime.min