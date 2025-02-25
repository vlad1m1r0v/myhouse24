from django.urls import path, include

app_name = "adminlte"

urlpatterns = [
    path('adminlte/', include([
        path('', include('src.system_settings.urls.adminlte')),
        path('', include('src.website_management.urls.adminlte')),
        path('', include('src.meter_indicators.urls.adminlte')),
        path('', include('src.master_call_requests.urls.adminlte')),
        path('', include('src.houses.urls.adminlte')),
        path('', include('src.flats.urls.adminlte')),
        path('', include('src.flat_owners.urls.adminlte')),
        path('', include('src.personal_accounts.urls.adminlte')),
        path('', include('src.payment_receipts.urls.adminlte'))
    ]))
]
