from .serializers import SkillSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Service,Category,Skill,Certificate
from rest_framework.response import Response
from rest_framework import status





#sky this issssss Registeeeeeerrrrrrrrr APi
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_skill(request):
    serializer = SkillSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)