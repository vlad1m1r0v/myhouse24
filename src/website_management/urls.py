from django.urls import path

from src.website_management import views

urlpatterns = [
    path('adminlte/website-management/home/',
         views.MainPageView.as_view(),
         name='adminlte_website_management_home')
]