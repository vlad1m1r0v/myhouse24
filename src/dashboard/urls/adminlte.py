from django.urls import path, include

from src.dashboard import views

app_name = "dashboard"

urlpatterns = [
    path('dashboard/', include([
        path('', views.AdminDashboardView.as_view(), name='index'),
    ]))
]