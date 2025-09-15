# # signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from appForSellerSupplier.sellerSupplierOrder.models import SellerSupplierOrder, SellerSupplierOrderItem
# from earning.models import Earning

# @receiver(post_save, sender=SellerSupplierOrder)
# def update_earning_on_order_status(sender, instance, created, **kwargs):
#     """
#     Update the reseller's earning when order status changes.
#     """
#     if created:
#         return  # Ignore newly created orders, we only care about status updates

#     user = instance.user

#     # Get or create the Earning record for this user
#     earning, _ = Earning.objects.get_or_create(user=user)

#     # Calculate total reseller commission for the order
#     total_commission = sum(
#         (item.reselling_price - item.price) * item.quantity
#         for item in instance.items.all()
#     )

#     if instance.status.lower() == "delivered":
#         earning.current_balance += (total_commission*earning.reseller_commission)/100
#         # earning.reseller_commission += total_commission
#         earning.save()
#     elif instance.status.lower() == "cancelled":
#         # optionally, you can reset reseller_commission for cancelled orders
#         earning.reseller_commission += 0
#         earning.save()




# # signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from appForSellerSupplier.sellerSupplierOrder.models import SellerSupplierOrder
# from earning.models import Earning

# COMMISSION_PERCENTAGE = 10  # Set reseller commission %

# @receiver(post_save, sender=SellerSupplierOrder)
# def update_earning_on_order_status(sender, instance, created, **kwargs):
#     """
#     Update the reseller's earning when order status changes.
#     """
#     if created:
#         return  # Only handle updates

#     user = instance.user
#     earning, _ = Earning.objects.get_or_create(user=user)

#     # Calculate total commission for the order
#     total_commission = sum(
#         (item.reselling_price - item.price) * item.quantity
#         for item in instance.items.all()
#     )

#     # Apply fixed percentage
#     commission_to_add = total_commission * COMMISSION_PERCENTAGE / 100

#     if instance.status.lower() == "delivered":
#         # Only add if not already added
#         if not hasattr(instance, "_commission_added"):
#             earning.current_balance += commission_to_add
#             earning.reseller_commission += commission_to_add
#             earning.save()
#             instance._commission_added = True

#     elif instance.status.lower() == "cancelled":
#         # Optionally remove previously added commission
#         if hasattr(instance, "_commission_added") and instance._commission_added:
#             earning.current_balance -= commission_to_add
#             earning.reseller_commission -= commission_to_add
#             earning.save()
#             instance._commission_added = False



#this handles balance even if order is cancelld

# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from appForSellerSupplier.sellerSupplierOrder.models import SellerSupplierOrder
# from earning.models import Earning

# print("🔔 signals.py loaded")  # <--- debug check

# @receiver(post_save, sender=SellerSupplierOrder)
# def update_earning_on_order_status(sender, instance, created, **kwargs):
#     print("✅ Signal fired for order:", instance.id, "Status:", instance.status)  # debug
#     if created:
#         return

#     user = instance.user
#     earning, _ = Earning.objects.get_or_create(user=user)

#     total_commission = sum(
#         (item.reselling_price - item.price) * item.quantity
#         for item in instance.items.all()
#     )

#     if instance.status.lower() == "delivered":
#         earning.current_balance += (total_commission * earning.reseller_commission) / 100
#         earning.save()
#     elif instance.status.lower() == "cancelled":
#         earning.reseller_commission += 0
#         earning.save()


# # appForSellerSupplier/sellerSupplierOrder/signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import SellerSupplierOrder
# from earning.models import Earning

# @receiver(post_save, sender=SellerSupplierOrder, dispatch_uid="order_status_signal")
# def create_or_update_earning(sender, instance, created, **kwargs):
#     print(f"✅ Signal fired for order: {instance.id} Status: {instance.status}")

#     # Only run when status is delivered
#     if instance.status != "delivered":
#         print("⏭ Not delivered, skipping earning update")
#         return

#     supplier = getattr(instance, "supplier", None)
#     if not supplier:
#         print("⚠ No supplier found for this order")
#         return

#     earning, created = Earning.objects.get_or_create(
#         user=supplier.user,  # or supplier if Earning links directly to Supplier
#         defaults={"balance": 0},
#     )
#     print(f"📊 Earning object: {earning}, created={created}")
#     # earning.current_balance += instance.total_amount  # or instance.price/commission logic
#     earning.current_balance += 10  # or instance.price/commission logic
#     earning.save()
#     print(f"💰 New balance for {earning.user}: {earning.balance}")


# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal

from appForSellerSupplier.sellerSupplierOrder.models import (
    SellerSupplierOrder,
    SellerSupplierOrderItem,
)
from earning.models import Earning


# @receiver(post_save, sender=SellerSupplierOrder, dispatch_uid="update_earning_on_order_status")
# def update_earning_on_order_status(sender, instance, created, **kwargs):
#     """
#     Update the reseller's earning when order status changes to 'delivered'.
#     """
#     print(f"✅ Signal fired for order: {instance.id} Status: {instance.status}")

#     if created:
#         print("⏭ New order created, skipping balance update")
#         return

#     if instance.status.lower() != "delivered":
#         print("⏭ Not delivered, skipping earning update")
#         return

#     # Ensure order has a user (reseller)
#     if not instance.user:
#         print("⚠ No user found for this order")
#         return

#    # Get or create earning for the reseller
#     earning, _ = Earning.objects.get_or_create(user=instance.user)
#     # orders, _ =SellerSupplierOrder.objects.get_or_create(id=instance.id)
#     # Use commission % from the earning model (default 95 if not set)
#     commission_percent = earning.reseller_commission or Decimal("95.00")

#     total_commission = Decimal("0.00")
#     for item in instance.items.all():
#         profit = (item.reselling_price - item.price) * item.quantity
#         commission = (profit * commission_percent)/100
#         total_commission += commission

#     print(f"📊 Total commission for order {instance.id}: {total_commission} (with {commission_percent}% rate)")

#     # Update reseller balance
#     earning.current_balance += total_commission
#     earning.save()

#     print(f"💰 Updated balance for {earning.user}: {earning.current_balance}")


@receiver(post_save, sender=SellerSupplierOrder, dispatch_uid="update_earning_on_order_status")
def update_earning_on_order_status(sender, instance, created, **kwargs):
    print(f"✅ Signal fired for order: {instance.id} Status: {instance.status}")

    if created or instance.status.lower() != "delivered":
        print("⏭ Not delivered or new order, skipping")
        return

    earning, _ = Earning.objects.get_or_create(user=instance.user)

    commission_percent = earning.commission_percent or Decimal("95.00")

    total_commission = Decimal("0.00")
    for item in instance.items.all():
        profit = (item.reselling_price - item.price) * item.quantity
        # profit = (item.wholeSale_price - item.reselling_price) * item.amount
        commission = (profit * commission_percent) / Decimal("100")
        total_commission += commission
        #toal sales balance(reselling price)
        total_Sale=item.reselling_price

    print(f"📊 Commission for order {instance.id}: {total_commission} at {commission_percent}%")

    # ✅ Add to balances (cumulative, not reset)
    earning.current_balance += total_commission
    earning.total_sales_balance+=total_Sale
    earning.total_commission_earned += profit
    earning.save()

    print(f"💰 Updated balance: {earning.current_balance}, Total earned: {earning.total_commission_earned}")
