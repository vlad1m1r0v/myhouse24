from django.urls import path, include

from src.meter_indicators import views

app_name = "meter-indicators"

urlpatterns = [
    path('meter-indicators/', include([
        path('', views.AdminMeterIndicatorsListView.as_view(), name='list'),
        path('for-flat/', views.AdminMeterIndicatorsListForFlatView.as_view(), name='list-for-flat'),
        path('for-flat/datatable/', views.AdminMeterIndicatorsDatatableForFlatView.as_view(), name='datatable-for-flat'),
        path('datatable/', views.AdminMeterIndicatorsDatatableView.as_view(), name='datatable'),
        path('api/houses/', views.AdminMeterIndicatorsHousesView.as_view(), name='houses'),
        path('api/sections/', views.AdminMeterIndicatorsSectionsView.as_view(), name='sections'),
        path('api/flats/', views.AdminMeterIndicatorsFlatsView.as_view(), name='flats'),
        path('api/services/', views.AdminMeterIndicatorsServicesView.as_view(), name='services'),
    ]))
]
