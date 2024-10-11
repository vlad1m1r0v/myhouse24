from django.urls import path
from src.house_owners import views

urlpatterns = [
    path('adminlte/house-owners/create/',
         views.AdminHouseOwnerCreateView.as_view(),
         name='adminlte_house_owner_create'),
]
