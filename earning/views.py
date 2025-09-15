from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Earning
from .serializers import EarningSerializer, WithdrawRequestSerializer


class EarningListView(generics.ListAPIView):
    """List all earnings of the logged-in user"""
    serializer_class = EarningSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Earning.objects.filter(user=self.request.user)


class WithdrawRequestView(APIView):
    """User requests withdrawal"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = WithdrawRequestSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data["amount"]

            earning, created = Earning.objects.get_or_create(user=request.user)
            success, message = earning.request_withdraw(amount)

            if success:
                return Response({"detail": message}, status=status.HTTP_200_OK)
            return Response({"detail": message}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MarkAsPaidView(APIView):
    """Admin marks withdrawal as paid"""
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        try:
            earning = Earning.objects.get(pk=pk)
        except Earning.DoesNotExist:
            return Response({"detail": "Earning record not found"}, status=status.HTTP_404_NOT_FOUND)

        success, message = earning.mark_as_paid()
        if success:
            return Response({"detail": message}, status=status.HTTP_200_OK)
        return Response({"detail": message}, status=status.HTTP_400_BAD_REQUEST)


class MarkAsFailedView(APIView):
    """Admin marks withdrawal as failed"""
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        try:
            earning = Earning.objects.get(pk=pk)
        except Earning.DoesNotExist:
            return Response({"detail": "Earning record not found"}, status=status.HTTP_404_NOT_FOUND)

        success, message = earning.mark_as_failed()
        if success:
            return Response({"detail": message}, status=status.HTTP_200_OK)
        return Response({"detail": message}, status=status.HTTP_400_BAD_REQUEST)


class ChangeEarningStatusView(APIView):
    """Admin changes the status of an earning record"""
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        try:
            earning = Earning.objects.get(pk=pk)
        except Earning.DoesNotExist:
            return Response({"detail": "Earning record not found"}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get("status")
        if new_status not in ["pending", "paid", "failed"]:
            return Response({"detail": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        earning.status = new_status
        earning.save()
        return Response({"detail": f"Earning status changed to {new_status}"}, status=status.HTTP_200_OK)
    



from appForSellerSupplier.sellerSupplierOrder.models import SellerSupplierOrder

#change upcoming_balance based on commmission set by admin
# def update_upcoming_balance(user):
#     try:
#         earning = Earning.objects.get(user=user)
#     except Earning.DoesNotExist:
#         earning = Earning.objects.create(user=user)

#     # Calculate total commission from all delivered orders
#     total_commission = 0
#     delivered_orders = SellerSupplierOrder.objects.filter(user=user, status='delivered')
#     for order in delivered_orders:
#         if order.reselling_price and order.wholeSale_price:
#             commission = order.reselling_price - order.wholeSale_price
#             total_commission += commission

    # earning.upcoming_balance = (total_commission * earning.reseller_commission) / 100
    # earning.save()

def upcoming_balance_update(self, request, *args, **kwargs):
    try:
        earning = Earning.objects.get(user=request.user)
    except Earning.DoesNotExist:
        earning = Earning.objects.create(user=request.user)

    # Calculate total commission from all delivered orders
    total_commission = 0
    reseller_percentage_of_commission= earning.reseller_commission
    wholeSale_price = request.data.get("wholesale_price")
    reselling_price = request.data.get("reselling_price")
    if wholeSale_price and reselling_price:
        commission = float(reselling_price) - float(wholeSale_price)
        total_commission += commission
    earning.upcoming_balance = (reseller_percentage_of_commission * total_commission) / 100
    earning.save()
    return Response({"detail": "Upcoming balance added"}, status=status.HTTP_200_OK)

    

    


#for admin only
from rest_framework import generics, permissions
from .models import Earning
from .serializers import EarningAdminSerializer

# ✅ Admin can view all earnings
class EarningAdminListView(generics.ListAPIView):
    queryset = Earning.objects.all().order_by("-created_at")
    serializer_class = EarningAdminSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only admin can access

# ✅ Admin can retrieve & update earnings
class EarningAdminDetailView(generics.RetrieveUpdateAPIView):
    queryset = Earning.objects.all()
    serializer_class = EarningAdminSerializer
    permission_classes = [permissions.IsAdminUser]
