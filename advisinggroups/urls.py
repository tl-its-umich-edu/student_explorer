from django.conf.urls import url
from views import ExcelFormView, confirmTable, undoTable


urlpatterns = [
    url(r'^$', ExcelFormView.as_view(), name='index'),
    url(r'^confirm/$', confirmTable, name='confirm'),
    url(r'^undo/$', undoTable, name='undo'),
]
