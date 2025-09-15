from django.contrib import admin
from .models import Category
# Register your models here.
class CateogoryAdmin(admin.ModelAdmin):
    list_display = ("id",'name', 'slug', 'created_at')
admin.site.register(Category, CateogoryAdmin)