from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status,views,generics,permissions
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import RegisterSerializer,getSerializer,EmailVerificationSerializer,LoginSerializer,LogoutSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from .utils import Util
import jwt
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render,get_object_or_404
from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django.http import QueryDict
from service.models import Block

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
            context = {
                'name': user.username,

            }
            return render(request, 'account_verified.html', context)

        except jwt.ExpiredSignatureError as identifier:
            context = {
                'title': 'Link Expired',
                'message': 'We\'re sorry, but the link you clicked on has expired.',
                'image_url': 'https://i.postimg.cc/jS6fS7v7/error.png'
            }
            return render(request, 'expired_link.html', context)
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
@permission_classes([IsAuthenticated])
def geet(request):
    user_id =request.query_params.get('user_id')
    if user_id:
        user_model = get_user_model()
        profile_user = get_object_or_404(user_model, id=user_id)
        if Block.objects.filter(blocked=request.user, blocker=profile_user).exists():
            return Response({'message':'You do not have permission to access this user\'s information.'},status=status.HTTP_403_FORBIDDEN)
        elif profile_user==request.user:
            serializer = getSerializer(instance=request.user)
            return Response({'data':serializer.data})
        else: 
            is_blocked=Block.objects.filter(blocked=profile_user, blocker=request.user).exists()
            serializer=getSerializer(instance=profile_user)
            return Response({'is_blocked':is_blocked,'data':serializer.data})
    
    else:
        serializer = getSerializer(instance=request.user)
        return Response({'data':serializer.data})


#green this issssss LoooooooooooooooooooooogIn APi
@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



#green this issssss ReseeeeeeeeeeeeeeetPassword APi
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "authentication/password_reset.html"
    email_template_name = "authentication/password_reset_email.html"
    subject_template_name = "authentication/password_reset_subject.txt"
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."





#green this issssss LoooooooooooooooogOut APi
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    
    serializer =LogoutSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(status=status.HTTP_204_NO_CONTENT)



#green this issssss Proooofile-Ediiiiit APi
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def edit_profile(request):
    user = request.user
    mutable_data = QueryDict(mutable=True) 
    mutable_data.update(request.data)
    if 'email' in mutable_data:
        del mutable_data['email']
        return Response({"msg":"you can't update your email"}, status=status.HTTP_400_BAD_REQUEST)
    serializer = RegisterSerializer(instance=user, data=mutable_data, partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({"msg": "Your profile has been updated", "data": serializer.data}, status=status.HTTP_200_OK)
    else:
        errors = serializer.errors
        return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)




#green this issssss Deletiiiiiiingg APi
permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def delete_user(request):
    try:
        user = request.user
        user.delete()
        return Response({"msg":"Your account has been deleted."}, status=status.HTTP_200_OK)
    except user.DoesNotExis:
        return Response({"msg":"User not found."}, status=status.HTTP_404_NOT_FOUND)
