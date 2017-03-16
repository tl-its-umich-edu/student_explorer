from django import forms

from management.models import Cohort

import csv


class CohortForm(forms.ModelForm):
    members = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(CohortForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    def clean_members(self):
        data = self.cleaned_data['members']
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

    class Meta:
        model = Cohort
        fields = ('code', 'description', 'group',)
