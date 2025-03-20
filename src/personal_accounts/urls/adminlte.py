from django.urls import path, include

from src.personal_accounts import views

app_name = "personal-accounts"

urlpatterns = [
    path('personal-accounts/', include([
        path('', views.AdminPersonalAccountsListView.as_view(), name='list'),
        path('export/', views.AdminAccountsExportView.as_view(), name='export'),
        path('<int:pk>/', views.AdminPersonalAccountDetailView.as_view(), name='detail'),
        path('<int:pk>/delete/', views.AdminPersonalAccountsDeleteView.as_view(), name='delete'),
        path('datatable/', views.AdminPersonalAccountsDatatableView.as_view(), name='datatable'),
        path('create/', views.AdminPersonaAccountCreateView.as_view(), name='create'),
        path('<int:pk>/update/', views.AdminPersonaAccountUpdateView.as_view(), name='update'),
        path('api/houses/', views.AdminPersonalAccountHousesView.as_view(), name='houses'),
        path('api/sections/', views.AdminPersonalAccountSectionsView.as_view(), name='sections'),
        path('api/flats/', views.AdminPersonalAccountFlatsView.as_view(), name='tariffs'),
        path('api/owner/', views.AdminPersonalAccountOwnerView.as_view(), name='owner'),
        path('api/owners/', views.AdminPersonalAccountOwnersView.as_view(), name='owners'),
    ]))
]
