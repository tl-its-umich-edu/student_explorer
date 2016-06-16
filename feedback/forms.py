from django import forms


class FeedbackForm(forms.Form):
    user_name = forms.CharField(max_length=200)
    user_email = forms.EmailField()
    feedback_message = forms.CharField(widget=forms.Textarea)
