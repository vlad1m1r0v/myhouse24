from django.urls import path, include

from src.flat_owners import views

app_name = "profile"

urlpatterns = [
    path('profile/', include([
        path('', views.AccountProfileView.as_view(), name='index'),
    ]))
]
