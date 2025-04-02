from django.urls import path, include

from src.flat_owners import views
from src.flat_owners.views import AccountProfileUpdateView

app_name = "profile"

urlpatterns = [
    path('profile/', include([
        path('', views.AccountProfileView.as_view(), name='index'),
        path('update/', AccountProfileUpdateView.as_view(), name='update')
    ]))
]
