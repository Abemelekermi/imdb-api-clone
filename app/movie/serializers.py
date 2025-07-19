"""
Serializer for movie APIs
"""
from core.models import Movie
from rest_framework import serializers

class MovieSerializer(serializers.ModelSerializer):
    """Serializer for Movie"""
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'is_active', 'released_date']
        read_only_fields = ['id']