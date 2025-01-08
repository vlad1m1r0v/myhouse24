from django.urls import path

from src.system_settings import views

app_name = "users"

urlpatterns = [
    path('', views.AdminUsersView.as_view(), name='list'),
    path('datatable/', views.AdminUsersDatatableView.as_view(), name='datatable'),
    path('create/', views.AdminUserCreateView.as_view(), name='create'),
    path('<int:pk>/', views.AdminUserDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.AdminUserUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/',  views.AdminUserDeleteView.as_view(), name='delete')
]