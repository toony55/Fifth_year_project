from django.urls import path,include
from .views import create_skill,create_certificate,create_service,get_certificates,get_skills,edit_certificate,\
    edit_skill,delete_certificate,delete_Skill,create_sellservice,get_PServices,get_PSellServices,all_services,all_SellServices


urlpatterns = [
    path('create_skill/',create_skill,name="create_skill"),
    path('create_certificate/',create_certificate,name="create_certificate"),
    path('create_service/',create_service,name="create_service"),
    path('create_sellservice/',create_sellservice,name="create_sellservice"),
    path('get_certificates/',get_certificates,name="get_certificates"),
    path('get_skills/',get_skills,name="get_skills"),
    path('edit_certificate/',edit_certificate,name="edit_certificate"),
    path('edit_skill/',edit_skill,name="edit_skill"),
    path('delete_certificate/',delete_certificate,name="delete_certificate"),
    path('delete_Skill/',delete_Skill,name="delete_Skill"),
    path('get_Profile_Services/',get_PServices,name="get_PServices"),
    path('get_Profile_Sell_Services/',get_PSellServices,name="get_PSellServices"),
    path('all_services/',all_services,name="all_services"),
    path('all_SellServices/',all_SellServices,name="all_SellServices"),


]