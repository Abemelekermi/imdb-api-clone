"""
Serializer for movie APIs
"""
from core.models import (Movie,
                         Rating)
from rest_framework import serializers

class RatingSerializer(serializers.ModelSerializer):
    """Serializer for rating"""
    class Meta:
        model = Rating
        fields = ['id', 'rating', 'description']
        read_only_fields = ['id']

class MovieSerializer(serializers.ModelSerializer):
    """Serializer for Movie"""
    rating = RatingSerializer(many=True, required=False)
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'is_active', 'released_date', 'rating']
        read_only_fields = ['id']

