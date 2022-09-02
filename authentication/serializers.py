
from django.forms import ValidationError
from rest_framework import serializers
from .models import User
import re
from django.utils.translation import gettext_lazy as _



class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']

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
        
        
    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class getSerializer(serializers.ModelSerializer):
    created_at=serializers.DateTimeField(format="%Y-%m-%d- %H:%M")
    updated_at=serializers.DateTimeField(format="%Y-%m-%d- %H:%M")
    class Meta:
        model = User
        fields = '__all__'



