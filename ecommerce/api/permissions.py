from rest_framework import permissions

SAFE_METHODS = ["GET", "HEAD", "OPTIONS"]

SELLER_METHODS = ["POST", "PUT", "PATCH", "DELETE"]


class ProductPermission(permissions.BasePermission):
    """
    Read-only for clients and guests. Post, modify, delete for sellers.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or (
            request.user.groups.filter(name="Sellers").exists() and request.method in SELLER_METHODS
        ):
            return True
        return False


class OrderPermission(permissions.BasePermission):
    """
    Post only for Clients.
    """

    def has_permission(self, request, view):
        if request.user.groups.filter(name="Clients").exists():
            return True
        return False


class SellerPermission(permissions.BasePermission):
    """
    Is Seller
    """

    def has_permission(self, request, view):
        if request.user.groups.filter(name="Seller").exists():
            return True
        return False
