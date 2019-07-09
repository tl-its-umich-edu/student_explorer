from django import forms
from django.contrib.auth.models import User

from management.models import Cohort

import csv
import os
import re


class UserCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        default_password = User.objects.make_random_password()
        user.set_password(default_password)
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('username',)


class CohortForm(forms.ModelForm):
    members = forms.CharField(widget=forms.Textarea,
                              help_text=('Add two columns: student uniqname '
                                         'and mentor uniqname. '
                                         'Separate the columns with tabs, '
                                         'spaces or commas.'),
                              required=False)
    excel_file = forms.FileField(label='Select an Excel file to Import:',
                                 help_text=('Add two columns: student '
                                            'uniqname and mentor uniqname. '
                                            'Separate the columns with tabs, '
                                            'spaces or commas.'),
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
                    raise forms.ValidationError(f"Inconsistent Delimiter at Line {line_number + 1}")
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

        # verify the code input
        code = cleaned_data.get('code')
        if (not bool(re.match('^[-\w\s]+$', code))):
            msg = ("Please enter only alphanumeric, space, or dash characters for cohort code field")
            self.add_error('code', msg)

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
