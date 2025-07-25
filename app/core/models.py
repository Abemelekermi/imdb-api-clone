from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

import os
import uuid
def movie_image_file_path(instance, filename):
    """Generate file path for the movie image"""
    ext = os.path.split(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'movie', filename)

class UserManager(BaseUserManager):
    """Manages user in the system"""
    def create_user(self, username, email, password=None, **extra_fields):
        """Create user in the system"""
        if not username:
            raise ValueError("Username must be provided")
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError("Password must be Provided")

        email = self.normalize_email(email)
        user = self.model(username=username,
                          email=email,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """Create super user in the system"""
        user = self.create_user(username, email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """Users in the system"""
    username = models.CharField(max_length=255, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    email = models.CharField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active =  models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name','email']
class Movie(models.Model):
    """Movie model"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    released_date = models.DateField()
    ratings = models.ManyToManyField('Rating')
    image = models.ImageField(null=True, upload_to=movie_image_file_path)
    def __str__(self):
        return self.title

class Rating(models.Model):
    """Rating model"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description
