from django.conf.urls import url

from . import views

app_name = 'management'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^users/$', views.UserListView.as_view(), name='user-list'),
    url(r'^cohorts/$', views.CohortListView.as_view(), name='cohort-list'),
    url(r'^cohorts/add/$', views.AddCohortView.as_view(), name='add-cohort'),
    url(r'^cohorts/download/$',
        views.CohortListDownloadView.as_view(),
        name='cohort-list-download'),
    url(r'^cohorts/detail/download/$',
        views.CohortDetailDownloadView.as_view(),
        name='cohort-detail-download'),
    url(r'^cohorts/edit/(?P<code>[\s\w-]+)/$',
        views.EditCohortView.as_view(),
        name='edit-cohort'),
    url(r'^cohorts/(?P<code>[\s\w-]+)/$',
        views.CohortDetailView.as_view(),
        name='cohort-detail'),
]
