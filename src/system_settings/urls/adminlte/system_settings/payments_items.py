from django.urls import path

from src.system_settings import views

app_name = "payment-items"

urlpatterns = [
    path('', views.AdminPaymentItemsView.as_view(), name='list'),
    path('datatable/', views.AdminPaymentItemsDatatableView.as_view(), name='datatable'),
    path('create/', views.AdminPaymentItemCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.AdminPaymentItemUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.AdminPaymentItemsDeleteView.as_view(), name='delete'),
]