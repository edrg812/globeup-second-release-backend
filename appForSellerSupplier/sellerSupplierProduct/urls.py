

####################### previous urls before comment #############
# from django.urls import path
# from . import views

# urlpatterns = [
#     # Products
#     path("seller_supplier_products/", views.SellerSupplierProductListView.as_view(), name="product-list"),
#     path("seller_supplier_products/create/", views.SellerSupplierProductCreateView.as_view()),
#     path("seller_supplier_products/<int:id>/", views.SellerSupplierProductDetailView.as_view(), name="product-detail"),
#     path("seller_supplier_products/<int:id>/update/", views.SellerSupplierProductUpdateView.as_view(), name="product-update"),

#     # Variants
#     path("sellersuppliervariants/", views.SellerSupplierProductVariantListView.as_view(), name="variant-list"),
    
   
# ]



########### new url after comment ###############

from . import views
# urls.py (current / improved)
from django.urls import path
from .productsViews import (
    SellerSupplierProductListView,
    SellerSupplierProductDetailView,
    SellerSupplierProductCreateView,
    SellerSupplierProductUpdateDeleteView,
)
from .variantViews import (
    SellerSupplierProductVariantListView,
    SellerSupplierProductVariantDetailView,
    SellerSupplierProductVariantCreateView,
    SellerSupplierProductVariantUpdateDeleteView,
    SingleSupplierProductVariantListView
)

urlpatterns = [
    # ------------------- PRODUCT -------------------
    # Read-only
    path("seller_supplier_products/", SellerSupplierProductListView.as_view(), name="product-list"),
    path("seller_supplier_products/<int:id>/", SellerSupplierProductDetailView.as_view(), name="product-detail"),

    # Write
    path("seller_supplier_products/create/", SellerSupplierProductCreateView.as_view(), name="product-create"),
    path("seller_supplier_products/<int:id>/update-delete/", SellerSupplierProductUpdateDeleteView.as_view(), name="product-update-delete"),

    # ------------------- VARIANTS -------------------
    # Read-only
    path("seller_supplier_variants/", SellerSupplierProductVariantListView.as_view(), name="variant-list"),
    path("seller_supplier_variants/<int:id>/", SellerSupplierProductVariantDetailView.as_view(), name="variant-detail"),

    # Write
    path("seller_supplier_variants/create/", SellerSupplierProductVariantCreateView.as_view(), name="variant-create"),
    path("seller_supplier_variants/<int:id>/update-delete/", SellerSupplierProductVariantUpdateDeleteView.as_view(), name="variant-update-delete"),
    path("supplier_added_product_variants", SingleSupplierProductVariantListView.as_view(), name = "supplier-product-details"),


    #this will edit price
    path("supplier/product-variant/<int:pk>/edit-price/", views.SupplierProductVariantPriceUpdateView.as_view()),
    #this will edit price
    path("delete/product/<int:pk>/", views.DestroyProductVariantView.as_view())
]







