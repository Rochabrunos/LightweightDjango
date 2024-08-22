from rest_framework import authentication, permissions, viewsets

from .models import Sprint
from .serializers import SprintSerializer

# ModelViewSet provides the scaffolding needed for CRUD operations
class SprintViewSet(viewsets.ModelViewSet):
    """API endpoint for listing and creating sprints."""

    queryset = Sprint.objects.order_by('end')
    serializer_class = SprintSerializer

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