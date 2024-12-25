from django.urls import path

from src.master_call_requests import views

urlpatterns = [
    path('adminlte/master-call-requests/',
         views.AdminMasterCallRequestListView.as_view(),
         name="adminlte_master_call_requests_list"),
    path('adminlte/master-call-requests/datatable/',
         views.AdminMasterCallRequestDatatableView.as_view(),
         name="adminlte_master_call_requests_datatable"),
    path('adminlte/master-call-requests/create/',
         views.AdminMasterCallRequestCreateView.as_view(),
         name="adminlte_master_call_request_create"),
    path('adminlte/master-call-requests/<int:pk>/update/',
         views.AdminMasterCallRequestUpdateView.as_view(),
         name="adminlte_master_call_request_update"),
    path('adminlte/master-call-requests/<int:pk>/delete/',
         views.AdminMasterCallRequestDeleteView.as_view(),
         name="adminlte_master_call_request_delete"),
    path('adminlte/master-call-requests/<int:pk>/',
         views.AdminMasterCallRequestDetailView.as_view(),
         name="adminlte_master_call_request_detail"),
    path('adminlte/master-call-requests/flat/<int:flat_id>/',
         views.AdminMasterCallRequestFlatView.as_view(),
         name="adminlte_master_call_request_flat"),
    path('adminlte/master-call-requests/masters/',
         views.AdminMasterCallRequestMastersView.as_view(),
         name="adminlte_master_call_request_masters"),
]