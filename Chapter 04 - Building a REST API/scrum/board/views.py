from django.contrib.auth import get_user_model
from rest_framework import authentication, permissions, viewsets

from .models import Sprint, Task
from .serializers import SprintSerializer, TaskSerializer, UserSerializer

User = get_user_model()

class DefaultMixin(object):
    """Default settings for view authentication, permissions, filtering adn pagination"""
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )
    permissions_classes = (
        permissions.IsAuthenticated,
    )
    paginated_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100

# ModelViewSet provides the scaffolding needed for CRUD operations
class SprintViewSet(viewsets.ModelViewSet):
    """API endpoint for listing and creating sprints."""

    queryset = Sprint.objects.order_by('end')
    serializer_class = SprintSerializer

class TaskViewSet(DefaultMixin, viewsets.ModelViewSet):
    """API endpoint for listing and creating tasks."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

# ReadOnlyModelViewSet only exposes the action of lookup for a determined User
class UserViewSet(DefaultMixin, viewsets.ReadOnlyModelViewSet):
    """API endpoint for listing users."""
    # Changes the lookup from using the ID of the user to the username
    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializer
