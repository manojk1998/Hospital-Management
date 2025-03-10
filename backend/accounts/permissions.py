from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admin users to access the view.
    """
    
    def has_permission(self, request, view):
        return request.user and (request.user.is_superuser or request.user.is_admin)


class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users to access the view.
    Alias for IsAdmin for consistency with other permission naming.
    """
    
    def has_permission(self, request, view):
        return request.user and (request.user.is_superuser or request.user.is_admin)


class IsStaffUser(permissions.BasePermission):
    """
    Custom permission to only allow staff users to access the view.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_staff_member


class IsClientUser(permissions.BasePermission):
    """
    Custom permission to only allow client users to access the view.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_client


class IsAdminOrSelf(permissions.BasePermission):
    """
    Custom permission to only allow admin users or the user themselves to access their data.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Allow admin users
        if request.user.is_superuser or request.user.is_admin:
            return True
        
        # Allow users to access their own data
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return obj == request.user


class IsAdminOrStaff(permissions.BasePermission):
    """
    Custom permission to only allow admin or staff users to access the view.
    """
    
    def has_permission(self, request, view):
        return request.user and (request.user.is_superuser or request.user.is_admin or request.user.is_staff_member)


class IsAdminOrStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow admin or staff users to perform any action,
    but only allow read-only access to others.
    """
    
    def has_permission(self, request, view):
        # Allow GET, HEAD, OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Allow admin or staff users
        return request.user and (request.user.is_superuser or request.user.is_admin or request.user.is_staff_member) 