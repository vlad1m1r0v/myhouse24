from django.urls import path, include

from src.authentication.views import (
    AuthenticationAdminLoginView,
    AuthenticationAdminLogoutView
)

app_name = 'adminlte'

urlpatterns = [
    path('adminlte/', include([
        path('login/',
             AuthenticationAdminLoginView.as_view(),
             name='login'),
        path('logout/',
             AuthenticationAdminLogoutView.as_view(),
             name='logout')
    ]))
]
