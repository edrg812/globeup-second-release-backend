from django.contrib import admin
from .models import Contact
# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'hotline_number', 'phone_number', 'whatsapp_number', 'status', 'created_at')
    search_fields = ('email', 'hotline_number', 'phone_number', 'whatsapp_number')
    list_filter = ('status', 'created_at')


admin.site.register(Contact, ContactAdmin)


