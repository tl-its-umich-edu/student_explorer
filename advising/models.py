from django.conf import settings
import importlib
from models_dev import *

if hasattr(settings, 'ADVISING_PACKAGE'):
    # Override the definitions above if an alternate package has been
    # specified.

    advising_models_module = settings.ADVISING_PACKAGE + '.models'
    advising_models = importlib.import_module(advising_models_module)

    Student = advising_models.Student
    Advisor = advising_models.Advisor
    Mentor = advising_models.Mentor
    Term = advising_models.Term
    AdvisorRole = advising_models.AdvisorRole
    StudentAdvisorRole = advising_models.StudentAdvisorRole
    Cohort = advising_models.Cohort
    StudentCohortMentor = advising_models.StudentCohortMentor
    ClassSite = advising_models.ClassSite
    ClassSiteTerm = advising_models.ClassSiteTerm
    Status = advising_models.Status
    StudentClassSiteStatus = advising_models.StudentClassSiteStatus
    Assignment = advising_models.Assignment
    StudentClassSiteAssignment = advising_models.StudentClassSiteAssignment

    EventType = advising_models.EventType

    WeeklyStudentClassSiteEvent = advising_models.WeeklyStudentClassSiteEvent
    WeeklyStudentClassSiteStatus = advising_models.WeeklyStudentClassSiteStatus
    WeeklyStudentClassSiteScore = advising_models.WeeklyStudentClassSiteScore
    WeeklyClassSiteScore = advising_models.WeeklyClassSiteScore
