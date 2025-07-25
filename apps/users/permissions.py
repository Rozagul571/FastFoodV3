from rest_framework.permissions import BasePermission

class RoleBasedPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        allowed_roles = getattr(view, 'allowed_roles', ['admin', 'restaurantManager', 'oshpaz'])
        return request.user.role in allowed_roles

    @classmethod
    def with_roles(cls, roles):
        class RoleBasedPermissionWithRoles(cls):
            allowed_roles = roles
        return RoleBasedPermissionWithRoles

class IsAdminOrRestaurantRole(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ['admin', 'restaurantOwner', 'restaurantManager']

# class IsUser(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated
#
#
# class IsAdmin(BasePermission):
#     def has_permission(self, request, view):
#         return request.user and request.user.is_authenticated and request.user.is_staff