from django.urls import path, include

from src.system_settings import views

app_name = "tariffs"

urlpatterns = [
    path('tariffs/', include([
        path('', views.AccountTariffDetailView.as_view(), name='detail'),
    ]))
]