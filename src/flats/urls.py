from django.urls import path

from src.flats import views

urlpatterns = [
    path('adminlte/flats/create/', views.AdminCreateFlatView.as_view(), name="adminlte_flat_create"),
    path('adminlte/flats/create/houses/', views.AdminFlatHousesView.as_view(), name="adminlte_flat_houses"),
    path('adminlte/flats/create/sections/', views.AdminFlatSectionsView.as_view(), name="adminlte_flat_sections"),
    path('adminlte/flats/create/floors/', views.AdminFlatFloorsView.as_view(), name="adminlte_flat_floors"),
    path('adminlte/flats/create/owners/', views.AdminFlatOwnersView.as_view(), name="adminlte_flat_owners"),
    path('adminlte/flats/create/tariffs/', views.AdminFlatTariffsView.as_view(), name="adminlte_flat_tariffs"),
]
