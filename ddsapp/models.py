from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager,PermissionsMixin,UserManager)

from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


# class UserManager(BaseUserManager):

#     def create_user(self, username, email, password=None):
#         if username is None:
#             raise TypeError('Users should have a username')
#         if email is None:
#             raise TypeError('Users should have a Email')

#         user = self.model(username=username, email=self.normalize_email(email))
#         user.set_password(password)
#         user.save()
#         return user
        
# def create_superuser(self, username, email, password=None):
#         if password is None:
#             raise TypeError('Password should not be none')

#         user = self.create_user(username, email, password)
#         user.is_superuser = True
#         user.is_staff = True
#         user.save()
#         return user

# class Role(models.Model):
#     user_type=models.CharField(max_length=60)

#     def __str__(self):
#         return self.user_type       

class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects=UserManager()


    def __str__(self):
        return self.email


    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class Movi_Model(models.Model):
    created_by=models.CharField(max_length = 200)
    movi_title = models.CharField(max_length = 200)
    movi_rank = models.CharField(max_length = 200)
    description = models.TextField()
    imd_rating = models.CharField(max_length = 200)
    relese_date = models.DateTimeField(auto_now_add = True)
    
  
    def __str__(self):
        return self.movi_title