from rest_framework import permissions

class IsAdminOrSupplier(permissions.BasePermission):
    """
    Allow only admins or suppliers to update status
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Admin check
        if request.user.is_staff or request.user.is_superuser:
            return True

        # Supplier check
        try:
            return request.user.profile.user_type == "supplier"
        except AttributeError:
            return False




from rest_framework import permissions

class IsAdminOrSeller(permissions.BasePermission):
    """
    Allow only admins or suppliers to update status
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Admin check
        if request.user.is_staff or request.user.is_superuser:
            return True

        # Supplier check
        # try:
        #     return request.user.profile.user_type == "supplier"
        # except AttributeError:
        #     return False

        #  Supplier or reseller check
        try:
            return request.user.profile.user_type in ["supplier", "reseller"]
        except AttributeError:
            return False







from rest_framework import permissions

class IsSupplierOwner(permissions.BasePermission):
    """
    Allow access only to the supplier who owns the product.
    """
    def has_object_permission(self, request, view, obj):
        # Ensure user is authenticated and is a supplier
        if not request.user.is_authenticated:
            return False
        if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'supplier':
            return False
        # Only allow editing if the variant belongs to a product of this supplier
        return obj.product.user == request.user

