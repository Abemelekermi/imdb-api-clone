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
    Rating
)
from movie import serializers

class MovieViewSet(viewsets.ModelViewSet):
    """View for managing Movie in the databse"""
    serializer_class = serializers.MovieSerializer
    authentication_classes = [TokenAuthentication]
    queryset = Movie.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        """Assign the authenticated user to the movie instance."""
        serializer.save(user=self.request.user)

class RatingViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """View for managing rating in the databse"""
    serializer_class = serializers.RatingSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Rating.objects.all()

    def perform_create(self, serializer):
        """Assign the authenticated user to the movie instance."""
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Return ratings for the authenticated user."""
        print("Getting queryset for ratings")
        return self.queryset
