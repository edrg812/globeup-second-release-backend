from django.urls import path
from . import views

urlpatterns = [
    # Reseller-specific views
    # Use this URL to create new orders and view the reseller's own orders.
    path(
        "reseller/orders/",
        views.ResellerOrderListCreateAPIView.as_view(),
        name="reseller-order-list-create",
    ),
    # Supplier-specific views
    # This single URL replaces the five separate status views.
    # You can now filter by status using a query parameter, e.g., /supplier/orders/?status=pending
    path(
        "supplier/orders/",
        views.SupplierOrderListAPIView.as_view(),
        name="supplier-order-list",
    ),
    # Common views for Reseller/Admin/Supplier
    # Retrieve, update, or delete a specific order by its ID.
    path("orders/<str:pk>/", views.OrderDetailAPIView.as_view(), name="order-detail"),
    # Update only the status of a specific order.
    path(
        "orders/<str:pk>/update-status/supplier/",
        views.OrderStatusUpdateAPIView.as_view(),
        name="order-status-update",
    ),
    # View all of a user's past orders.
    path("orders/history/", views.OrderHistoryView.as_view(), name="order-history"),
    # Order Items
    path(
        "order-items/",
        views.OrderItemListCreateAPIView.as_view(),
        name="orderitem-list-create",
    ),
    path(
        "order-items/<str:pk>/",
        views.SellerSupplierOrderItemDetailAPIView.as_view(),
        name="orderitem-detail",
    ),
]
