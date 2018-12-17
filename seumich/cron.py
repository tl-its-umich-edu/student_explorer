# -*- coding: future_fstrings -*-

from __future__ import print_function #python 3 support

from django.db import connections as conns

import logging, datetime

from django.conf import settings

from django_cron import CronJobBase, Schedule

from umich_api.api_utils import ApiUtil

from seumich.models import Mentor

logger = logging.getLogger(__name__)

# cron job to populate course and user tables
class StudentExplorerCronJob(CronJobBase):

    schedule = Schedule(run_at_times=settings.RUN_AT_TIMES)
    code = 'student_explorer.DashboardCronJob'    # a unique code

    def update_advisors_in_canvas_sites(self):
        """This process is intended to
            Iterate through advisor candidate list
            Verifies that advisor has been added to his/her student Canvas sites as observer role
            If not, add the advisor to Canvas site as observer
            Will use the ApiUtil to verify the status
        """

        # Get all of the advisors
        for mentor in Mentor.objects.all():
            for student in mentor.students.all():
                logger.info(student)

    def do(self):
        logger.info("************ Student Explorer cron tab")

        status = ""

        status += "Start cron at: " +  str(datetime.datetime.now()) + "\n"
        self.update_advisors_in_canvas_sites()

        status += "End cron at: " +  str(datetime.datetime.now()) + "\n"

        logger.info("************ total status=" + status + "/n/n")

        return status