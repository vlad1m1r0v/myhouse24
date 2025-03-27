from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


@shared_task
def send_verification_email(domain, uid, token, protocol, email):
    mail_subject = "Підтвердження акаунту для системи MyHouse24"

    message = render_to_string(
        template_name='authentication/account/verification_email.html',
        context={
            'domain': domain,
            'uid': uid,
            'token': token,
            "protocol": protocol
        })

    email_message = EmailMessage(mail_subject, message, settings.EMAIL_HOST_USER, [email])
    email_message.content_subtype = "html"
    email_message.send()
