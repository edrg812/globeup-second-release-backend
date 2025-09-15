from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from .models import Wishlist
from .serializers import WishlistSerializer


class WishlistListCreateAPIView(APIView):
    """List all wishlist items (for user) or add a new one"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.is_staff:
            wishlists = Wishlist.objects.select_related("user", "product").all()
        else:
            wishlists = Wishlist.objects.filter(user=request.user).select_related("product")
        serializer = WishlistSerializer(wishlists, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data["user_id"] = request.user.id
        serializer = WishlistSerializer(data=data)
        if serializer.is_valid():
            try:
                wishlist = serializer.save()
                return Response(WishlistSerializer(wishlist).data, status=status.HTTP_201_CREATED)
            except Exception:
                return Response({"error": "This product is already in your wishlist."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WishlistDetailAPIView(APIView):
    """Retrieve or delete a single wishlist item"""
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        qs = Wishlist.objects.select_related("product", "user")
        if user.is_staff:
            return get_object_or_404(qs, pk=pk)
        return get_object_or_404(qs, pk=pk, user=user)

    def get(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)

    def delete(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        wishlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
