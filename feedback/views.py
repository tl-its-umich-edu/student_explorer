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
            user = request.user
            feedback_message = form.cleaned_data['feedback_message']

            feedback = Feedback.objects.create(
                user=user, feedback_message=feedback_message)

            feedback_message_email = "From: %s <%s>\nFeedback:\n\n%s" % (
                user.get_full_name(), user.email, feedback_message)
            send_mail('Student Explorer Feedback (%s : %s)' % (
                feedback.id, user.email),
                feedback_message_email, settings.FEEDBACK_EMAIL,
                (settings.FEEDBACK_EMAIL,),
                fail_silently=False,
            )
            return HttpResponseRedirect('/')
    else:
        form = FeedbackForm()

    return render(
        request,
        'feedback/feedback.html',
        {'form': form}
    )
