from django.urls import path, include

app_name = "system-settings"

urlpatterns = [path('system-settings/', include(
    [
        path('payment-items/',
             include('src.system_settings.urls.adminlte.payments_items')),
        path('payment-credential/',
             include('src.system_settings.urls.adminlte.payment_credential')),
        path('users/',
             include('src.system_settings.urls.adminlte.users')),
        path('permissions/',
             include('src.system_settings.urls.adminlte.permissions')),
        path('tariffs/',
             include('src.system_settings.urls.adminlte.tariffs')),
        path('services/',
             include('src.system_settings.urls.adminlte.services')),
    ]
))
               ]
