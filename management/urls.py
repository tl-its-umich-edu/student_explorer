from django.conf.urls import url

from . import views

app_name = 'management'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^users/$', views.UserListView.as_view(), name='user-list'),
    url(r'^cohorts/$', views.CohortListView.as_view(), name='cohort-list'),
    url(r'^cohorts/add/$', views.AddCohortView.as_view(), name='add-cohort'),
    url(r'^users/add/$', views.AddUserView.as_view(), name='add-user'),
    url(r'^cohorts/download/$',
        views.CohortListDownloadView.as_view(),
        name='cohort-list-download'),
    url(r'^cohorts/detail/download/$',
        views.CohortDetailDownloadView.as_view(),
        name='cohort-detail-download'),
    url(r'^cohorts/(?P<code>[\s\w-]+)/members/download/$',
        views.CohortMembersDownloadView.as_view(),
        name='cohort-members-download'),
    url(r'^cohorts/(?P<code>[\s\w-]+)/members/$',
        views.CohortMembersView.as_view(),
        name='cohort-members'),
]
