from django.urls import path

from src.website_management import views

urlpatterns = [
    path('home/', views.WebsiteHomeView.as_view(), name='home'),
    path('about-us/', views.WebsiteAboutUsView.as_view(), name='about-us'),
    path('services/', views.WebsiteServicesView.as_view(), name='services'),
    path('tariffs/', views.WebsiteTariffsView.as_view(), name='tariffs'),
    path('contacts/', views.WebsiteContactsView.as_view(), name='contacts'),
]