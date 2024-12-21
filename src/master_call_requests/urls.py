from django.urls import path

from src.master_call_requests import views

urlpatterns = [
    path('adminlte/master-call-requests/create/',
         views.AdminMasterCallRequestCreateView.as_view(),
         name="adminlte_master_call_request_create"),
    path('adminlte/master-call-requests/flat/<int:flat_id>/',
         views.AdminMasterCallRequestFlatView.as_view(),
         name="adminlte_master_call_request_flat"),
    path('adminlte/master-call-requests/masters/',
         views.AdminMasterCallRequestMastersView.as_view(),
         name="adminlte_master_call_request_masters"),
]