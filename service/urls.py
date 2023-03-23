from django.urls import path,include
from .views import create_skill


urlpatterns = [
    path('create_skill/',create_skill,name="create_skill"),

]