from django.http import JsonResponse
from django.views import generic
from openpyxl import load_workbook
from advisinggroups.models import Student, Advisor, Group, StudentGroupAdvisor


class ExcelFormview(generic.TemplateView):
    template_name = 'advisinggroups/index.html'

    def post(self, request, *args, **kwargs):
        status = {}
        try:
            myfile = request.FILES['input-file']
            wb = load_workbook(filename=myfile, read_only=True)
            sheet_name = wb.get_sheet_names()[0]
            ws = wb[sheet_name]  # ws is now an IterableWorksheet
            first_row = True
            for row in ws.rows:
                if first_row:
                    first_row = False
                    continue

                student_umid = row[0].value
                student_uniqname = row[1].value
                advisor_uniqname = row[2].value
                cohort_name = row[3].value

                student_qs = Student.objects.filter(univ_id=student_umid)
                advisor_qs = Advisor.objects.filter(
                    username=advisor_uniqname)
                group_qs = Group.objects.filter(description=cohort_name)

                if not student_qs.exists():
                    student = Student.objects.create(univ_id=student_umid,
                                                     username=student_uniqname)
                else:
                    student = student_qs[0]
                if not advisor_qs.exists():
                    advisor = Advisor.objects.create(
                        username=advisor_uniqname)
                else:
                    advisor = advisor_qs[0]
                if not group_qs.exists():
                    group = Group.objects.create(description=cohort_name)
                else:
                    group = group_qs[0]

                StudentGroupAdvisor.objects.get_or_create(
                    student=student, advisor=advisor, group=group)
            status['completed'] = 'Done'
        except:
            status['completed'] = 'Error'
        return JsonResponse(status)
