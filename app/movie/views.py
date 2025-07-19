from rest_framework import (
    viewsets,
    mixins,
    status
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import (IsAuthenticated,
                                        IsAdminUser)

from core.models import (
    Movie,
)
from movie import serializers

class MovieViewSet(viewsets.ModelViewSet):
    """View for managing"""
    serializer_class = serializers.MovieSerializer
    authentication_classes = [TokenAuthentication]
    queryset = Movie.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
