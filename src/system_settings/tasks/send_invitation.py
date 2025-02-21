from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


@shared_task
def send_invitation_email(email, login_url):
    subject = "Запрошення до MyHouse24"
    message = render_to_string(
        template_name='system_settings/adminlte/users/send_invitation.html',
        context={'login_url': login_url},
    )

    email_message = EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
    )

    email_message.content_subtype = 'html'
    email_message.send()
