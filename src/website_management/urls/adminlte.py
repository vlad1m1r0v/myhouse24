from django.urls import path, include

from src.website_management import views

app_name = "website-management"

urlpatterns = [
    path('website-management/', include([
        path('home/', views.AdminMainPageView.as_view(), name='home'),
        path('about-us/', views.AdminAboutUsPageView.as_view(), name='about-us'),
        path('services/', views.AdminServicesPageView.as_view(), name='services'),
        path('tariffs/', views.AdminTariffsPageView.as_view(), name='tariffs'),
        path('contacts/', views.AdminContactsPageView.as_view(), name='contacts'),
    ]))
]
