from django.urls import path

from src.system_settings import views

urlpatterns = [
    path('adminlte/system-settings/payment-items/',
         views.AdminPaymentItemsView.as_view(),
         name='adminlte_payment_items_list'),
    path('adminlte/system-settings/payment-items/datatable/',
         views.AdminPaymentItemsDatatableView.as_view(),
         name='adminlte_payment_items_datatable'),
    path('adminlte/system-settings/payment-items/<int:pk>/delete/',
         views.AdminPaymentItemsDeleteView.as_view(),
         name='adminlte_payment_items_delete'),
    path('adminlte/system-settings/payment-items/create/',
         views.AdminPaymentItemCreateView.as_view(),
         name='adminlte_payment_items_create'),
    path('adminlte/system-settings/payment-items/<int:pk>/update/',
         views.AdminPaymentItemUpdateView.as_view(),
         name='adminlte_payment_items_update'),
    path('adminlte/system-settings/payment-credential/',
         views.AdminPaymentCredentialView.as_view(),
         name='adminlte_payment_credential'),
]
