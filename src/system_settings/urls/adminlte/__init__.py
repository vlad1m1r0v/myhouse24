from django.urls import path, include

app_name = "adminlte"

urlpatterns = [path("adminlte/", include('src.system_settings.urls.adminlte.system_settings'))]
