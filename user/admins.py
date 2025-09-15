# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import User, UserProfile
# from django.utils.translation import gettext_lazy as _

# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     model = User
#     list_display = ("phone_number", "email", "is_active", "is_staff", "is_verified", "date_joined")
#     search_fields = ("phone_number", "email")
#     ordering = ("-date_joined",)
#     list_filter = ("is_active", "is_staff", "is_verified")
    
#     fieldsets = (
#         (None, {"fields": ("phone_number", "email", "password")}),
#         (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
#         (_("Important dates"), {"fields": ("last_login", "date_joined")}),
#     )

#     add_fieldsets = (
#         (None, {
#             "classes": ("wide",),
#             "fields": ("phone_number", "email", "password1", "password2", "is_active", "is_staff", "is_superuser"),
#         }),
#     )


# @admin.register(UserProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ("user", "first_name", "last_name", "user_type", "gender", "modified_at")
#     search_fields = ("first_name", "last_name", "user__phone_number", "user__email")
#     list_filter = ("user_type", "gender", "modified_at")


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile
from django.utils.translation import gettext_lazy as _

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("phone_number", "email", "is_active", "is_staff", "is_verified", "date_joined")
    search_fields = ("phone_number", "email")
    ordering = ("-date_joined",)
    list_filter = ("is_active", "is_staff", "is_verified")
    
    fieldsets = (
        (None, {"fields": ("phone_number", "email", "password")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone_number", "email", "password1", "password2", "is_active", "is_staff", "is_superuser"),
        }),
    )


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "user_type", "gender", "modified_at")
    search_fields = ("first_name", "last_name", "user__phone_number", "user__email")
    list_filter = ("user_type", "gender", "modified_at")

# Explicit registration
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
