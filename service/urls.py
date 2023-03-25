from django.urls import path,include
from .views import create_skill,create_certificate,create_service,get_certificates,get_skills,edit_certificate,edit_skill,delete_certificate,delete_Skill


urlpatterns = [
    path('create_skill/',create_skill,name="create_skill"),
    path('create_certificate/',create_certificate,name="create_certificate"),
    path('create_service/',create_service,name="create_service"),
    path('get_certificates/',get_certificates,name="get_certificates"),
    path('get_skills/',get_skills,name="get_skills"),
    path('edit_certificate/',edit_certificate,name="edit_certificate"),
    path('edit_skill/',edit_skill,name="edit_skill"),
    path('delete_certificate/',delete_certificate,name="delete_certificate"),
    path('delete_Skill/',delete_Skill,name="delete_Skill"),


]