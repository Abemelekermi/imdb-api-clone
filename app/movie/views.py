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

from movie.permissions import IsOwnerOrReadOnly

class MovieViewSet(viewsets.ModelViewSet):
    """View for managing Movie in the databse"""
    serializer_class = serializers.MovieDetailSerializer
    authentication_classes = [TokenAuthentication]
    queryset = Movie.objects.all()
    http_method_names = [
        'get', 'post', 'patch', 'delete', 'head', 'options', 'trace'
    ]

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        """Assign the authenticated user to the movie instance."""
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == 'list':
            return serializers.MovieSerializer
        elif self.action == 'upload_image':
            return serializers.MovieDetailSerializer

        return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to Movie"""
        movie = self.get_object()
        serializer = self.get_serializer(movie, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RatingViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """View for managing rating in the databse"""
    serializer_class = serializers.RatingDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Rating.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.RatingSerializer
        return self.serializer_class

    def get_queryset(self):
        """Return ratings for the authenticated user."""
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
