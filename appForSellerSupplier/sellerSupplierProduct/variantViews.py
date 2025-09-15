# views_variant.py
from rest_framework import generics, permissions
from .models import SellerSupplierProductVariant
from .serializers import SellerSupplierProductVariantSerializer
from .serializers import ProductVariantCreateUpdateSerializer



from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from django.core.paginator import Paginator


# --- Read-only list ---
class SellerSupplierProductVariantListView(generics.ListAPIView):
    queryset = SellerSupplierProductVariant.objects.all().select_related("product")
    serializer_class = SellerSupplierProductVariantSerializer
    permission_classes = [permissions.AllowAny]

class SingleSupplierProductVariantListView(generics.ListAPIView):
    serializer_class = SellerSupplierProductVariantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter variants where the product's user is the current user
        return SellerSupplierProductVariant.objects.filter(
            product__user=self.request.user
        ).select_related("product")

# --- Read-only detail ---
class SellerSupplierProductVariantDetailView(generics.RetrieveAPIView):
    queryset = SellerSupplierProductVariant.objects.all().select_related("product")
    serializer_class = SellerSupplierProductVariantSerializer
    lookup_field = "id"
    permission_classes = [permissions.AllowAny]

# --- Create variant ---
class SellerSupplierProductVariantCreateView(generics.CreateAPIView):
    queryset = SellerSupplierProductVariant.objects.all()
    serializer_class = ProductVariantCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

# --- Update/Delete variant ---
class SellerSupplierProductVariantUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SellerSupplierProductVariant.objects.all()
    serializer_class = ProductVariantCreateUpdateSerializer
    lookup_field = "id"
    permission_classes = [permissions.IsAuthenticated]
