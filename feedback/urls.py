from django.conf.urls import url
from feedback import views

urlpatterns = [
    url(
        r'^$', views.submitFeedback, name='feedback'), ]
