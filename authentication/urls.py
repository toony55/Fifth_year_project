from django.urls import path
from .views import post,geet,verified


urlpatterns = [
    path('reg/',post,name="register"),
    path('geet/',geet,name="get"),
    path('email-verify/',verified,name="email-verify"),
]
