"""
Testing user api
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

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


class PublicApiTests(TestCase):
    """Test the public feature of the user API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful"""
        payload = {
            'first_name':'firstname',
            'last_name':'lastname',
            'email':'user@example.com',
            'password':'test123',
            'username':'username',

        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_email_exists_error(self):
        """Test email is already used"""
        payload = {
            'username':'username',
            'email':'user@example.com',
            'password':'test123'
        }
        payload1 = {
            'username':'username1',
            'email':'user@example.com',
            'password':'test123'
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload1)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_username_already_exists(self):
        """Test username is already used"""
        payload = {
            'username':'username',
            'email':'user@example.com',
            'password':'test123'
        }
        payload1 = {
            'username':'username',
            'email':'use1r@example.com',
            'password':'test123'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload1)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_small(self):
        """Test small password is not allowed"""
        payload = {
            'username':'username',
            'email':'user@example.com',
            'password':''
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_successful(self):
        """Test token gets generated for valid credentials"""
        user_details = {
            'username':'username',
            'email':'user@example.com',
            'password':'test123'
        }
        create_user(**user_details)

        payload = {
            'username':user_details['username'],
            'email':user_details['email'],
            'password':user_details['password'],
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_unsuccessful(self):
        """Test token doesn't get generated for unknown user"""
        payload = {
            'username':'username',
            'email':'user@example.com',
            'password':'test123'
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_blank_password(self):
        """Test token doesn't get generated if the password is blank"""
        user_details = {
            'username':'username',
            'email':'user@example.com',
            'password':'test123'
        }
        create_user(**user_details)

        payload = {
            'email':user_details['email'],
            'password':'',
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_authentication_is_required(self):
        """Test authentication is required for users"""
        res = self.client.post(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateApiTests(TestCase):
    """Test the private feature of the API"""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(user=self.user)

    def test_retrive_profile_success(self):
        """Test retriveing profile for logged in user"""

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data,
            {
                'first_name':self.user.first_name,
                'last_name':self.user.last_name,
                'username':self.user.username,
                'email':self.user.email
            })

    def test_post_is_not_allowed(self):
        """Test post is not allowed for me url"""
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_updating_user_profile(self):
        """Test updating user profile for authenticated user"""
        payload = {
            'username':'new username',
            'password':'new pass'
        }

        res = self.client.patch(ME_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(self.user.username, payload['username'])