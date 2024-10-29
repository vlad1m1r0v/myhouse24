from django.urls import path
from src.personal_accounts import views

urlpatterns = [
    path('adminlte/personal-accounts/create/',
         views.AdminPersonaAccountCreateView.as_view(),
         name='adminlte_personal_account_create'),
    path('adminlte/personal-accounts/<int:pk>/update/',
         views.AdminPersonaAccountUpdateView.as_view(),
         name='adminlte_personal_account_update'),
    path('adminlte/personal-accounts/flats/',
         views.AdminPersonalAccountFlatsView.as_view(),
         name='adminlte_personal_account_flats'),
    path('adminlte/personal-accounts/flats/owner/',
         views.AdminPersonalAccountOwnerView.as_view(),
         name='adminlte_personal_account_owner'
         )
]
