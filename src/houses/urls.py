from django.urls import path
from src.houses import views

urlpatterns = [
    path('adminlte/houses/create/', views.AdminHouseCreateView.as_view(), name='adminlte_houses_create'),
    path('adminlte/houses/<int:pk>/', views.AdminHouseDetailView.as_view(), name='adminlte_house_detail'),
]