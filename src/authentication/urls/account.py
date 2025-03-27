from django.urls import path, include

import src.authentication.views as views

app_name = 'account'

urlpatterns = [
    path('account/', include([
        path('register/', views.AccountRegisterView.as_view(), name='register'),
        path('login/', views.AccountLoginView.as_view(), name='login'),
        path('activate/<uidb64>/<token>/', views.AccountActivateView.as_view(), name='activate'),
    ]))
]