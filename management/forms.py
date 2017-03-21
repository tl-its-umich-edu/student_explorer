from django import forms

from management.models import Cohort

import csv
import os


class CohortForm(forms.ModelForm):
    members = forms.CharField(widget=forms.Textarea, required=False)
    excel_file = forms.FileField(label='Select an Excel file to Import:',
                                 required=False)

    def __init__(self, *args, **kwargs):
        super(CohortForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    def clean_members(self):
        data = self.cleaned_data['members']
        if data:
            sniffer = csv.Sniffer()
            members = data.split('\r\n')
            dialect = sniffer.sniff(members[0])
            delimiter = dialect.delimiter
            for line_number, member in enumerate(members):
                record = member.split(delimiter)
                if len(record) < 2:
                    raise (forms
                           .ValidationError(
                               "Inconsistent Delimiter at Line %d" % (
                                   line_number + 1)
                           ))
        return data

    def clean_excel_file(self):
        data = self.cleaned_data['excel_file']
        if data:
            ext = os.path.splitext(data.name)[1]
            valid_extensions = ['.xlsx', '.xls']
            if not ext.lower() in valid_extensions:
                raise forms.ValidationError("Unsupported file extension")
        return data

    def clean(self):
        cleaned_data = super(CohortForm, self).clean()
        members = cleaned_data.get('members')
        excel_file = cleaned_data.get('excel_file')

        if (not members and not excel_file) or (members and excel_file):
            msg = ("Please enter valid records in the textarea OR "
                   "upload a valid excel file")
            self.add_error('members', msg)
            self.add_error('excel_file', msg)

        return cleaned_data

    class Meta:
        model = Cohort
        fields = ('code', 'description', 'group',)
