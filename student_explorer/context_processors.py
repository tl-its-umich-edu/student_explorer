from student_explorer.common import db_util
import logging

logger = logging.getLogger(__name__)

def last_updated(request):
    results = db_util.get_data_date()

    return {'data_time': results.get("data_time"),
            'data_schema': results.get("data_schema")}
