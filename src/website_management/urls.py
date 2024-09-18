from django.urls import path

from src.website_management import views

urlpatterns = [
    path('adminlte/website-management/home/',
         views.AdminMainPageView.as_view(),
         name='adminlte_website_management_home'),
    path('adminlte/website-management/about-us/',
         views.AdminAboutUsPageView.as_view(),
         name='adminlte_website_management_about_us'),
]