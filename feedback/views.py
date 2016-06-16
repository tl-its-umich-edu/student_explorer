from django.shortcuts import render
from feedback.forms import FeedbackForm
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from feedback.models import Feedback
from django.contrib.auth.decorators import login_required


@login_required
def submitFeedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            feedback_message = form.cleaned_data['feedback_message']
            from_address = form.cleaned_data['user_email']
            to_address = settings.FEEDBACK_EMAIL
            Feedback.objects.get_or_create(
                user_name=user_name, user_email=from_address,
                feedback_message=feedback_message)
            send_mail('Feedback From: ' + from_address,
                      feedback_message, from_address,
                      [to_address],
                      fail_silently=True,
                      )
            return HttpResponseRedirect('/')
    else:
        form = FeedbackForm()

    return render(
        request,
        'feedback/feedback.html',
        {'form': form}
    )
