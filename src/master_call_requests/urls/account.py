from django.urls import path, include

from src.master_call_requests import views

app_name = "master-call-requests"

urlpatterns = [
    path('master-call-requests/', include([
        path('', views.AccountMasterCallRequestsListView.as_view(), name='list'),
    ]))
]