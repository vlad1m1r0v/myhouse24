from django.urls import path, include
import src.authentication.views as views

app_name = "password-reset"

urlpatterns = [
    path('password-reset/', include([
        path('', views.AuthenticationPasswordResetView.as_view(), name='index'),
        path('done/', views.AuthenticationPasswordResetDoneView.as_view(), name='done'),
        path('<uidb64>/<token>/', views.AuthenticationPasswordResetConfirmView.as_view(), name='confirm'),
        path('complete/', views.PasswordResetCompleteView.as_view(), name='complete'),
    ]))
]
