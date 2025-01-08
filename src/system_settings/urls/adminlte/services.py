from django.urls import path

from src.system_settings import views

app_name = "services"

urlpatterns = [
    path('', views.AdminServicesView.as_view(), name='index'),
]