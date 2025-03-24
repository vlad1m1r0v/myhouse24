from django.urls import path

from src.payment_receipts import views

app_name = "templates"

urlpatterns = [
        path('', views.AdminReceiptsTemplateSettingsView.as_view(), name='index'),
        path('<int:pk>/print/', views.AdminReceiptPrintView.as_view(), name='print'),
        path('<int:pk>/select/', views.AdminReceiptsTemplateSetDefaultView.as_view(), name='select-as-default'),
        path('<int:pk>/delete/', views.AdminReceiptTemplatesDeleteView.as_view(), name='delete'),
]