from django.urls import path, include

from src.master_call_requests import views

app_name = "master-call-requests"

urlpatterns = [
    path('master-call-requests/', include([
        path('', views.AdminMasterCallRequestsListView.as_view(), name='list'),
        path('datatable/', views.AdminMasterCallRequestsDatatableView.as_view(), name='datatable'),
        path('create/', views.AdminMasterCallRequestCreateView.as_view(), name='create'),
        path('<int:pk>/update/', views.AdminMasterCallRequestUpdateView.as_view(), name='update'),
        path('<int:pk>/delete/', views.AdminMasterCallRequestsDeleteView.as_view(), name='delete'),
        path('<int:pk>/', views.AdminMasterCallRequestsDetailView.as_view(), name='detail'),
        path('api/flats/', views.AdminMasterCallRequestsFlatsView.as_view(), name='flats'),
        path('api/owners/', views.AdminMasterCallRequestsFlatOwnersView.as_view(), name='owners'),
        path('api/masters/', views.AdminMasterCallRequestMastersView.as_view(), name='masters'),
    ]))
]