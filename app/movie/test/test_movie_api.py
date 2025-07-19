"""
Test for Movie APIs
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from datetime import date

from core.models import(Movie)

from movie.serializers import (MovieSerializer)

MOVIES_URL = reverse('movie:movie-list')

def create_user(is_super=False,**params):
    details = {
        'username':'username',
        'email':'user@example.com',
        'password':'test123'
    }
    details.update(**params)
    if is_super:
        return get_user_model().objects.create_superuser(**details)
    else:
        return get_user_model().objects.create_user(**details)

def create_movie(user, **params):
    defaults = {
        'title':'Sample movie title',
        'description':'Sample movie description',
        'is_active':False,
        'released_date':date(2014, 12, 2)
    }
    defaults.update(**params)

    return Movie.objects.create(user=user, **defaults)

class PublicMovieApiTests(TestCase):
    """Test unauthenticated API requests"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call the API"""
        res = self.client.get(MOVIES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateMovieApiTests(TestCase):
    """Test Authenticated API requests"""
    def setUp(self):
        self.client = APIClient()
        self.regular_user = create_user(username='regular', email='regular@example.com', is_super=False)
        self.admin_user = create_user(username='admin', email='admin@example.com', is_super=True)

    def test_retrive_movies(self):
        self.client.force_authenticate(self.regular_user)
        """Test retriving list of movies"""

        payload = {
            'title':'Sample movie title',
            'description':'Sample movie description',
            'is_active':False,
            'released_date':date(2014, 12, 2)
        }


        res = self.client.put(MOVIES_URL, payload)

        movies = Movie.objects.all()

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_movie_successful(self):
        """Test admin creating a movie"""
