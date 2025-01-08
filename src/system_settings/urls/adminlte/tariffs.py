from django.urls import path

from src.system_settings import views

app_name = "tariffs"

urlpatterns = [
    path('', views.AdminTariffsView.as_view(), name='list'),
    path('datatable/', views.AdminTariffsDatatableView.as_view(), name='datatable'),
    path('create/', views.AdminTariffCreateView.as_view(), name='create'),
    path('<int:pk>/', views.AdminTariffDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.AdminTariffUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.AdminTariffDeleteView.as_view(), name='delete')
]