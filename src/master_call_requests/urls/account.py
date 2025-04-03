from django.urls import path, include

from src.master_call_requests import views

app_name = "master-call-requests"

urlpatterns = [
    path('master-call-requests/', include([
        path('', views.AccountMasterCallRequestsListView.as_view(), name='list'),
        path('create/', views.AccountMasterCallRequestCreateView.as_view(), name='create'),
        path('<int:pk>/delete/', views.AccountMasterCallRequestDeleteView.as_view(), name='delete')
    ]))
]