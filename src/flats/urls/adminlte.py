from django.urls import path, include

from src.flats import views

app_name = "flats"

urlpatterns = [
    path('flats/', include([
        path('', views.AdminFlatsListView.as_view(), name='list'),
        path('<int:pk>/delete/', views.AdminFlatsDeleteView.as_view(), name='delete'),
        path('datatable/', views.AdminFlatsDatatableView.as_view(), name='datatable'),
        path('create/', views.AdminFlatCreateView.as_view(), name='create'),
        path('<int:pk>/', views.AdminFlatDetailView.as_view(), name='detail'),
        path('<int:pk>/update/', views.AdminFlatUpdateView.as_view(), name='update'),
        path('api/houses/', views.AdminFlatHousesView.as_view(), name='houses'),
        path('api/sections/', views.AdminFlatSectionsView.as_view(), name='sections'),
        path('api/floors/', views.AdminFlatFloorsView.as_view(), name='floors'),
        path('api/owners/', views.AdminFlatOwnersView.as_view(), name='owners'),
        path('api/tariffs/', views.AdminFlatTariffsView.as_view(), name='tariffs'),
    ]))
]
