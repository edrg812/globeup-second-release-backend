from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import WithdrawRequestByReseller
from .serializers import WithdrawRequestByResellerSerializer

# ✅ Create a withdrawal request
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_withdraw_request(request):
    serializer = WithdrawRequestByResellerSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(user=request.user)  # attach logged-in user automatically
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Optional: List all withdrawal requests of the logged-in user
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_my_withdraw_requests(request):
    requests = WithdrawRequestByReseller.objects.filter(user=request.user).order_by('-requested_at')
    serializer = WithdrawRequestByResellerSerializer(requests, many=True)
    return Response(serializer.data)


from django.utils.timezone import now

# Optional: update processed at by admin after payment
@api_view(['PATCH'])
@permission_classes([permissions.IsAdminUser])
def update_withdraw_request(request, pk):
    try:
        withdraw_request = WithdrawRequestByReseller.objects.get(pk=pk)
    except WithdrawRequestByReseller.DoesNotExist:
        return Response({"detail": "Withdraw request not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = WithdrawRequestByResellerSerializer(
        withdraw_request,
        data=request.data,
        partial=True,
        context={'request': request}
    )

    if serializer.is_valid():
        # If processed=True, set both processed and processed_at
        if serializer.validated_data.get("processed") is True:
            serializer.save(processed=True, processed_at=now())  # ✅ update via serializer
        else:
            serializer.save()  # normal save

        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# ✅ Admin-only: list all withdrawal requests
@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def list_all_withdraw_requests_admin(request):
    requests = WithdrawRequestByReseller.objects.all().order_by('-requested_at')
    serializer = WithdrawRequestByResellerSerializer(requests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
