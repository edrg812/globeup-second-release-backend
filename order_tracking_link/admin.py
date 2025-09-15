from django.contrib import admin
from .models import CustomerOrderTrackingLink, ResellerOrderTrackingLink
# Register your models here.


admin.site.register(CustomerOrderTrackingLink)
admin.site.register(ResellerOrderTrackingLink)


