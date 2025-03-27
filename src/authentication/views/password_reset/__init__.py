from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)

from django.urls import reverse_lazy

from src.authentication.forms import (
    AuthenticationPasswordResetForm,
    AuthenticationSetPasswordForm
)


class AuthenticationPasswordResetView(PasswordResetView):
    template_name = "authentication/password_reset/form.html"
    email_template_name = "authentication/password_reset/email.txt"
    subject_template_name = "authentication/password_reset/subject.txt"
    html_email_template_name = "authentication/password_reset/email.html"
    form_class = AuthenticationPasswordResetForm
    success_url = reverse_lazy('authentication:password-reset:done')


class AuthenticationPasswordResetDoneView(PasswordResetDoneView):
    template_name = "authentication/password_reset/done.html"


class AuthenticationPasswordResetConfirmView(PasswordResetConfirmView):
    success_url=reverse_lazy('authentication:password-reset:complete')
    form_class=AuthenticationSetPasswordForm
    template_name='authentication/password_reset/confirm.html'


class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'authentication/password_reset/complete.html'