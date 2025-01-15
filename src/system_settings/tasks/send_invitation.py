from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


@shared_task
def send_invitation_email(email):
    subject = "Запрошення до MyHouse24"
    message = render_to_string('system_settings/adminlte/users/send_invitation.html')

    email_message = EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
    )

    email_message.content_subtype = 'html'
    email_message.send()
