from django.conf.urls import url

from . import views

app_name = 'management'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^users/$', views.UserListView.as_view(), name='user-list'),
    url(r'^cohorts/$', views.CohortListView.as_view(), name='cohort-list'),
]
