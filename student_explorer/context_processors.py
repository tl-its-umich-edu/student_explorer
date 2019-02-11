from student_explorer.common import db_util
import logging
from datetime import datetime
import pytz

logger = logging.getLogger(__name__)

def last_updated(request):
    est = pytz.timezone('US/Eastern')
    utc = pytz.utc
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'

    results = db_util.get_data_date()
    data_time = results.get("data_time")
    data_time.replace(tzinfo=utc)

    data_schema = results.get("data_schema")

    return {'last_updated_1': "Data last updated from Canvas: " + data_time.astimezone(est).strftime(fmt),
            'last_updated_2': "(UDW: " + data_time.replace(microsecond=0).isoformat() + "; Schema: " + data_schema + ")"}