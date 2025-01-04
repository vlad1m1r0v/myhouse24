from django.urls import path
from src.system_settings import views

app_name = "payment-credential"

urlpatterns = [
    path('', views.AdminPaymentCredentialView.as_view(), name='index'),
]
