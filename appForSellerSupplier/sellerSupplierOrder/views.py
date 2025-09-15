from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from django.shortcuts import get_object_or_404
from .models import SellerSupplierOrder, SellerSupplierOrderItem
from .serializers import (
    SellerSupplierOrderSerializer,
    SellerSupplierOrderItemSerializer,
)
from user.models import UserProfile
from .permissions import IsOwnerOrAdminOrSupplier, IsResellerOrReadOnly
from django.db.models import Prefetch


class ResellerOrderListCreateAPIView(APIView):
    """Allow only resellers to view (GET) or create (POST) their own orders."""

    permission_classes = [IsResellerOrReadOnly]

    def get(self, request):
        orders = SellerSupplierOrder.objects.filter(user=request.user).order_by(
            "-created_at"
        )
        serializer = SellerSupplierOrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data["user"] = request.user.id
        serializer = SellerSupplierOrderSerializer(
            data=data, context={"request": request}
        )

        if serializer.is_valid():
            order = serializer.save(user=request.user)
            return Response(
                SellerSupplierOrderSerializer(order).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailAPIView(APIView):
    """
    Retrieve, update, or delete a single order.
    A user can only access their own order. Admin and supplier can access any.
    """

    permission_classes = [IsOwnerOrAdminOrSupplier]

    def get_object(self, pk):
        order = get_object_or_404(
            SellerSupplierOrder.objects.prefetch_related(
                Prefetch(
                    "items",
                    queryset=SellerSupplierOrderItem.objects.select_related(
                        "product_variant"
                    ),
                )
            ),
            pk=pk,
        )
        self.check_object_permissions(self.request, order)
        return order

    def get(self, request, pk):
        order = self.get_object(pk)
        serializer = SellerSupplierOrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk):
        order = self.get_object(pk)
        serializer = SellerSupplierOrderSerializer(
            order, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        order = self.get_object(pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderStatusUpdateAPIView(APIView):
    """Update only the status of an order (supplier and admin only)"""

    # permission_classes = [permissions.i]

    def patch(self, request, pk):
        order = get_object_or_404(SellerSupplierOrder, pk=pk)
        self.check_object_permissions(request, order)

        status_value = request.data.get("status")
        if status_value not in dict(SellerSupplierOrder.STATUS_CHOICES):
            return Response(
                {"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = SellerSupplierOrderSerializer(
            order, data={"status": status_value}, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SupplierOrderListAPIView(generics.ListAPIView):
    """
    List all orders containing products created by the logged-in supplier.
    This view can be filtered by `status` using a query parameter (e.g., ?status=pending).
    """

    serializer_class = SellerSupplierOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            if (
                not hasattr(self.request.user, "profile")
                or self.request.user.profile.user_type != "supplier"
            ):
                return SellerSupplierOrder.objects.none()
        except UserProfile.DoesNotExist:
            return SellerSupplierOrder.objects.none()

        supplier_user = self.request.user
        queryset = (
            SellerSupplierOrder.objects.filter(
                items__product_variant__product__user=supplier_user
            )
            .distinct()
            .order_by("-created_at")
        )

        # Filter by status if query parameter exists
        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Manually serialize to filter items per supplier
        data = []
        for order in queryset:
            supplier_items = order.items.filter(
                product_variant__product__user=request.user
            )
            order_data = SellerSupplierOrderSerializer(order).data
            order_data["items"] = SellerSupplierOrderItemSerializer(
                supplier_items, many=True
            ).data
            data.append(order_data)

        return Response(
            {
                "status": request.query_params.get("status", "all"),
                "total_orders": len(data),
                "orders": data,
            },
            status=status.HTTP_200_OK,
        )


class OrderItemListCreateAPIView(APIView):
    """List all order items or create a new one"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        items = SellerSupplierOrderItem.objects.filter(
            order__user=request.user
        ).select_related("order", "product_variant")
        serializer = SellerSupplierOrderItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SellerSupplierOrderItemSerializer(data=request.data)
        if serializer.is_valid():
            item = serializer.save()
            return Response(
                SellerSupplierOrderItemSerializer(item).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SellerSupplierOrderItemDetailAPIView(APIView):
    """Retrieve, update, or delete a single order item"""

    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdminOrSupplier]

    def get_object(self, pk):
        item = get_object_or_404(
            SellerSupplierOrderItem.objects.select_related("order", "product_variant"),
            pk=pk,
        )
        self.check_object_permissions(self.request, item)
        return item

    def get(self, request, pk):
        item = self.get_object(pk)
        serializer = SellerSupplierOrderItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk):
        item = self.get_object(pk)
        serializer = SellerSupplierOrderItemSerializer(
            item, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderHistoryView(generics.ListAPIView):
    serializer_class = SellerSupplierOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SellerSupplierOrder.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )
