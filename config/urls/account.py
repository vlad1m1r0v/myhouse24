from django.urls import path, include

app_name = "account"

urlpatterns = [
    path('account/', include([
        path('', include('src.flat_owners.urls.account')),
    ]))
]
