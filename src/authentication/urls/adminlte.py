from django.urls import path, include

import src.authentication.views as views

app_name = 'adminlte'

urlpatterns = [
    path('adminlte/', include([
        path('login/', views.AdminLoginView.as_view(),name='login'),
        path('logout/', views.AdminLogoutView.as_view(), name='logout')
    ]))
]
