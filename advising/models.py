from django.conf import settings
import importlib
from models_dev import *

if hasattr(settings, 'ADVISING_PACKAGE'):
    # Override the definitions above if an alternate package has been
    # specified.

    advising_models_module = settings.ADVISING_PACKAGE + '.models'
    advising_models = importlib.import_module(advising_models_module)

    # "Dimension" models

    Advisor = advising_models.Advisor
    Mentor = advising_models.Mentor
    Status = advising_models.Status
    Student = advising_models.Student
    Term = advising_models.Term
    SourceSystem = advising_models.SourceSystem

    # "Dimension" models that depend on SourceSystem

    AdvisorRole = advising_models.AdvisorRole
    Assignment = advising_models.Assignment
    ClassSite = advising_models.ClassSite
    Cohort = advising_models.Cohort
    EventType = advising_models.EventType

    # "Bridge" models

    ClassSiteTerm = advising_models.ClassSiteTerm
    StudentAdvisorRole = advising_models.StudentAdvisorRole
    StudentCohortMentor = advising_models.StudentCohortMentor

    # "Fact" models

    StudentClassSiteAssignment = advising_models.StudentClassSiteAssignment
    StudentClassSiteStatus = advising_models.StudentClassSiteStatus
    WeeklyClassSiteScore = advising_models.WeeklyClassSiteScore
    WeeklyStudentClassSiteEvent = advising_models.WeeklyStudentClassSiteEvent
    WeeklyStudentClassSiteScore = advising_models.WeeklyStudentClassSiteScore
    WeeklyStudentClassSiteStatus = advising_models.WeeklyStudentClassSiteStatus
