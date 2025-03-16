from django.urls import path, include

from src.flat_owners import views

app_name = "flat-owners"

urlpatterns = [
    path('flat-owners/', include([
        path('', views.AdminFlatOwnersListView.as_view(), name='list'),
        path('datatable/', views.AdminUsersDatatableView.as_view(), name='datatable'),
        path('create/', views.AdminFlatOwnerCreateView.as_view(), name='create'),
        path('<int:pk>/update/', views.AdminFlatOwnerUpdateView.as_view(), name='update'),
        path('api/houses/', views.AdminFlatOwnersHousesView.as_view(), name='houses'),
    ]))
]
