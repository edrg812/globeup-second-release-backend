from django.urls import path
from . import views


urlpatterns = [
    path("", views.SellerSupplierBrandListView.as_view(), name="seller_supplier_brand_list_create"),
    path("create/", views.SellerSupplierBrandCreateView.as_view()),
    path("<str:id>/update/", views.SellerSupplierBrandUpdateView.as_view()),
    path("<str:id>/delete/", views.SellerSupplierBrandDeleteView.as_view()),
]


# from django.urls import path
# from .views import BrandListView, BrandCreateView, BrandUpdateView, BrandDeleteView

# urlpatterns = [
#     path('brands/', BrandListView.as_view(), name='brand-list'),
#     path('brands/create/', BrandCreateView.as_view(), name='brand-create'),
#     path('brands/<str:id>/update/', BrandUpdateView.as_view(), name='brand-update'),
#     path('brands/<str:id>/delete/', BrandDeleteView.as_view(), name='brand-delete'),
# ]
