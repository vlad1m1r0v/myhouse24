from django.urls import path

from src.website_management import views

urlpatterns = [
    path('adminlte/website-management/home/',
         views.AdminMainPageView.as_view(),
         name='adminlte_website_management_home'),
    path('adminlte/website-management/about-us/',
         views.AdminAboutUsPageView.as_view(),
         name='adminlte_website_management_about_us'),
    path('adminlte/website-management/services/',
         views.AdminServicesPageView.as_view(),
         name='adminlte_website_management_services'),
    path('adminlte/website-management/tariffs/',
         views.AdminTariffsPageView.as_view(),
         name='adminlte_website_management_tariffs'),
    path('adminlte/website-management/contacts/',
         views.AdminContactsPageView.as_view(),
         name='adminlte_website_management_contacts'),
]