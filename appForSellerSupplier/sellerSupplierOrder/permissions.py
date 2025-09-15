from rest_framework import permissions


class IsResellerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only resellers to create orders.
    Read-only access is allowed for any authenticated user (e.g., to list orders).
    """

    def has_permission(self, request, view):
        # Allow GET, HEAD, or OPTIONS requests for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        # Only allow resellers to create orders
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, "profile")
            and request.user.profile.user_type == "reseller"
        )


class IsOwnerOrAdminOrSupplier(permissions.BasePermission):
    """
    Custom permission to allow a user to see or modify their own object.
    Allows admin or suppliers to also access the object.
    """

    def has_object_permission(self, request, view, obj):
        # Admins and suppliers have full access
        if request.user.is_staff or (
            hasattr(request.user, "profile")
            and request.user.profile.user_type == "supplier"
        ):
            return True

        # The object's owner has permission
        if hasattr(obj, "user"):
            return obj.user == request.user

        # Fallback for other objects
        return False


