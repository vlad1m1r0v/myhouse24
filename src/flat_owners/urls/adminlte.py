from django.urls import path, include

from src.flat_owners import views

app_name = "flat-owners"

urlpatterns = [
    path('flat-owners/', include([
        path('', views.AdminFlatOwnersListView.as_view(), name='list'),
        path('invite/', views.AdminFlatOwnersInviteView.as_view(), name='invite'),
        path('<int:pk>/', views.AdminFlatOwnerDetailView.as_view(), name='detail'),
        path('<int:pk>/delete/', views.AdminFlatOwnersDeleteView.as_view(), name='delete'),
        path('datatable/', views.AdminFlatOwnersDatatableView.as_view(), name='datatable'),
        path('create/', views.AdminFlatOwnerCreateView.as_view(), name='create'),
        path('<int:pk>/update/', views.AdminFlatOwnerUpdateView.as_view(), name='update'),
        path('api/houses/', views.AdminFlatOwnersHousesView.as_view(), name='houses'),
    ]))
]
