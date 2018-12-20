# -*- coding: future_fstrings -*-

from __future__ import print_function #python 3 support

from django.db import connections as conns

import logging, datetime, json

from django.conf import settings

from django_cron import CronJobBase, Schedule

from umich_api.api_utils import ApiUtil

from seumich.models import Mentor

import dateutil.parser as parser

from decouple import config


logger = logging.getLogger(__name__)

# use ApiUtil for all API directory calls
apiUtil = ApiUtil(config("APIUTIL_URL", default=""), config("APIUTIL_KEY", default=""), config("APIUTIL_SECRET", default=""))


# cron job to populate course and user tables
class StudentExplorerCronJob(CronJobBase):

    schedule = Schedule(run_at_times=settings.RUN_AT_TIMES)
    code = 'student_explorer.StudentExplorerCronJob'    # a unique code

    def get_mentor_canvas_id(self, mentor_uniqname):
        """
        This process gets the canvas user id for mentor
        :param mentor_uniqname:
        :return:
        """
        mentor_result = apiUtil.api_call(f"aa/CanvasReadOnly/users/sis_login_id:{mentor_uniqname}/profile", "canvasreadonly")
        mentor_json = json.loads(mentor_result.text)
        return mentor_json.get("id", "")

    def mentor_in_athletic(self, mentor_uniqname):
        """
        checks whether the mentor is in athletic department
        :param mentor_uniqname:
        :return:
        """
        in_athletic = False

        logger.info("mentor uniquename=" + mentor_uniqname)
        resp = apiUtil.api_call(f"MCommunity/People/{mentor_uniqname}", "mcommunity")
        person_json = json.loads(resp.text)
        if (person_json.get("httpCode", "") =="401"):
            # if unauthorized, respose text will be:
            # { "httpCode":"401", "httpMessage":"Unauthorized", "moreInformation":"Client id not registered." }
            logger.warn(f"Not authorized to call MCommunity API")
        elif (person_json.get("person", "").get("errors") !=""):
            # cannot find user
            logger.warn(f"Cannot find user {mentor_uniqname} in MCommunity")
        else:
            advisor_json = json.loads(resp.text)
            affiliation = advisor_json.get("person").get("affiliation", "")
            # array of affiliated department.
            # The advisors of those department will be added as observers to student's Canvas courses
            affiliated_depts = ["Athletics - Faculty and Staff"]
            for dept in affiliated_depts:
                if dept in affiliation:
                    # advisor with right dept affiliation
                    in_athletic = True

        return in_athletic

    def add_user_as_observer_to_course(self, class_site_id, mentor_canvas_user_id):
        """
        check whether the mentor is enrolled in this Canvas course
        if enrolled, do nothing;
        else add the mentor user to the Canvas course with Observer role
        :param class_site_id:
        :param mentor_canvas_user_id:
        :return:
        """
        enrolled = False
        enrollments_resp = apiUtil.api_call(f"aa/CanvasReadOnly/courses/{class_site_id}/enrollments", "canvasreadonly")
        if (enrollments_resp.text.find("errors") != -1):
            # check for error message
            # {"errors":[{"message":"The specified resource does not exist."}],"error_report_id":7008726002}
            logger.warn(f"errors retrieving enrollments for class {class_site_id}: {enrollments_resp.text}")
        else:
            enrollments_json = json.loads(enrollments_resp.text)
            for item in enrollments_json:
                user_id=item.get("user_id")

                if user_id == mentor_canvas_user_id:
                    # advisor is enrolled in the course
                    # break and do nothing
                    enrolled = True
                    break

            if not enrolled:
                logger.info(f"Start: User id {mentor_canvas_user_id} is NOT enrolled in course {class_site_id}. Preparing to add user with Observer role. ")
                # add user as observer role to the Canvas course site
                payload_dictionary = {
                    "enrollment[user_id]": mentor_canvas_user_id,
                    "enrollment[type]": "ObserverEnrollment",
                    "enrollment[enrollment_state]": "active",
                    "enrollment[course_section_id]": class_site_id,
                    "enrollment[limit_privileges_to_course_section]": "true",
                    "enrollment[notify]": "true"
                }
                # POST call to add user
                post_result = apiUtil.api_call(f"aa/CanvasReadOnly/courses/{class_site_id}/enrollments", "canvasreadonly", method="POST", payload=payload_dictionary)
                logger.info(f"End: result of adding user id {mentor_canvas_user_id} to course {class_site_id}: {post_result}")

    def iterate_all_student_for_mentor(self, student_list, mentor_canvas_user_id ):
        """
        This process is loops through all students associated with the mentor
        :param student_list:
        :param mentor_canvas_user_id:
        :return:
        """
        # all students associated with the mentor
        for student in student_list:
            uniqname = student.username
            logger.info(uniqname)

            # all current class for given user
            class_sites = student.studentclasssitestatus_set.all()
            for element in class_sites:
                class_site_id = element.class_site.code
                logger.info(f"class site id {class_site_id} {element.class_site}")

                # if needed, add mentor as Observer to Canvas course site
                self.add_user_as_observer_to_course(class_site_id, mentor_canvas_user_id)

    def update_advisors_in_canvas_sites(self):
        """
        This process is intended to
        Iterate through advisor candidate list
        Verifies that advisor has been added to his/her student Canvas sites as observer role
        If not, add the advisor to Canvas site as observer
        Will use the ApiUtil to verify the status
        :return:
        """
        # Get all of the advisors
        for mentor in Mentor.objects.all():
            mentor_uniqname = mentor.username

            # this is mentor in athletic department
            if (self.mentor_in_athletic(mentor_uniqname)):

                # iterator through all users for mentor
                self.iterate_all_student_for_mentor(mentor.students.all(), self.get_mentor_canvas_id(mentor_uniqname))

    def do(self):
            logger.warn("************ Student Explorer cron tab")

            status = ""

            status += "Start cron at: " +  str(datetime.datetime.now()) + "\n"
            self.update_advisors_in_canvas_sites()

            status += "End cron at: " +  str(datetime.datetime.now()) + "\n"

            logger.info("************ total status=" + status + "/n/n")

            return status