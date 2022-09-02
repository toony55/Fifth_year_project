from django.urls import path
from .views import register,geet,verified,login
from rest_framework_simplejwt.views import ( TokenRefreshView)




urlpatterns = [
    path('register/',register,name="register"),
    path('get-info/',geet,name="get"),
    path('email-verify/',verified,name="email-verify"),
    path('login/', login, name="login"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
