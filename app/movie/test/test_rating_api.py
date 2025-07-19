"""
Test rating API
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from datetime import date

from core.models import(Movie,
                        Rating)

from movie.serializers import (MovieSerializer,
                               RatingSerializer)

RATING_URL = reverse('movie:rating-list')

def detail_url(rating_id):
    """Get detail url"""
    return reverse('movie:rating-detail', args=[rating_id])

def create_user(is_super=False,**params):
    """Create and return user"""
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
    """Create and return a movie"""
    defaults = {
        'title':'Sample movie title',
        'description':'Sample movie description',
        'is_active':False,
        'released_date':date(2014, 12, 2)
    }
    defaults.update(**params)

    return Movie.objects.create(user=user, **defaults)

class PublicAPiTest(TestCase):
    """Test unauthorized API Access"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call the APIs"""
        res = self.client.get(RATING_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateApiTest(TestCase):
    """Test authorized API Access"""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(user=self.user)

    def test_ratings_are_not_limitted_to_user(self):
        """Test anyone can see the rating"""
        user2 = create_user(username='user2', email='user2@example.com')
        Rating.objects.create(user=user2,
                              rating=2.2,
                              description='Test desc')
        Rating.objects.create(user=self.user,
                              rating=2.2,
                              description='Test desc')

        res = self.client.get(RATING_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_update_rating(self):
        """Test updating rating"""
        rating = Rating.objects.create(user=self.user,
                                       rating=1.2,
                                       description='description')
        payload = {'rating':1.3}
        url = detail_url(rating.id)

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        rating.refresh_from_db()
        self.assertEqual(rating.rating, payload['rating'])

    def test_delete_rating_successful(self):
        """Test deleting rating"""
        rating = Rating.objects.create(user=self.user,
                                       rating=1.2,
                                       description='description')

        url = detail_url(rating.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        ratings = Rating.objects.all().filter(user=self.user)
        self.assertEqual(len(ratings), 0)

    def test_delete_rating_unsuccessful(self):
        """Test deleting someone's rating is not allowed"""
        user = create_user(email='user3@example.com', username='user3')
        rating = Rating.objects.create(user=user,
                                       rating=1.2,
                                       description='description')
        url = detail_url(rating.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        ratings = Rating.objects.all().filter(user=user)
        self.assertEqual(len(ratings), 1)
