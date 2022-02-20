# Django
from django.shortcuts import get_object_or_404
# Django REST Framework
from rest_framework.permissions import BasePermission
# Models
from circles.models import Membership, Circle


class IsCircleAdmin(BasePermission):
    def has_permission(self, request, view):
        circle = get_object_or_404(Circle, slug_name=view.kwargs['slug_name'])
        try:
            Membership.objects.get(user=request.user, circle=circle, is_admin=True,
                                   is_active=True)
        except Membership.DoesNotExist:
            return False
        return True


class IsActiveCircleMember(BasePermission):
    def has_permission(self, request, view):
        circle = get_object_or_404(Circle, slug_name=view.kwargs['slug_name'])
        try:
            Membership.objects.get(user=request.user, circle=circle, is_active=True)
        except Membership.DoesNotExist:
            return False
        return True
