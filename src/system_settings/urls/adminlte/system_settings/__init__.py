from django.urls import path, include

app_name = "system-settings"

urlpatterns = [path('system-settings/', include(
    [
        path('payment-items/',
             include('src.system_settings.urls.adminlte.system_settings.payments_items')),
        path('payment-credential/',
             include('src.system_settings.urls.adminlte.system_settings.payment_credential')),
        path('users/',
             include('src.system_settings.urls.adminlte.system_settings.users')),
        path('permissions/',
             include('src.system_settings.urls.adminlte.system_settings.permissions')),
        path('tariffs/',
             include('src.system_settings.urls.adminlte.system_settings.tariffs')),
        path('services/',
             include('src.system_settings.urls.adminlte.system_settings.services')),
    ]
))
               ]
