# from django.shortcuts import render
# from django.http import HttpResponse
# # Create your views here.
# from .serializers import UserProfileSerializer
# from .models import UserProfile
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status

# class UserProfileViewSet(APIView):
#     def get(self, request):
        
#         profile = UserProfile.objects.filter(user=request.user).first()
#         if not profile:
#             return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
#         serializer = UserProfileSerializer(profile)
#         return Response(serializer.data)
    
#     def patch(self, request):
    
#         profile = UserProfile.objects.filter(user=request.user).first()
#         if not profile:
#             return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

#         serializer = UserProfileSerializer(profile, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save(user=request.user)  # lock user
#             return Response({"msg": "thank you for updating profile"})
#         return Response(serializer.data, status=status.HTTP_200_OK)



from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from .serializers import UserProfileSerializer

class UserProfileViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = UserProfile.objects.filter(user=request.user).first()
        if not profile:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def patch(self, request):
        profile = UserProfile.objects.filter(user=request.user).first()
        if not profile:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # user is already locked in serializer if read_only
            return Response({"msg": "Profile updated successfully."})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import ResellerSuplierRequestSerializer
from .models import UserProfile

# ✅ Users create requests (attach to logged-in user)
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_reseller_supplier_request(request):
    # Ensure the user has a profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    serializer = ResellerSuplierRequestSerializer(
        profile, data=request.data, partial=True, context={"request": request}
    )
    if serializer.is_valid():
        serializer.save()  # user already attached
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ Only Admins can update requests
@api_view(["PUT", "PATCH"])
@permission_classes([permissions.IsAdminUser])
def update_reseller_supplier_request(request, pk):
    try:
        req = UserProfile.objects.get(pk=pk)
    except UserProfile.DoesNotExist:
        return Response(
            {"detail": "Request not found", "code": "request_not_found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = ResellerSuplierRequestSerializer(
        req, data=request.data, partial=True, context={"request": request}
    )
    if serializer.is_valid():
        serializer.save()  # admin can update any field
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




from rest_framework import generics, permissions
class RequestedUsersListView(generics.ListAPIView):
    serializer_class = ResellerSuplierRequestSerializer
    permission_classes = [permissions.IsAdminUser]  # or IsAuthenticated

    def get_queryset(self):
        return UserProfile.objects.filter(is_request=True)
    




from rest_framework import generics, permissions
from user.models import UserProfile
from .serializers import ResellerSuplierRequestSerializer

class AllUsersListView(generics.ListAPIView):
    """
    API endpoint to list all users (UserProfile).
    """
    queryset = UserProfile.objects.all().select_related("user")
    # serializer_class = ResellerSuplierRequestSerializer
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAdminUser]  # only admins can see all users

    def get_queryset(self):
        return (
            UserProfile.objects.all()
            .select_related("user")
            .order_by("-id")[:7]  # get latest 7 users
        )
