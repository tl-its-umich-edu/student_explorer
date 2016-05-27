from django.http import JsonResponse
from django.views import generic
from django.shortcuts import render
from advisinggroups.models import Student, Advisor, Group, StudentGroupAdvisor
from django.core.cache import cache
import pandas as pd
import json


class ExcelFormview(generic.TemplateView):
    template_name = 'advisinggroups/index.html'

    def post(self, request, *args, **kwargs):
        status = {}
        try:
            myfile = request.FILES['input-file']
            df = pd.read_excel(myfile)

            cache.set('data', df, 60 * 10)
            excel_data = df[:1].to_dict(orient='records')
            cols = list(df.columns.values)
            cols_ind = {cols.index(val): val for val in cols}

            status['completed'] = 'Success'
            status['excel_data'] = excel_data[0]
            status['cols_order'] = cols_ind
        except:
            status['completed'] = 'Fail'
        return JsonResponse(status)

    def get(self, request, *args, **kwargs):
        mapping_data = request.GET.get('tabledata')

        #
        # student_umid = row[0].value
        # student_uniqname = row[1].value
        # advisor_uniqname = row[2].value
        # cohort_name = row[3].value
        #
        # student, created = Student.objects.get_or_create(
        #     univ_id=student_umid,
        #     username=student_uniqname)
        # advisor, created = Advisor.objects.get_or_create(
        #     username=advisor_uniqname)
        # #group, created = Group.objects.get_or_create(
        #     description=cohort_name)
        #
        # #StudentGroupAdvisor.objects.get_or_create(
        #     student=student, advisor=advisor, group=group)

        my_mapping = {}
        my_mapping['advisinggroups_student'] = Student
        my_mapping['advisinggroups_advisor'] = Advisor
        my_mapping['advisinggroups_group'] = Group
        df = cache.get('data')
        if mapping_data:
            mapping_data = json.loads(mapping_data)
        return render(request, self.template_name)
