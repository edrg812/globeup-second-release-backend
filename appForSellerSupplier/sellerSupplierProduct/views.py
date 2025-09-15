

from rest_framework import generics, permissions
from .models import SellerSupplierProduct, SellerSupplierProductVariant
from .serializers import SellerSupplierProductSerializer, SellerSupplierProductVariantSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
import json
from .permissions import IsAdminOrSupplier, IsAdminOrSeller

from rest_framework import generics, permissions
from .models import SellerSupplierProduct
from .serializers import SellerSupplierProductSerializer


class IsSupplier(permissions.BasePermission):
    """
    Custom permission to only allow users with supplier profile.
    """
    
    def has_permission(self, request, view):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # Check if user has a profile and is a supplier
        return (hasattr(request.user, 'profile') and 
                request.user.profile.user_type == 'supplier')


class SellerSupplierProductListView(generics.ListCreateAPIView):
    queryset = SellerSupplierProduct.objects.all().prefetch_related("variants")
    serializer_class = SellerSupplierProductSerializer
    http_method_names = ["get", "post"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAdminOrSeller()]
        elif self.request.method == "POST":
            return [permissions.IsAdminUser(), IsSupplier()]
        return super().get_permissions()


class SellerSupplierProductDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a single product by its id.
    - RetrieveAPIView is a generic view for read-only endpoints of a single model instance.
    - permission_classes = [AllowAny] makes this endpoint publicly accessible.
    """

    # Prefetch related objects to optimize database queries.
    queryset = SellerSupplierProduct.objects.filter(is_active=True).prefetch_related(
        "variants"
    )  # , 'reviews__user')
    serializer_class = SellerSupplierProductSerializer
    lookup_field = "id"


# Create product (POST)
from rest_framework import generics, permissions
from .models import SellerSupplierProduct
from .serializers import SellerSupplierProductSerializer

class SellerSupplierProductCreateView(generics.CreateAPIView):
    queryset = SellerSupplierProduct.objects.all()
    serializer_class = SellerSupplierProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Update product (PUT/PATCH)
class SellerSupplierProductUpdateView(generics.UpdateAPIView):
    queryset = SellerSupplierProduct.objects.all()
    serializer_class = SellerSupplierProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"
    http_method_names = ["put", "patch"]


# ------------------- PRODUCT VARIANT VIEWS -------------------


# List all product variants (GET)(post)
class SellerSupplierProductVariantListCreateView(generics.ListCreateAPIView):
    queryset = SellerSupplierProductVariant.objects.all().select_related("product")
    serializer_class = SellerSupplierProductVariantSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ["get", "post"]





# Retrieve single variant (GET)
class ProductVariantDetailView(generics.RetrieveAPIView):
    queryset = SellerSupplierProductVariant.objects.all().select_related("product")
    serializer_class = SellerSupplierProductVariantSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ["get"]


# Update variant (PUT/PATCH)
class SellerSuplierProductVariantUpdateView(generics.UpdateAPIView):
    queryset = SellerSupplierProductVariant.objects.all().select_related("product")
    serializer_class = SellerSupplierProductVariantSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["put", "patch"]







#this view will give the list of productvariant created by a particular supplier
from rest_framework import generics, permissions
from .models import SellerSupplierProductVariant
from .serializers import SellerSupplierProductVariantSerializer

class SupplierProductVariantListView(generics.ListAPIView):
    """
    List all product variants created by the logged-in supplier.
    """
    serializer_class = SellerSupplierProductVariantSerializer
    permission_classes = [permissions.IsAuthenticated]  # only logged-in users

    def get_queryset(self):
        # Filter variants where the product's user is the logged-in user
        return SellerSupplierProductVariant.objects.filter(
            product__user=self.request.user
        ).select_related("product")











#this view will allow supplier to edit price and old_price of a particular product variant

from .serializers import PriceEditSerializer
from .permissions import IsSupplierOwner

class SupplierProductVariantPriceUpdateView(generics.UpdateAPIView):
    queryset = SellerSupplierProductVariant.objects.all()
    serializer_class = PriceEditSerializer
    permission_classes = [permissions.IsAuthenticated, IsSupplierOwner]
    http_method_names = ['patch']  # Only PATCH allowed


class DestroyProductVariantView(generics.DestroyAPIView):
    serializer_class = SellerSupplierProductVariantSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["delete"]
    lookup_field = "pk"

    def get_queryset(self):
        # Only allow the logged-in supplier to delete their own products
        user = self.request.user
        return SellerSupplierProduct.objects.filter(user=user)  # <-- changed 'supplier' to 'user'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Product deleted successfully"}, status=200)



