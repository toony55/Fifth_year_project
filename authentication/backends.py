from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class CustomAuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(email=email))
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None