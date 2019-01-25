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
        return_date_info = "UDW Data Last Updated: " + c.load_dt.strftime("%Y-%m-%d %H:%M:%S") + "; Schema: " + c.dw_ownr_nm
        return return_date_info
    except LearningAnalyticsStats.DoesNotExist:
        return datetime.min.strftime("%Y-%m-%d %H:%M:%S")