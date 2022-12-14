from django.forms import ValidationError
from rest_framework import serializers,status
from .models import User
import re
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from .utils import Util


#green this issssss verrrrrrrrrrrrrified Serializer

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']

#green this issssss Registeeeeeerrrrrrrrr Serializer

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'}

    class Meta:
        model = User
        fields = ['email', 'username', 'password']
    
    def validate_password(self,value):
       if len(value) < 8:
        raise ValidationError(_("Your password must contain at least 8 Characters."))
       elif len(value) > 68:
        raise ValidationError(_("Your password must not exceed 68 Characters."))
       elif re.search('[A-Z]', value)==None:
         raise ValidationError(_("Your password must contain at least 1 uppercase character."))
       elif re.search('[0-9]', value)==None:
         raise ValidationError(_("Your password must contain at least 1 number."))
       elif re.search('[^A-Za-z0-9]', value)==None:
         raise ValidationError(_("Your password must contain at least 1 symbol."))
       else:
            return value
        
        
    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

#green this issssss Geeeeeeeeeeeeeeeeeeeeeet Serializer

class getSerializer(serializers.ModelSerializer):
    created_at=serializers.DateTimeField(format="%Y-%m-%d- %H:%M")
    updated_at=serializers.DateTimeField(format="%Y-%m-%d- %H:%M")
    class Meta:
        model = User
        exclude=['password',]

#green this issssss LoooooooooooooooooooooogIn Serializer

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access'] }
        
    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']


    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = authenticate(email=email, password=password)


        if not user:
            raise AuthenticationFailed('Wrong Email or Password')

        if not user.is_verified:
            token = RefreshToken.for_user(user).access_token
            print(user.email)
            relativeLink = reverse('email-verify')
            absurl = 'http://127.0.0.1:8000'+relativeLink+"?token="+str(token)
            email_body = 'Hi '+user.username + \
            ' Use the link below to verify your email \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}
            Util.send_email(data)
            raise AuthenticationFailed('Your Account is not verified yet,plz check your email')
           
        if not user.Active:
            raise AuthenticationFailed('Account disabled, contact admin')
       

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }

#green this issssss LoooooooooooooooooooooogOut Serializer
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')

