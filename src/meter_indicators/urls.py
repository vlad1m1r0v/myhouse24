from django.urls import path

from src.meter_indicators import views

urlpatterns = [
    path('adminlte/meter-indicators/create/',
         views.AdminCreateMeterIndicatorView.as_view(),
         name='adminlte_meter_indicator_create'),
    path('adminlte/meter-indicators/update/<int:pk>/',
         views.AdminUpdateMeterIndicatorView.as_view(),
         name='adminlte_meter_indicator_update'),
]