from django.core.cache import cache
import pandas as pd
import json
import logging
from django.http import JsonResponse
from django.views import generic
from advisinggroups.models import (Student,
                                   Advisor,
                                   Group,
                                   Import,
                                   StudentGroupAdvisor
                                   )


logger = logging.getLogger(__name__)


class ExcelFormView(generic.TemplateView):
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
        except Exception as e:
            status['completed'] = 'Fail'
            logger.exception(e.message)
        return JsonResponse(status)


class ConfirmImport(generic.View):

    def post(self, request, *args, **kwargs):
        status = {}
        try:
            mapping_data = request.POST['tabledata']
            if mapping_data:
                mapping_data = json.loads(mapping_data)
                df = cache.get('data')
                imp = Import.objects.create()

                for index, row in df.iterrows():
                    student_umid = row[mapping_data[
                        'advisinggroups_studentuniv_id']]
                    student_uniqname = row[mapping_data[
                        'advisinggroups_studentusername']]
                    advisor_uniqname = row[mapping_data[
                        'advisinggroups_advisorusername']]
                    cohort_name = row[mapping_data[
                        'advisinggroups_groupdescription']]

                    student, created = Student.objects.get_or_create(
                        univ_id=student_umid,
                        username=student_uniqname)
                    advisor, created = Advisor.objects.get_or_create(
                        username=advisor_uniqname)
                    group, created = Group.objects.get_or_create(
                        description=cohort_name)

                    StudentGroupAdvisor.objects.get_or_create(imp=imp,
                                                              student=student,
                                                              advisor=advisor,
                                                              group=group)
                status['completed'] = 'Success'
                status['current_id'] = imp.id
        except Exception as e:
            status['completed'] = 'Fail'
            logger.exception(e.message)
        return JsonResponse(status)


class UndoImport(generic.View):

    def post(self, request, *args, **kwargs):
        status = {}
        try:
            current_id = request.POST['id']
            if current_id:
                imp = Import.objects.get(id=current_id)
                imp.delete()
                status['completed'] = 'Success'
        except Exception as e:
            status['completed'] = 'Fail'
            logger.exception(e.message)
        return JsonResponse(status)
