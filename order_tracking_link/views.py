# from django.shortcuts import render
# from rest_framework.decorators import api_view, permission_classes
# from .serializers import CustomerOrderTrackingSerializer, ResellerOrderTrackingSerializer
# from rest_framework import permissions, status
# from .models import CustomerOrderTrackingLink, ResellerOrderTrackingLink
# from rest_framework.response import Response


# @api_view(['GET'])
# @permission_classes([permissions.IsAuthenticated])
# def get_cutomer_tracking_link_view(request):
#     requests = CustomerOrderTrackingLink.objects.all()
#     serializer = CustomerOrderTrackingSerializer(requests)
#     return Response(serializer.data, status=status.HTTP_200_OK)



# @api_view(['GET'])
# @permission_classes([permissions.IsAuthenticated])
# def get_seller_tracking_link_view(request):
#     requests = ResellerOrderTrackingLink.objects.all()
#     serializer = ResellerOrderTrackingSerializer(requests)
#     return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
# def post_customer_tracking_link_view(request):
#     serializer = CustomerOrderTrackingSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()  # Creates a new object
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
# def post_seller_tracking_link_view(request):
#     serializer = ResellerOrderTrackingSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions, status

from .models import CustomerOrderTrackingLink, ResellerOrderTrackingLink
from .serializers import CustomerOrderTrackingSerializer, ResellerOrderTrackingSerializer


# ---------- CUSTOMER ----------
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_customer_tracking_link_view(request, order_id):
    """Fetch tracking link for a specific order."""
    obj = get_object_or_404(CustomerOrderTrackingLink, order_model_id=order_id)
    serializer = CustomerOrderTrackingSerializer(obj)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def post_customer_tracking_link_view(request, order_id):
    """Create or update tracking link for a specific order."""
    obj, created = CustomerOrderTrackingLink.objects.get_or_create(order_model_id=order_id)
    serializer = CustomerOrderTrackingSerializer(obj, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------- SELLER ----------
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_seller_tracking_link_view(request, order_id):
    obj = get_object_or_404(ResellerOrderTrackingLink, order_model_id=order_id)
    serializer = ResellerOrderTrackingSerializer(obj)
    return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
# def post_seller_tracking_link_view(request, order_id):
#     obj, created = ResellerOrderTrackingLink.objects.get_or_create(order_model_id=order_id)
#     serializer = ResellerOrderTrackingSerializer(obj, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(
#             serializer.data,
#             status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
#         )
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# ---------- SELLER ----------
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def post_seller_tracking_link_view(request, order_id):
    try:
        # Get or create the tracking link for this specific order
        obj, created = ResellerOrderTrackingLink.objects.get_or_create(
            order_model_id=order_id
        )
        
        # Extract tracking link from request data
        tracking_link = (
            request.data.get('tracking_link') or 
            request.data.get('delivery_link')  # Support both field names
        )
        
        if not tracking_link:
            return Response(
                {"error": "Tracking link is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update the object directly (bypass serializer validation issues)
        obj.tracking_link = tracking_link
        obj.save()
        
        # Return the updated object using serializer
        serializer = ResellerOrderTrackingSerializer(obj)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )
        
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

