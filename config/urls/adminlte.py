from django.urls import path, include

app_name = "adminlte"

urlpatterns = [
    path('adminlte/', include([
        path('', include('src.flat_owners.urls.adminlte')),
        path('', include('src.houses.urls.adminlte')),
        path('', include('src.website_management.urls.adminlte')),
        path('', include('src.system_settings.urls.adminlte')),
        path('', include('src.flats.urls.adminlte')),
        path('', include('src.personal_accounts.urls.adminlte'))
    ]))
]
