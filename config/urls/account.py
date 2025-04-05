from django.urls import path, include

app_name = "account"

urlpatterns = [
    path('account/', include([
        path('', include('src.flat_owners.urls.account')),
        path('', include('src.master_call_requests.urls.account')),
        path('', include('src.user_messages.urls.account')),
        path('', include('src.system_settings.urls.account')),
        path('', include('src.payment_receipts.urls.account'))
    ]))
]
