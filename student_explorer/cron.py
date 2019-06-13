 #python 3 support

 #py3 management conflict in cron

from django.db import connections as conns

import logging, datetime, json

from django.conf import settings

from django_cron import CronJobBase, Schedule

from umich_api.api_utils import ApiUtil

from seumich.models import Mentor

from management.models import MentorStudentCourseObserver

import dateutil.parser as parser

from decouple import config, Csv


logger = logging.getLogger(__name__)

# use ApiUtil for all API directory calls
apiUtil = ApiUtil(config("APIUTIL_URL", default=""), config("APIUTIL_KEY", default=""), config("APIUTIL_SECRET", default=""))

# cron job to populate course and user tables
class StudentExplorerCronJob(CronJobBase):

    schedule = Schedule(run_at_times=settings.RUN_AT_TIMES)
    code = 'student_explorer.StudentExplorerCronJob'    # a unique code

    def get_user_canvas_id(self, user_uniqname):
        """
        This process gets the canvas user id for user
        :param user_uniqname:
        :return:
        """
        user_result = apiUtil.api_call(f"aa/CanvasReadOnly/users/sis_login_id:{user_uniqname}/profile", "canvasreadonly")
        user_json = json.loads(user_result.text)
        return user_json.get("id", "")

    def mentor_in_affiliated_department(self, mentor_uniqname):
        """
        checks whether the mentor is in affiliated department
        :param mentor_uniqname:
        :return:
        """
        in_affiliated_department = False

        # get the array of affiliated department from config settings
        deptAffiliations = config("DEPT_AFFILIATION", default="", cast=Csv())

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
            user_affiliation = advisor_json.get("person").get("affiliation", "")
            # array of affiliated department.
            # The advisors of those department will be added as observers to student's Canvas courses
            in_affiliated_department = any(dept in deptAffiliations for dept in user_affiliation)

        return in_affiliated_department

    def add_user_as_observer_to_course(self, class_site_id, mentor_uniqname, mentor_canvas_user_id, user_canvas_user_id):
        """
        check whether the mentor is enrolled in this Canvas course
        if enrolled, do nothing;
        else add the mentor user to the Canvas course with Observer role
        :param class_site_id:
        :param mentor_uniqname:
        :param mentor_canvas_user_id:
        :param user_canvas_user_id:
        :return:
        """
        enrolled = False
        course_section_id = ""
        enrollments_resp = apiUtil.api_call(f"aa/CanvasReadOnly/courses/{class_site_id}/enrollments", "canvasreadonly")
        if (enrollments_resp.text.find("errors") != -1):
            # check for error message
            # {"errors":[{"message":"The specified resource does not exist."}],"error_report_id":7008726002}
            logger.warn(f"errors retrieving enrollments for class {class_site_id}: {enrollments_resp.text}")
        else:
            enrollments_json = json.loads(enrollments_resp.text)
            for item in enrollments_json:
                user_id=item.get("user_id")
                # get the Canvas section id for student enrollment
                if (user_id == user_canvas_user_id):
                    course_section_id = item.get("course_section_id")

            #enroll mentor to the Canvas course site with Observer role
            logger.info(f"Start: User id {mentor_canvas_user_id} is NOT enrolled in course {class_site_id}. Preparing to add user with Observer role. ")

            # POST call to add mentor with Observer role to given section
            payload_dictionary = {
                "enrollment[user_id]": mentor_canvas_user_id,
                "enrollment[type]": "ObserverEnrollment",
                "enrollment[enrollment_state]": "active",
                "enrollment[course_section_id]": course_section_id,
                "enrollment[limit_privileges_to_course_section]": "false",
                "enrollment[notify]": "true",
                "enrollment[associated_user_id]":user_canvas_user_id
            }
            post_result = apiUtil.api_call(f"aa/CanvasTLAdmin/courses/{class_site_id}/enrollments", "canvastladmin", method="POST", payload=payload_dictionary)

            #update the MentorStudentCourseObserver table with the insert information
            r = MentorStudentCourseObserver(student_id=user_canvas_user_id,
                                            mentor_uniqname= mentor_uniqname,
                                            course_id=class_site_id,
                                            course_section_id=course_section_id)
            r.save()
            logger.info(f"updated MentorStudentCourseObserver tracking table for student={user_canvas_user_id}, mentor_uniqname={mentor_uniqname}, course_id={class_site_id} course_section_id={course_section_id}")


            logger.info(f"End: result of adding user id {mentor_canvas_user_id} to course {class_site_id}: {post_result.text}")


    def iterate_all_student_for_mentor(self, student_list, mentor_uniqname, mentor_canvas_user_id ):
        """
        This process is loops through all students associated with the mentor
        :param student_list:
        :param mentor_uniqname:
        :param mentor_canvas_user_id:
        :return:
        """
        # all students associated with the mentor
        for student in student_list:
            uniqname = student.username
            student_canvas_id = self.get_user_canvas_id(uniqname)

            # all current class for given user
            class_sites = student.studentclasssitestatus_set.all()
            for element in class_sites:
                class_site_id = element.class_site.code
                logger.info(f"checking mentor={mentor_uniqname} for student={uniqname}, class site id={class_site_id}, class title={element.class_site} " )

                # check whether mentor has been added into the course as student observer
                qResult = MentorStudentCourseObserver.objects.filter(
                            student_id=str(student_canvas_id),
                            mentor_uniqname = str(mentor_uniqname),
                            course_id = str(class_site_id))

                if (len(qResult) == 0):
                    # if needed, add mentor as Observer to Canvas course site
                    self.add_user_as_observer_to_course(class_site_id, mentor_uniqname, mentor_canvas_user_id, student_canvas_id)
                else:
                    logger.debug(f"STOP here: existing record in MentorStudentCourseObserver tracking table for student={student_canvas_id}, mentor_uniqname={mentor_uniqname}, course={class_site_id}")

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

            qResult = MentorStudentCourseObserver.objects.filter(mentor_uniqname = mentor_uniqname )
            # if mentor uniqname is NOT already in tracking table, check for affiliated department
            if (len(qResult) > 0 or self.mentor_in_affiliated_department(mentor_uniqname)):
                    # iterator through all users for mentor
                    logger.info(f"{mentor_uniqname} is in affiliated department. ")
                    self.iterate_all_student_for_mentor(mentor.students.all(), mentor_uniqname, self.get_user_canvas_id(mentor_uniqname))

    def do(self):
            logger.warn("************ Student Explorer cron tab")

            status = ""

            status += "Start cron at: " +  str(datetime.datetime.now()) + "\n"
            self.update_advisors_in_canvas_sites()

            status += "End cron at: " +  str(datetime.datetime.now()) + "\n"

            logger.info("************ total status=" + status + "/n/n")

            return status