from django.urls import path, include

from src.user_messages import views
from src.user_messages.views import AccountMessageDetailView, AccountMessagesDeleteView

app_name = "messages"

urlpatterns = [
    path('messages/', include([
        path('', views.AccountMessagesListView.as_view(), name='list'),
        path('datatable/', views.AccountMessagesDatatableView.as_view(), name='datatable'),
        path('delete-many/', views.AccountMessagesDeleteManyView.as_view(), name='delete-many'),
        path('<int:pk>/', AccountMessageDetailView.as_view(), name='detail'),
        path('<int:pk>/delete/', AccountMessagesDeleteView.as_view(), name='delete'),
    ]))
]
