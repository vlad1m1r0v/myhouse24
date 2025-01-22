from django.urls import path, include

from src.houses import views

app_name = "houses"

urlpatterns = [
    path('houses/', include([
        path('', views.AdminHousesListView.as_view(), name='list'),
        path('datatable/', views.AdminHousesDatatableView.as_view(), name='datatable'),
        path('create/', views.AdminHouseCreateView.as_view(), name='create'),
        path('<int:pk>/', views.AdminHouseDetailView.as_view(), name='detail'),
        path('<int:pk>/update/', views.AdminHouseUpdateView.as_view(), name='update'),
        path('<int:pk>/delete/', views.AdminHousesDeleteView.as_view(), name='delete'),
    ]))
]
