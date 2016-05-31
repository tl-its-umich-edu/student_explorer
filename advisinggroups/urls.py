from django.conf.urls import url
from views import ExcelFormView, confirmTable


urlpatterns = [
    url(r'^$', ExcelFormView.as_view(), name='index'),
    url(r'^confirm/$', confirmTable, name='confirm'),
]
