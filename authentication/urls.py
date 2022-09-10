from django.urls import path
from .views import register,geet,verified,login,ResetPasswordView,logout
from rest_framework_simplejwt.views import ( TokenRefreshView)
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('register/',register,name="register"),
    path('get-info/',geet,name="get"),
    path('email-verify/',verified,name="email-verify"),
    path('login/', login, name="login"),
    path('logout/',logout, name="logout"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reset_password/',
   ResetPasswordView.as_view(),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="authentication/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="authentication/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="authentication/password_reset_done.html"), 
        name="password_reset_complete"),
]
