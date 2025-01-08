from django.urls import path, include

app_name = "authentication"

urlpatterns = [
    path('authentication/', include('src.authentication.urls'))
]
