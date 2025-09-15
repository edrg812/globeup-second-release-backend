from rest_framework import generics, permissions
from .models import SellerSupplierBrand
from .serializers import SellerSupplierBrandSerializer

# List all brands (any authenticated user)
class SellerSupplierBrandListView(generics.ListAPIView):
    queryset = SellerSupplierBrand.objects.all().order_by('-id')
    serializer_class = SellerSupplierBrandSerializer
    permission_classes = [permissions.AllowAny]

# Create a brand (only admin users)
class SellerSupplierBrandCreateView(generics.CreateAPIView):
    queryset = SellerSupplierBrand.objects.all()
    serializer_class = SellerSupplierBrandSerializer
    permission_classes = [permissions.IsAdminUser]

# Update a brand by ID (only admin users)
class SellerSupplierBrandUpdateView(generics.UpdateAPIView):
    queryset = SellerSupplierBrand.objects.all()
    serializer_class = SellerSupplierBrandSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"

# Delete a brand by ID (only admin users)
class SellerSupplierBrandDeleteView(generics.DestroyAPIView):
    queryset = SellerSupplierBrand.objects.all()
    serializer_class = SellerSupplierBrandSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"

