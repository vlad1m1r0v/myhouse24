from celery import shared_task
from django.contrib.auth.forms import PasswordResetForm

from src.authentication.models import CustomUser


@shared_task
def send_reset_password_email(subject_template_name, email_template_name, context,
              from_email, to_email, html_email_template_name):
    context['user'] = CustomUser.objects.get(pk=context['user'])

    PasswordResetForm.send_mail(
        None,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name
    )