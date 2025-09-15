from rest_framework import generics, permissions
from .models import Brand
from .serializers import BrandSerializer

# List all brands (any authenticated user)
class BrandListView(generics.ListAPIView):
    queryset = Brand.objects.all().order_by('-id')
    serializer_class = BrandSerializer
    permission_classes = [permissions.AllowAny]

# Create a brand (only admin users)
class BrandCreateView(generics.CreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAdminUser]

# Update a brand by ID (only admin users)
class BrandUpdateView(generics.UpdateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"

# Delete a brand by ID (only admin users)
class BrandDeleteView(generics.DestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"

