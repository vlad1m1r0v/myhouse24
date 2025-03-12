from django.urls import path, include

from src.cash_box import views

app_name = "cash-box"

urlpatterns = [
    path('cash-box/', include([
        path('', views.AdminCashBoxListView.as_view(), name='list'),
        path('export/', views.AdminCashBoxExportView.as_view(), name='export'),
        path('datatable/', views.AdminCashBoxDatatableView.as_view(), name='datatable'),
        path('create/', views.AdminTransactionCreateView.as_view(), name='create'),
        path('<int:pk>/', views.AdminTransactionDetailView.as_view(), name='detail'),
        path('<int:pk>/update/', views.AdminTransactionUpdateView.as_view(), name='update'),
        path('<int:pk>/delete/', views.AdminTransactionDeleteView.as_view(), name='delete'),
        path('<int:pk>/export/', views.AdminTransactionExportView.as_view(), name='export-transaction'),
        path('api/owners/', views.AdminCashBoxOwnersView.as_view(), name='owners'),
        path('api/accounts/', views.AdminCashBoxAccountsView.as_view(), name='accounts'),
        path('api/payment-items/', views.AdminCashBoxPaymentItemsView.as_view(), name='payment-items'),
        path('api/managers/', views.AdminCashBoxManagersView.as_view(), name='managers'),
    ]))
]
