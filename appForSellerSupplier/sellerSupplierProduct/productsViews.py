# views_product.py
from rest_framework import generics, permissions
from .models import SellerSupplierProduct
from .serializers import SellerSupplierProductSerializer
from .serializers import ProductCreateUpdateSerializer

# --- Read-only list (with nested variants, category/brand names) ---
class SellerSupplierProductListView(generics.ListAPIView):
    queryset = SellerSupplierProduct.objects.all().prefetch_related("variants")
    serializer_class = SellerSupplierProductSerializer
    permission_classes = [permissions.AllowAny]

# --- Read-only detail ---
class SellerSupplierProductDetailView(generics.RetrieveAPIView):
    queryset = SellerSupplierProduct.objects.all().prefetch_related("variants")
    serializer_class = SellerSupplierProductSerializer
    lookup_field = "id"
    permission_classes = [permissions.AllowAny]

# --- Create product (write serializer) ---
class SellerSupplierProductCreateView(generics.CreateAPIView):
    queryset = SellerSupplierProduct.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# --- Update/Delete product (write serializer) ---
class SellerSupplierProductUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SellerSupplierProduct.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    lookup_field = "id"
    permission_classes = [permissions.IsAuthenticated]
