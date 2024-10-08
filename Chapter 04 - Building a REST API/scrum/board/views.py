from django.contrib.auth import get_user_model
from rest_framework import authentication, permissions, viewsets, filters, status
from rest_framework import filters
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from .models import Sprint, Task
from .serializers import SprintSerializer, TaskSerializer, UserSerializer
from .forms import TaskFilter, SprintFilter

User = get_user_model()

class DefaultMixin(object):
    """Default settings for view authentication, permissions, filtering adn pagination"""
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = (
        permissions.IsAuthenticated,
    )
    paginated_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )

# ModelViewSet provides the scaffolding needed for CRUD operations
class SprintViewSet(DefaultMixin, viewsets.ModelViewSet):
    """API endpoint for listing and creating sprints."""

    queryset = Sprint.objects.order_by('end')
    serializer_class = SprintSerializer
    filterset_class = SprintFilter
    # Allow searching on the given list of fields
    search_fields = ('name', 'description',)
    # Make the class orderable in the API /api/sprints/?search=foobar
    ordering_fields = ('end', 'name', )

class TaskViewSet(DefaultMixin, viewsets.ModelViewSet):
    """API endpoint for listing and creating tasks."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_class = TaskFilter
    # Allow searching on the given list of fields
    search_fields = ('name', 'description')
    # Make the class orderable in the API /api/tasks/?search=foobar
    ordering_fields = ('name', 'order', 'started', 'due', 'completed', )

# ReadOnlyModelViewSet only exposes the action of lookup for a determined User
class UserViewSet(DefaultMixin, viewsets.ReadOnlyModelViewSet):
    """API endpoint for listing users."""
    # Changes the lookup from using the ID of the user to the username
    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.order_by(User.USERNAME_FIELD)
    # Allow searching on the given list of fields
    serializer_class = UserSerializer
