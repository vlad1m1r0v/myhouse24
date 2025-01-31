from django.urls import path, include

from src.flat_owners import views

app_name = "flat-owners"

urlpatterns = [
    path('flat-owners/', include([
        path('create/', views.AdminFlatOwnerCreateView.as_view(), name='create'),
        path('<int:pk>/update/', views.AdminFlatOwnerUpdateView.as_view(), name='update'),
    ]))
]
