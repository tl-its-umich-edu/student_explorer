from django.urls import path

from . import views

app_name = 'management'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('cohorts/', views.CohortListView.as_view(), name='cohort-list'),
    path('cohorts/add/', views.AddCohortView.as_view(), name='add-cohort'),
    path('users/add/', views.AddUserView.as_view(), name='add-user'),
    path('cohorts/download/', views.CohortListDownloadView.as_view(), name='cohort-list-download'),
    path('cohorts/detail/download/', views.CohortDetailDownloadView.as_view(), name='cohort-detail-download'),
    path(
        'cohorts/<code>/members/download/',
        views.CohortMembersDownloadView.as_view(),
        name='cohort-members-download'
    ),
    path('cohorts/<code>/members/', views.CohortMembersView.as_view(), name='cohort-members'),
]
