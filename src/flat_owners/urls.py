from django.urls import path
from src.flat_owners import views

urlpatterns = [
    path('adminlte/flat-owners/create/',
         views.AdminFlatOwnerCreateView.as_view(),
         name='adminlte_flat_owner_create'),
    path('adminlte/flat-owners/<int:pk>/update/',
         views.AdminFlatOwnerUpdateView.as_view(),
         name='adminlte_flat_owner_update'),
]
