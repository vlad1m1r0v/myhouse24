from django.urls import path

from src.flats import views

urlpatterns = [
    path('adminlte/flats/create/', views.AdminCreateFlatView.as_view(), name="adminlte_flat_create"),
    path('adminlte/flats/houses/', views.AdminFlatHousesView.as_view(), name="adminlte_flat_houses"),
    path('adminlte/flats/sections/', views.AdminFlatSectionsView.as_view(), name="adminlte_flat_sections"),
    path('adminlte/flats/floors/', views.AdminFlatFloorsView.as_view(), name="adminlte_flat_floors"),
    path('adminlte/flats/owners/', views.AdminFlatOwnersView.as_view(), name="adminlte_flat_owners"),
    path('adminlte/flats/tariffs/', views.AdminFlatTariffsView.as_view(), name="adminlte_flat_tariffs"),
    path('adminlte/flats/<int:pk>/update/', views.AdminUpdateFlatView.as_view(), name="adminlte_flat_update"),
]
