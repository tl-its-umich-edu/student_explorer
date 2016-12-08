import json

from django.views.generic import View
from django.http import HttpResponse

from tracking import create_event

class RecordEventView(View):
    eventname_param = 'name'
    eventnote_param = 'note'

    def get(self, request, *args, **kwargs):
        event = create_event(user=request.user, request=request,
                             name=request.GET.get(self.eventname_param), 
                             note=request.GET.get(self.eventnote_param))
        return HttpResponse(json.dumps({'eventname':event.name,'status':'saved'}), content_type='application/json')

record_event = RecordEventView.as_view()