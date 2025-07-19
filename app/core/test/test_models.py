"""
Testing models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

from datetime import date

def create_user(is_super=False,
                user_name='username',
                email='user@example.com',
                password='test123'):
    details = {
        'username':user_name,
        'email':email,
        'password':password
    }
    if is_super:
        return get_user_model().objects.create_superuser(**details)
    else:
        return get_user_model().objects.create_user(**details)


class ModelTests(TestCase):
    def test_create_user_successful(self):
        """Test creating a user is successful"""
        email = 'user@example.com'
        password = 'test123'
        user = create_user()

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_without_username_error(self):
        """Test creating user without username results error"""
        with self.assertRaises(ValueError):
            create_user( user_name='')

    def test_create_user_without_email_error(self):
        """Test creating user without email results error"""
        with self.assertRaises(ValueError):
            create_user(email='')


    def test_create_user_without_password_error(self):
        """Test creating user without email results error"""
        with self.assertRaises(ValueError):
            create_user(password='')

    def test_create_super_user(self):
        """Test creating a super user"""
        user = create_user(is_super=True)

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_movie_successful(self):
        """Test creating a movie is successful"""
        user = create_user(is_super=True)

        movie = models.Movie.objects.create(
            user=user,
            title = 'Test title',
            description='Test description',
            is_active = True,
            released_date =date(2025, 10, 6)
        )

        self.assertEqual(str(movie), movie.title)

