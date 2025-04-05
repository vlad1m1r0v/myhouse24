from django.urls import path, include

from src.payment_receipts import views

app_name = "receipts"

urlpatterns = [
    path('receipts/', include([
        path('', views.AccountReceiptsListView.as_view(), name='list'),
        path('datatable/', views.AccountReceiptsDatatableView.as_view(), name='datatable'),
    ]))
]