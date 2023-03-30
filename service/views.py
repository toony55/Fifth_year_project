from .serializers import SkillSerializer,CertificateSerializer,ServiceSerializer,SellServiceSerializer,\
RequestSerializer,SellRequestSerializer,RatingSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Service,Category,Skill,Certificate,SellService,Request,SellRequest,Rating,Block
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Avg,Count






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
        return Response(serializer.data, status=status.HTTP_201_CREATEDHTTP_201)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#sky this issssss SellllServiiiiiice APi
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_sellservice(request):
    data=request.data.copy()
    serializer = SellServiceSerializer(data=data, context={'request': request})
    if serializer.is_valid():
        categories =data.pop('categories', [])
        service = serializer.save(user=request.user)
        for category in categories:
            service.categories.add(category)
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
        service = serializer.save(buyer=request.user)
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



#sky this issssss Profile-service-Get APi
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_PServices(request):
    services = Service.objects.filter(buyer=request.user).order_by('-created_at')
    serializer =ServiceSerializer(services, many=True)
    return Response(serializer.data)
#sky this issssss Profile-sellservice-Get APi
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_PSellServices(request):
    sellservices = SellService.objects.filter(seller=request.user).order_by('-created_at')
    serializer =SellServiceSerializer(sellservices, many=True)
    return Response(serializer.data)




#sky this issssss Filter-service-Get APi
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_services(request):
    category_ids = request.GET.getlist('category_id')
    price = request.GET.get('price')
    min_rating = request.GET.get('min_rating')

    services = Service.objects.all().order_by('-created_at')
    if category_ids:
        categories = Category.objects.filter(pk__in=category_ids)
        services = services.filter(categories__in=categories).distinct()
    if price:
        services = services.filter(price__gte=price)
    if min_rating:
        services = services.annotate(avg_rating=Avg('buyer__received_ratings__value'),count_rating=Count('buyer__received_ratings'))
        services = services.filter(avg_rating__gte=min_rating).order_by('-count_rating')

    blocking_relationships = Block.objects.filter(blocker=request.user)
    blocked_users = [br.blocked for br in blocking_relationships]
    services = services.exclude(buyer__in=blocked_users)
    blocked_by_relationships = Block.objects.filter(blocked=request.user)
    blocked_by_users = [br.blocker for br in blocked_by_relationships]
    services = services.exclude(buyer__in=blocked_by_users)  
    services = services.filter(is_taken=False)
    serializer = ServiceSerializer(services, many=True)

    return Response(serializer.data)



#sky this issssss Filter-Sellservice-Get APi
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_SellServices(request):
    category_ids = request.GET.getlist('category_id')
    price = request.GET.get('price')
    min_rating = request.GET.get('min_rating')

    services = SellService.objects.all().order_by('-created_at')
    if category_ids:
        categories = Category.objects.filter(pk__in=category_ids)
        services = services.filter(categories__in=categories).distinct()
    if price:
        services = services.filter(price__gte=price)
    if min_rating:
        services = services.annotate(avg_rating=Avg('buyer__received_ratings__value'),count_rating=Count('buyer__received_ratings'))
        services = services.filter(avg_rating__gte=min_rating).order_by('-count_rating')

    blocking_relationships = Block.objects.filter(blocker=request.user)
    blocked_users = [br.blocked for br in blocking_relationships]
    services = services.exclude(seller__in=blocked_users)
    blocked_by_relationships = Block.objects.filter(blocked=request.user)
    blocked_by_users = [br.blocker for br in blocked_by_relationships]
    services = services.exclude(seller__in=blocked_by_users)  
    services = services.filter(is_taken=False)
    serializer = SellServiceSerializer(services, many=True)

    return Response(serializer.data)


