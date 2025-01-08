from django.urls import path
from src.system_settings import views

app_name = "permissions"

urlpatterns = [
    path('', views.AdminGroupPermissionsView.as_view(), name='index'),
]
