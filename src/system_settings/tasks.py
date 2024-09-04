from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import send_mail


@shared_task
def send_password_update_notification(subject_template_name, email_template_name, context, from_email, to_email):
    subject = render_to_string(subject_template_name, context).strip()
    message = render_to_string(email_template_name, context)
    send_mail(subject, '', from_email, [to_email], html_message=message)
