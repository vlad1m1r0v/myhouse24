from django.urls import path, include

from src.dashboard import views

app_name = "dashboard"

urlpatterns = [
    path('dashboard/', include([
        path('', views.AdminDashboardView.as_view(), name='index'),
        path('api/receipt-chart/', views.AdminDashboardReceiptChartView.as_view(), name='receipt-chart'),
        path('api/cashbox-chart/', views.AdminDashboardCashBoxChartView.as_view(), name='cashbox-chart'),
    ]))
]