from django.urls import path, reverse_lazy, include

from src.authentication.forms import AuthenticationPasswordResetForm, AuthenticationSetPasswordForm
from django.contrib.auth import views as auth_views

app_name = "password-reset"

urlpatterns = [
    path('password-reset/', include([
        path('',
             auth_views.PasswordResetView.as_view(
                 template_name="authentication/password_reset/form.html",
                 email_template_name="authentication/password_reset/email.txt",
                 subject_template_name="authentication/password_reset/subject.txt",
                 html_email_template_name="authentication/password_reset/email.html",
                 form_class=AuthenticationPasswordResetForm,
                 success_url=reverse_lazy('authentication:password-reset:done')
             ),
             name='index'),
        path('done/',
             auth_views.PasswordResetDoneView.as_view(
                 template_name="authentication/password_reset/done.html",
             ),
             name='done'),
        path('<uidb64>/<token>/',
             auth_views.PasswordResetConfirmView.as_view(
                 success_url=reverse_lazy('authentication:password-reset:complete'),
                 form_class=AuthenticationSetPasswordForm,
                 template_name='authentication/password_reset/confirm.html',
             ), name='confirm'),
        path('complete/',
             auth_views.PasswordResetCompleteView.as_view(
                 template_name='authentication/password_reset/complete.html',
             ),
             name='complete'),
    ]))
]
