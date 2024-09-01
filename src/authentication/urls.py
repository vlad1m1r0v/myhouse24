from django.urls import path, reverse_lazy

from src.authentication.forms import AuthenticationPasswordResetForm, AuthenticationSetPasswordForm
from src.authentication.views import AuthenticationAdminLoginView, AuthenticationAdminLogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('authentication/adminlte/login/', AuthenticationAdminLoginView.as_view(),
         name='authentication_adminlte_login'),
    path('authentication/adminlte/logout/', AuthenticationAdminLogoutView.as_view(), name='authentication_adminlte_logout'),
    path('authentication/password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name="authentication/password_reset/password_reset_form.html",
             email_template_name="authentication/password_reset/password_reset_email.txt",
             subject_template_name="authentication/password_reset/password_reset_subject.txt",
             html_email_template_name="authentication/password_reset/password_reset_email.html",
             form_class=AuthenticationPasswordResetForm,
             success_url=reverse_lazy('authentication_password_reset_done')
         ),
         name='authentication_password_reset'),
    path('authentication/password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="authentication/password_reset/password_reset_done.html",
         ),
         name='authentication_password_reset_done'),
    path('authentication/password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             success_url=reverse_lazy('authentication_password_reset_complete'),
             form_class=AuthenticationSetPasswordForm,
             template_name='authentication/password_reset/password_reset_confirm.html',
         ), name='authentication_password_reset_confirm'),
    path('authentication/password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='authentication/password_reset/password_reset_complete.html',
         ),
         name='authentication_password_reset_complete'),
]
