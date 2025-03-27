from django.urls import path, include
urlpatterns = [
    path('', include([
        path('', include('src.authentication.urls.adminlte')),
        path('', include('src.authentication.urls.account')),
        path('', include('src.authentication.urls.password_reset')),
    ]))
]
