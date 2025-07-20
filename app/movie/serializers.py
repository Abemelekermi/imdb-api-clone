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
        fields = ['id', 'rating']
        read_only_fields = ['id']

class RatingDetailSerializer(RatingSerializer):
    """Serializer for rating detail view"""
    class Meta(RatingSerializer.Meta):
        fields = RatingSerializer.Meta.fields + ['description']

class MovieSerializer(serializers.ModelSerializer):
    """Serializer for Movie"""
    ratings = RatingSerializer(many=True, required=False)
    class Meta:
        model = Movie
        fields = ['id', 'title', 'is_active', 'released_date', 'ratings']
        read_only_fields = ['id']
    def create(self, validated_data):
        ratings_data = validated_data.pop('ratings', [])
        movie = Movie.objects.create(**validated_data)

        for rating_data in ratings_data:
            rating = Rating.objects.create(user=self.context['request'].user, **rating_data)
            movie.ratings.add(rating)

        return movie


class MovieDetailSerializer(MovieSerializer):
    """Serializer for movie detail view"""
    class Meta(MovieSerializer.Meta):
        fields = MovieSerializer.Meta.fields + ['description', 'image']

class MovieImageSerializer(serializers.ModelSerializer):
    """Serializers for uploading image to the movies"""

    class Meta:
        model = Movie
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image':{'required': 'True'}}