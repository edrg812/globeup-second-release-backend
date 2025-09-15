from . import views
from django.urls import path

urlpatterns = [
    path('', views.SellerSupplierCategoryListView.as_view(), name='seller-supplier-category-list'),
    path('create/', views.SellerSupplierCategoryCreateView.as_view(), name='seller-supplier-category-create'),
    path('<int:id>/update/', views.SellerSupplierCategoryUpdateView
            .as_view(), name='seller-supplier-category-update'),
    path('<int:id>/delete/', views.SellerSupplierCategoryDeleteView
            .as_view(), name='seller-supplier-category-delete'),
]