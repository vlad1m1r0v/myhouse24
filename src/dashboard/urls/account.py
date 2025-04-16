from django.urls import path, include

from src.dashboard import views

app_name = "dashboard"

urlpatterns = [
    path('dashboard/', include([
        path('', views.AccountDashboardView.as_view(), name='index'),
        path('api/piechart-year/', views.AccountDashboardPiechartYearView.as_view(), name='piechart-year'),
        path('api/piechart-month/', views.AccountDashboardPiechartMonthView.as_view(), name='piechart-month'),
    ]))
]
