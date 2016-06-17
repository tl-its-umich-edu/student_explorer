from django import forms


class FeedbackForm(forms.Form):
    feedback_message = forms.CharField(widget=forms.Textarea)
