from rest_framework.permissions import BasePermission
from rest_framework import status

class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'OPTIONS', 'HEAD']:
            return True
        elif obj.user == request.user:
            return True
        else:
            return False
