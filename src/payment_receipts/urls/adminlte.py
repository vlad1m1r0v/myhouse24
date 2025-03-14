from django.urls import path, include

from src.payment_receipts import views

app_name = "receipts"

urlpatterns = [
    path('receipts/', include([
        path('create/', views.AdminReceiptsCreateView.as_view(), name='create'),
        path('<int:pk>/update/', views.AdminReceiptsUpdateView.as_view(), name='update'),
        path('api/houses/', views.AdminReceiptsHousesView.as_view(), name='houses'),
        path('api/sections/', views.AdminReceiptsSectionsView.as_view(), name='sections'),
        path('api/flats/', views.AdminReceiptsFlatsView.as_view(), name='flats'),
        path('api/tariffs/', views.AdminReceiptsTariffsView.as_view(), name='tariffs'),
        path('api/flat-info/', views.AdminReceiptsFlatInfoView.as_view(), name='flat-info'),
        path('api/flat-info-by-account/', views.AdminReceiptsFlatInfoByAccountView.as_view(), name='flat-info-by-account'),
        path('api/services/', views.AdminReceiptsServicesView.as_view(), name='services'),
        path('api/indicators/', views.AdminReceiptsIndicatorsView.as_view(), name='indicators'),
        path('api/datatable/', views.AdminReceiptsIndicatorsDatatableView.as_view(), name='datatable-for-form'),
    ]))
]
