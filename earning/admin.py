from django.contrib import admin
from .models import Earning

# Register your models here.
class EarningAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'current_balance', 'pending_payout',"completed_payout", "user_requested_amount_withdraw","status", "created_at", "updated_at")  # Update field names as needed
admin.site.register(Earning, EarningAdmin)


