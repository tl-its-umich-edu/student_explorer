from django.urls import path
from usage import views

app_name = 'usage'

urlpatterns = [
    path('', views.UsageView.as_view(), name='usage_index'),
    path('download/', views.DownloadCsvView.as_view(), name='usage_download'),
]
