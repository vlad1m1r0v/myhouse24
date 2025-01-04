from django.urls import path, include

app_name = "authentication"

urlpatterns = [
    path('authentication/', include([
        path('', include('src.authentication.urls.adminlte')),
        path('', include('src.authentication.urls.password_reset')),
    ]))
]
