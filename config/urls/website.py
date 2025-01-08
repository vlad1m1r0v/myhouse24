from django.urls import path, include

app_name = "website"

urlpatterns = [
    path('', include('src.website_management.urls.website'))
]
