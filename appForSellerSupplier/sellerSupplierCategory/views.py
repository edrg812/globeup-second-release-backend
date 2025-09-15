from django.shortcuts import render
from rest_framework import generics, permissions
# Create your views here.
from .models import SellerSupplierCategory
from .serializers import SellerSupplierCategorySerializer

class SellerSupplierCategoryListView(generics.ListAPIView):
    queryset = SellerSupplierCategory.objects.all().order_by('-id')
    serializer_class = SellerSupplierCategorySerializer
    permission_classes = [permissions.AllowAny]

# Create a brand (only admin users)
class SellerSupplierCategoryCreateView(generics.CreateAPIView):
    queryset = SellerSupplierCategory.objects.all()
    serializer_class = SellerSupplierCategorySerializer
    permission_classes = [permissions.IsAdminUser]

# Update a brand by ID (only admin users)
class SellerSupplierCategoryUpdateView(generics.UpdateAPIView):
    queryset = SellerSupplierCategory.objects.all()
    serializer_class = SellerSupplierCategorySerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"

# Delete a brand by ID (only admin users)
class SellerSupplierCategoryDeleteView(generics.DestroyAPIView):
    queryset = SellerSupplierCategory.objects.all()
    serializer_class = SellerSupplierCategorySerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"