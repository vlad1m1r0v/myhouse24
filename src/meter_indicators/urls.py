from django.urls import path

from src.meter_indicators import views

urlpatterns = [
    path('adminlte/meter-indicators/create/',
         views.AdminCreateMeterIndicatorView.as_view(),
         name='adminlte_meter_indicator_create'),
    path('adminlte/meter-indicators/<int:pk>/update/',
         views.AdminUpdateMeterIndicatorView.as_view(),
         name='adminlte_meter_indicator_update'),
    path('adminlte/meter-indicators/<int:pk>/delete/',
         views.AdminMeterIndicatorDeleteView.as_view(),
         name='adminlte_meter_indicator_delete'),
    path('adminlte/meter-indicators/<int:pk>/',
         views.AdminDetailMeterIndicatorView.as_view(),
         name='adminlte_meter_indicator_detail'),
    path('adminlte/meter-indicators/for-flat/',
         views.AdminMeterIndicatorForFlatView.as_view(),
         name='adminlte_meter_indicators_for_flat'),
    path('adminlte/meter-indicators/for-flat/datatable/',
         views.AdminMeterIndicatorForFlatDatatableView.as_view(),
         name='adminlte_meter_indicators_for_flat_datatable'),
]
