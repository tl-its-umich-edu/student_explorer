from django.urls import path
from feedback import views

app_name = 'feedback'

urlpatterns = [
    path('', views.submitFeedback, name='feedback'),
]
