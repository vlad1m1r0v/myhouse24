from django.urls import path, include

from src.payment_receipts import views

app_name = "receipts"

urlpatterns = [
    path('receipts/', include([
        path('', views.AccountReceiptsListView.as_view(), name='list'),
        path('<int:pk>/', views.AccountReceiptDetailView.as_view(), name='detail'),
        path('<int:pk>/download/', views.AccountReceiptDownloadView.as_view(), name='download'),
        path('<int:pk>/print/', views.AccountReceiptPrintView.as_view(), name='print'),
        path('datatable/', views.AccountReceiptsDatatableView.as_view(), name='datatable'),
    ]))
]
