from django.urls import path, include

from src.user_messages import views
from src.user_messages.views import AdminMessagesListView

app_name = "messages"

urlpatterns = [
    path('messages/', include([
        path('', AdminMessagesListView.as_view(), name='list'),
        path('create/', views.AdminMessageCreateView.as_view(), name='create'),
        path('<int:pk>/', views.AdminMessageDetailView.as_view(), name='detail'),
        path('<int:pk>/delete/', views.AdminMessageDeleteView.as_view(), name='delete'),
        path('api/houses/', views.AdminMessagesHousesView.as_view(), name='houses'),
        path('api/sections/', views.AdminMessagesSectionsView.as_view(), name='sections'),
        path('api/floors/', views.AdminMessagesFloorsView.as_view(), name='floors'),
        path('api/flats/', views.AdminMessagesFlatsView.as_view(), name='flats'),
    ]))
]