from django.forms import ValidationError
from rest_framework import serializers,status
from .models import User
import re
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth import authenticate, get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from .utils import Util
from django.contrib.auth import authenticate
from django.db.models import Sum,Count


#green this issssss verrrrrrrrrrrrrified Serializer

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']

#green this issssss Registeeeeeerrrrrrrrr Serializer



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'}

    class Meta:
        model = User
        fields = ['email', 'username', 'password','confirm_password','first_name','last_name','phone_number','address','birthdate','image','experience']

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

    def validate_phone_number(self, value):
        mobile_regex = regex=r'^(09\d{8}|\+963\d{9})$'
        if not re.match(mobile_regex, value):
            errorr= "Invalid mobile number must be in the format 09XXXXXXXX or +963XXXXXXXXX"
            print(errorr)
            raise ValidationError("Invalid mobile number.Must be in the format 09XXXXXXXX or +963XXXXXXXXX")
        return value

    def validate_first_name(self, value):
        if not re.match(r'^[a-zA-Z]+$', value):
            raise serializers.ValidationError('First name must contain only characters')
        return value

    def validate_last_name(self, value):
        if not re.match(r'^[a-zA-Z]+$', value):
            raise serializers.ValidationError('Last name must contain only characters')
        return value



    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        confirm_password = attrs.get('confirm_password', '')
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs

    def create(self, validated_data):
        del validated_data['confirm_password']
        return User.objects.create_user(**validated_data)

#green this issssss Geeeeeeeeeeeeeeeeeeeeeet Serializer

class getSerializer(serializers.ModelSerializer):
    created_at=serializers.DateTimeField(format="%Y-%m-%d- %H:%M")
    updated_at=serializers.DateTimeField(format="%Y-%m-%d- %H:%M")
    image_url = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    number_of_ratings=serializers.SerializerMethodField()
    number_of_reports=serializers.SerializerMethodField()


    def get_image_url(self, obj):
        request = self.context.get('request')
        if request is not None:
            image_url = request.build_absolute_uri(obj.image.url)
            
        else:
            image_url = obj.image.url
        return image_url
    def get_number_of_reports(self, obj):
        result = obj.reports_received.aggregate(count=Count('reason'))
        reports = result.get('count', 0)
        return reports
    
    def get_number_of_ratings(self, obj):
        result = obj.received_ratings.aggregate(count=Count('value'))
        count = result.get('count', 0)
        return count
    def get_average_rating(self, obj):
        result = obj.received_ratings.aggregate(total=Sum('value'), count=Count('value'))
        total = result.get('total', 0)
        count = result.get('count', 0)
        if count == 0:
            return 0
        return round(total / count, 2)
    class Meta:
        model = User
        fields = ['email', 'username','first_name','last_name','phone_number','address','birthdate','image','image_url',\
                  'created_at','updated_at','experience','average_rating','number_of_ratings','number_of_reports']


#green this issssss LoooooooooooooooooooooogIn Serializer

class LoginSerializer(serializers.ModelSerializer):
    email_or_username = serializers.CharField(max_length=255, min_length=3, required=True)
    password = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        email_or_username = obj['email_or_username']

        user = None
        if '@' in email_or_username:
            user = User.objects.filter(email=email_or_username).first()
        else:
            user = User.objects.filter(username=email_or_username).first()

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['email_or_username', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email_or_username = attrs.get('email_or_username', '')
        password = attrs.get('password', '')

        user = authenticate(request=self.context.get('request'),
                            email=email_or_username,
                            password=password)

        if not user:
            user = authenticate(request=self.context.get('request'),
                                username=email_or_username,
                                password=password)

        if not user:
            raise AuthenticationFailed('Wrong Email|Username or Password')

        if not user.is_verified:
            token = RefreshToken.for_user(user).access_token
            relativeLink = reverse('email-verify')
            absurl = 'http://127.0.0.1:8000'+relativeLink+"?token="+str(token)
            email_body = 'Hi '+user.username + \
            ' Use the link below to verify your email \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}
            Util.send_email(data)
            raise AuthenticationFailed('Your Account is not verified yet,plz check your email')

        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')


        return {
            'email_or_username': user.email if user.email else user.username,
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

