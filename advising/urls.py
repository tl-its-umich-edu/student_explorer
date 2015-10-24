from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from advising import views

urlpatterns = [
    url(r'^$', views.api_root, name='advising-api-root'),
    url(r'^config/$', views.config, name='config'),

    url(r'^advisors/$',
        views.AdvisorList.as_view(),
        name='advisor-list'),
    url(r'^advisors/(?P<username>[a-zA-Z ]*)/$',
        views.AdvisorDetail.as_view(),
        name='advisor-detail'),
    url(r'^advisors/(?P<username>[a-zA-Z ]*)/students/$',
        views.AdvisorStudentsList.as_view(),
        name='advisor-students-list'),

    url(r'^students/$',
        views.StudentList.as_view(),
        name='student-list'),
    url(r'^students/(?P<username>[a-zA-Z ]*)/$',
        views.StudentDetail.as_view(),
        name='student-detail'),
    url(r'^students/(?P<username>[a-zA-Z ]*)/full/$',
        views.StudentFullDetail.as_view(),
        name='student-full-detail'),
    url(r'^students/(?P<username>[a-zA-Z ]*)/advisors/$',
        views.StudentAdvisorsList.as_view(),
        name='student-advisors-list'),
    url(r'^students/(?P<username>[a-zA-Z ]*)/class_sites/$',
        views.StudentClassSitesList.as_view(),
        name='student-classsite-list'),
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
