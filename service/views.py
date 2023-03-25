from .serializers import SkillSerializer,CertificateSerializer,ServiceSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Service,Category,Skill,Certificate
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model 






#sky this issssss Skiiiiiiiiiiiil APi
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_skill(request):
    serializer = SkillSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#sky this issssss Certificateeeee APi
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_certificate(request):
    serializer = CertificateSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#sky this issssss Serviiiiiice APi
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_service(request):
    data=request.data.copy()
    serializer = ServiceSerializer(data=data, context={'request': request})
    if serializer.is_valid():
        categories =data.pop('categories', [])
        service = serializer.save(user=request.user)
        for category in categories:
            service.categories.add(category)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#sky this issssss Certificate-Get APi
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_certificates(request):
    user=get_user_model()
    user_id = request.query_params.get('user_id')
    if user_id:
        user = get_object_or_404(user, id=user_id)
        certificates = Certificate.objects.filter(user=user)
    else:
        certificates = Certificate.objects.filter(user=request.user)
    serializer = CertificateSerializer(certificates, many=True)
    return Response(serializer.data)



#sky this issssss Skills-Get APi
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_skills(request):
    user=get_user_model()
    user_id = request.query_params.get('user_id')
    if user_id:
        user = get_object_or_404(user, id=user_id)
        skills = Skill.objects.filter(user=user)
    else:
        skills = Skill.objects.filter(user=request.user)
    serializer = SkillSerializer(skills, many=True)
    return Response(serializer.data)



#sky this issssss Certificate-Ediiiiit APi
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def edit_certificate(request):
    certificate_id = request.query_params.get('certificate_id')
    user = request.user
    certificate = get_object_or_404(Certificate, id=certificate_id, user=user)
    serializer = CertificateSerializer(instance=certificate, data=request.data, context={'request': request}, partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({"msg": "Your Certificates have been updated", "data": serializer.data}, status=status.HTTP_200_OK)
    else:
        errors = serializer.errors
        return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)




#sky this issssss Skiiiil-Ediiiiit APi
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def edit_skill(request,):
    skill_id = request.query_params.get('skill_id')
    user = request.user
    certificate=get_object_or_404(Skill,id=skill_id,user=user)
    serializer = SkillSerializer(instance=certificate, data=request.data,context={'request': request}, partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({"msg": "Your Skills have been updated", "data": serializer.data}, status=status.HTTP_200_OK)
    else:
        errors = serializer.errors
        return Response({"error": errors}, status=status.HTTP_400_BAD_REQUEST)


#sky this issssss Certificate-Deleeeete APi
@api_view(['DELETE'])
def delete_certificate(request):
    certificate_id = request.query_params.get('certificate_id')
    try:
        certificate = Certificate.objects.get(id=certificate_id, user=request.user)
    except Certificate.DoesNotExist:
        return Response({'error': 'Certificate not found'}, status=status.HTTP_404_NOT_FOUND)
    
    certificate.delete()
    
    return Response({'msg': 'Certificate has been deleted'}, status=status.HTTP_204_NO_CONTENT)




#sky this issssss Skill-Deleeeete APi
@api_view(['DELETE'])
def delete_Skill(request):
    skill_id = request.query_params.get('skill_id')
    try:
        skill = Skill.objects.get(id=skill_id, user=request.user)
    except Skill.DoesNotExist:
        return Response({'error': 'Skill not found'}, status=status.HTTP_404_NOT_FOUND)
    
    skill.delete()
    
    return Response({'msg': 'Skill has been deleted'}, status=status.HTTP_204_NO_CONTENT)



