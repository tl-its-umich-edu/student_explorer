from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from advising import views

urlpatterns = [
    url(r'^$', views.api_root, name='advising-api-root'),

    # Advisor API URLs

    url(r'^advisors/$',
        views.AdvisorList.as_view(),
        name='advisor-list'),

    url(r'^advisors/(?P<username>[a-zA-Z ]*)/$',
        views.AdvisorDetail.as_view(),
        name='advisor-detail'),

    url(r'^advisors/(?P<username>[a-zA-Z ]*)/students/$',
        views.AdvisorStudentList.as_view(),
        name='advisor-students-list'),


    # Mentor API URLs

    url(r'^mentors/$',
        views.MentorList.as_view(),
        name='mentor-list'),

    url(r'^mentors/(?P<username>[a-zA-Z ]*)/$',
        views.MentorDetail.as_view(),
        name='mentor-detail'),

    url(r'^mentors/(?P<username>[a-zA-Z ]*)/students/$',
        views.MentorStudentList.as_view(),
        name='mentor-students-list'),


    # Class Site API URLs
    url(r'^class_sites/(?P<code>[a-zA-Z0-9\-\~  ]*)/assignments/download/$',
        views.ClassSiteAssignmentDownload.as_view(),
        name='class-site-assignment-download'),

    url(r'^class_sites/(?P<code>[a-zA-Z0-9\-\~  ]*)/student/' +
        '(?P<username>[a-zA-Z ]*)/assignments/download/$',
        views.ClassSiteAssignmentDownload.as_view(),
        name='class-site-assignment-download'),

    url(r'^class_sites/$',
        views.ClassSiteList.as_view(),
        name='class-site-list'),

    url(r'^class_sites/(?P<code>[a-zA-Z0-9\-\~  ]*)/$',
        views.ClassSiteDetail.as_view(),
        name='class-site-detail'),

    url(r'^class_sites/(?P<code>[a-zA-Z0-9\-\~  ]*)/students/$',
        views.ClassSiteStudentList.as_view(),
        name='class-site-students-list'),


    # Student API URLs

    url(r'^students/$',
        views.StudentList.as_view(),
        name='student-list'),

    url(r'^students/(?P<username>[a-zA-Z ]*)/$',
        views.StudentDetail.as_view(),
        name='student-detail'),

    url(r'^students/(?P<username>[a-zA-Z ]*)/advisors/$',
        views.StudentAdvisorRoleList.as_view(),
        name='student-advisors-list'),

    url(r'^students/(?P<username>[a-zA-Z ]*)/mentors/$',
        views.StudentMentorList.as_view(),
        name='student-mentors-list'),

    url(r'^students/(?P<username>[a-zA-Z ]*)/class_sites/$',
        views.StudentClassSiteList.as_view(),
        name='student-classsite-list'),

    url((r'^students/(?P<username>[a-zA-Z ]*)/class_sites/'
         '(?P<code>[a-zA-Z0-9\- ]*)/$'),
        views.StudentClassSiteDetail.as_view(),
        name='student-classsite-detail'),

    url((r'^students/(?P<username>[a-zA-Z ]*)/class_sites/'
         '(?P<code>[a-zA-Z0-9\- ]*)/assignments/$'),
        views.StudentClassSiteAssignmentList.as_view(),
        name='student-classsite-assignment-list'),

    url((r'^students/(?P<username>[a-zA-Z ]*)/class_sites/'
         '(?P<code>[a-zA-Z0-9\- ]*)/history/$'),
        views.StudentClassSiteHistoryList.as_view(),
        name='student-classsite-history-list'),
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
