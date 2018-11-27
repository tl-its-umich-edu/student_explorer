from student_explorer.common import db_util
import logging

logger = logging.getLogger(__name__)

def last_updated(request):
    return {'last_updated': db_util.get_data_date()}