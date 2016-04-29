from django.views import generic
from django.shortcuts import render


class IndexView(generic.View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
