from django.urls import path, include

urlpatterns = [path('', include('src.system_settings.urls.adminlte'))]