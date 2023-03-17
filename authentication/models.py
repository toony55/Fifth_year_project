from email.policy import default
from django.db import models

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date



class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None,**other_fields):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username, email=self.normalize_email(email),**other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None,**other_fields):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active  = models.BooleanField(default=True)
    Active  = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    first_name = models.CharField(max_length=30,default="") 
    last_name = models.CharField(max_length=30,default="")
    address = models.TextField(max_length=50,blank=True) 
    phone_number = models.CharField(max_length=13,unique=True)
    birthdate = models.DateField(default=date.today)
    image = models.ImageField(upload_to='images/',default='images/1.png')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name','phone_number','birthdate']
    objects = UserManager()

    
    def __str__(self):
        return f'{self.email} - {self.username}'

    def age(self): 
        today = date.today() 
        age = today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day)) 
        return age

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


