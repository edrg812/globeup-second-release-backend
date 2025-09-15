# fraud/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import FraudAPI
from .serializers import FraudAPISerializer


class IsAdminUser(permissions.BasePermission):
    """Allow access only to admin users"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class FraudAPIListCreateView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        fraud_apis = FraudAPI.objects.all().order_by("-created_at")
        serializer = FraudAPISerializer(fraud_apis, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FraudAPISerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FraudAPIDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        return get_object_or_404(FraudAPI, pk=pk)

    def get(self, request, pk):
        fraud_api = self.get_object(pk)
        serializer = FraudAPISerializer(fraud_api)
        return Response(serializer.data)

    def put(self, request, pk):
        fraud_api = self.get_object(pk)
        serializer = FraudAPISerializer(fraud_api, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        fraud_api = self.get_object(pk)
        serializer = FraudAPISerializer(fraud_api, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        fraud_api = self.get_object(pk)
        fraud_api.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