#sky this issssss Make_Request APi
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_service_request(request):
    data = request.data
    service_id = data.get('service_id')
    try:
        service = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        return Response({'message': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)
        
    buyer = service.buyer
    seller = request.user

    if seller == buyer:
        return Response({'message': 'You cannot buy your own service'}, status=status.HTTP_400_BAD_REQUEST)
    
    if seller.seller_requests.filter(service=service, status=Request.PENDING).exists():
        return Response({'message': 'You already made a request for this service'}, status=status.HTTP_400_BAD_REQUEST)

    if service.is_taken:
        return Response({'message': 'This service is already taken'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = RequestSerializer(data=data)
    if serializer.is_valid():
        serializer.save(buyer=buyer, seller=seller, service=service)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


#sky this issssss Make_sell_Request APi
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_sell_service_request(request):
    data = request.data
    service_id = data.get('service_id')
    print(service_id)
    try:
        service = SellService.objects.get(id=service_id)
        print(service)
    except Service.DoesNotExist:
        return Response({'message': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)
        
    buyer = request.user

    seller = service.seller
    print(seller)

    if seller == buyer:
        return Response({'message': 'You cannot buy your own service'}, status=status.HTTP_400_BAD_REQUEST)
    
    if buyer.buyer_request.filter(service=service, status=Request.PENDING).exists():
        return Response({'message': 'You already made a request for this service'}, status=status.HTTP_400_BAD_REQUEST)

    if service.is_taken:
        return Response({'message': 'This service is already taken'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = SellRequestSerializer(data=data)
    if serializer.is_valid():
        serializer.save(buyer=buyer, seller=seller, service=service)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#sky this issssss get_Requests APi
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_requests(request):
    user = request.user
    
    # Get query parameters from the request URL
    role = request.query_params.get('role')
    status = request.query_params.get('status')

    if role == 'buyer':
        incoming_requests = Request.objects.filter(buyer=user)
    elif role == 'seller':
        incoming_requests = Request.objects.filter(seller=user)
    if status:
        incoming_requests = incoming_requests.filter(status=status)

    serializer = RequestSerializer(incoming_requests, many=True)
    return Response(serializer.data)


#sky this issssss get_Requests APi
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sell_requests(request):
    user = request.user
    
    # Get query parameters from the request URL
    role = request.query_params.get('role')
    status = request.query_params.get('status')

    if role == 'buyer':
        incoming_requests = SellRequest.objects.filter(buyer=user)
    elif role == 'seller':
        incoming_requests = SellRequest.objects.filter(seller=user)
    if status:
        incoming_requests = incoming_requests.filter(status=status)

    serializer = SellRequestSerializer(incoming_requests, many=True)
    return Response(serializer.data)



#sky this issssss Response_Requests APi
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def Response_request(request):
    id = request.data.get('id')
    try:
        request_obj = Request.objects.get(id=id)
    except Request.DoesNotExist:
        return Response({'message': 'Request does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    if request.user != request_obj.service.buyer:
        return Response({'message': 'You are not authorized to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

    if request_obj.status == 'accepted':
        return Response({'message': 'This request has already been accepted.'}, status=status.HTTP_400_BAD_REQUEST)
    elif request_obj.status == 'denied':
        return Response({'message': 'This request has already been denied.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = RequestSerializer(request_obj)
    action = request.data.get('action')
    if action == 'accept':
        request_obj.status = 'accepted'
        request_obj.service.is_taken = True
        request_obj.service.save()
        request_obj.save()
        return Response({'message': 'Request accepted.', 'data': serializer.data}, status=status.HTTP_200_OK)
    elif action == 'deny':
        request_obj.status = 'denied'
        request_obj.save()
        return Response({'message': 'Request denied.', 'data': serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)
    

#sky this issssss Response_Sell_Requests APi
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def Response_Sell_request(request):
    id = request.data.get('id')
    try:
        request_obj = SellRequest.objects.get(id=id)
    except SellRequest.DoesNotExist:
        return Response({'message': 'Request does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    if request.user != request_obj.service.seller:
        return Response({'message': 'You are not authorized to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

    if request_obj.status == 'accepted':
        return Response({'message': 'This request has already been accepted.'}, status=status.HTTP_400_BAD_REQUEST)
    elif request_obj.status == 'denied':
        return Response({'message': 'This request has already been denied.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = SellRequestSerializer(request_obj)
    action = request.data.get('action')
    if action == 'accept':
        request_obj.status = 'accepted'
        request_obj.service.is_taken = True
        request_obj.service.save()
        request_obj.save()
        return Response({'message': 'Request accepted.', 'data': serializer.data}, status=status.HTTP_200_OK)
    elif action == 'deny':
        request_obj.status = 'denied'
        request_obj.save()
        return Response({'message': 'Request denied.', 'data': serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)
    

#sky this issssss Delete_Requests APi
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_service_request(request):
    request_id = request.data.get('id')
    try:
        request_obj = Request.objects.get(id=request_id)
    except Request.DoesNotExist:
        return Response({'message': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)
    seller = request.user
    if seller != request_obj.seller:
        return Response({'message': 'You are not allowed to delete this request'}, status=status.HTTP_403_FORBIDDEN)

    if request_obj.status != 'pending':
        return Response({'message': 'Cannot delete the request as the status is not pending'}, status=status.HTTP_400_BAD_REQUEST)

    request_obj.delete()
    return Response({'message': 'Request deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


#sky this issssss Delete_Requests APi
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_sell_service_request(request):
    request_id = request.data.get('id')
    try:
        request_obj = SellRequest.objects.get(id=request_id)
    except SellRequest.DoesNotExist:
        return Response({'message': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)
    buyer = request.user
    if buyer != request_obj.buyer:
        return Response({'message': 'You are not allowed to delete this request'}, status=status.HTTP_403_FORBIDDEN)

    if request_obj.status != 'pending':
        return Response({'message': 'Cannot delete the request as the status is not pending'}, status=status.HTTP_400_BAD_REQUEST)

    request_obj.delete()
    return Response({'message': 'Request deleted successfully'}, status=status.HTTP_204_NO_CONTENT)





#sky this issssss Ratings APi
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def do_Ratings(request):
    rated_user_id =request.query_params.get('id')
    if request.method == 'GET':
        if request.query_params.get('type')=='incoming':
            ratings=Rating.objects.filter(rated_user=request.user)
        elif request.query_params.get('type')=='outcoming':
            ratings=Rating.objects.filter(rating_user=request.user)
        serializer=RatingSerializer(ratings,many=True)
        return Response({'message': 'Here are you ratings.', 'data': serializer.data}, status=status.HTTP_200_OK)


    elif request.method == 'POST':
        try:
            rated_user=get_user_model().objects.get(id=rated_user_id)
        except:
            return Response({'message': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        rating_user=request.user
        if Rating.objects.filter(rated_user=rated_user, rating_user=rating_user).exists():
            return Response({'message':'You have already rated this user.'},status=status.HTTP_400_BAD_REQUEST)
        serializer=RatingSerializer(data=request.data)
        if serializer.is_valid():
           serializer.save(rated_user=rated_user,rating_user=rating_user)
           return Response({'message': 'your rate has been submitied.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    

#sky this issssss Delete_Ratings APi
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_Ratings(request):
    rating_id =request.query_params.get('id')
    try:
        rate=Rating.objects.get(id=rating_id)
    except Rating.DoesNotExist:
        return Response({'message': 'the Rate does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    if request.user != rate.rating_user:
        return Response({'message': 'you are not allowed to delete the rate'},status=status.HTTP_403_FORBIDDEN)
    rate.delete()
    return Response({'message': 'your Rate has been deleted successfully'},status=status.HTTP_204_NO_CONTENT)

#sky this issssss edit_Ratings APi
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def edit_Ratings(request):
    rating_id =request.query_params.get('id')
    try:
        rate=Rating.objects.get(id=rating_id)
    except Rating.DoesNotExist:
        return Response({'message': 'the Rate does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    if request.user != rate.rating_user:
        return Response({'message': 'you are not allowed to edit the rate'},status=status.HTTP_403_FORBIDDEN)
    serializer = RatingSerializer(instance=rate, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"msg": "Your rate have been updated", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


#sky this issssss block APi
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def block_user(request):
    blocked_id =request.query_params.get('blocked_id')
    user_model=get_user_model()
    user_to_block = get_object_or_404(user_model, id=blocked_id)

    if user_to_block==request.user:
        return Response({'message':'You Cann''ot Block Yourself'},status=status.HTTP_204_NO_CONTENT)
    is_blocked = Block.objects.filter(blocker=request.user, blocked=user_to_block).exists()
    if is_blocked:
        Block.objects.filter(blocker=request.user, blocked=user_to_block).delete()
        return Response({'message': user_to_block.username+' '+'has been unblocked'},status=status.HTTP_204_NO_CONTENT)

    else:
        Block.objects.create(blocker=request.user, blocked=user_to_block)
        return Response({'message':'you have blocked'+' '+user_to_block.username},status=status.HTTP_204_NO_CONTENT)





    
