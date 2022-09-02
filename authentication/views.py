from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status,views,generics
from .models import User
from .serializers import RegisterSerializer,getSerializer,EmailVerificationSerializer,LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from .utils import Util
import jwt
from django.conf import settings

#green this issssss verrrrrrrrrrrrrified APi
@api_view(['GET'])
def verified(request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY,algorithms=["HS256"])
            user = User.objects.get(id=payload['user_id'])
            userr=user.username
            if not user.is_verified:
                user.is_verified = True
                user.save()
            html=f'<center> <h1>Hello <mark style="background-color:white; color: MediumSeaGreen;"> {userr} </mark> ,Your Account Has Been Verified </h1>'
            return HttpResponse(html)
        except jwt.ExpiredSignatureError as identifier:
            html=f'<center><h1>This Link Is Expired</h1></center>'
            return HttpResponse(html)
        except jwt.exceptions.DecodeError as identifier:
            html=f'<center><h1>Wrong Link</h1></center>'
            return HttpResponse(html)

#green this issssss Registeeeeeerrrrrrrrr APi
@api_view(['POST'])
def register(request):
    user=request.data
    serializer=RegisterSerializer(data=user)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user_data=serializer.data
    user = User.objects.get(email=user_data['email'])
    token = RefreshToken.for_user(user).access_token
    current_site = get_current_site(request).domain
    relativeLink = reverse('email-verify')
    absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
    email_body = 'Hi '+user.username + \
            ' Use the link below to verify your email \n' + absurl
    data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}
    Util.send_email(data)
         
    return Response({"alert":"Please check your email to verify your account","data":user_data},status=status.HTTP_201_CREATED)



#green this issssss Geeeeeeeeeeeeeeeeeeeeeet APi

@api_view(['GET'])
def geet(request):
    obj=User.objects.all()
    serializer=getSerializer(obj,many=True)
    return Response(serializer.data)


#green this issssss LoooooooooooooooooooooogIn APi
@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)