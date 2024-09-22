from django.urls import path

from src.website_management import views

urlpatterns = [
    path('home/', views.WebsiteHomeView.as_view(), name='website_home'),
]