from django.urls import path,include
from .views import create_skill,create_certificate,create_service


urlpatterns = [
    path('create_skill/',create_skill,name="create_skill"),
    path('create_certificate/',create_certificate,name="create_certificate"),
    path('create_service/',create_service,name="create_service"),


]