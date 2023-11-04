from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from .serializers import *
from knox.models import AuthToken
from knox.auth import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework import generics, permissions
from .models import UserProfile

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics



class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        
        
        type = request.data.get('type', 'member')
        user_type = 'member'
        
        if type == 'superadmin':
            user_type = 'superadmin'
        elif type == 'admin':
            user_type = 'admin'
        

        try:
            user = User.objects.get(email=request.data['email'])
            return Response({'error': 'Email already exists.'})
        except User.DoesNotExist:
            pass

        try:
            user = User.objects.create_user(
                username=request.data['username'],
                email=request.data['email'],
                password=request.data['password'],
            )
            UserProfile.objects.create(
                user=user,
                type=user_type,
                image=request.data.get('image'),  
                category=request.data.get('category'),
            )

            return Response({
                'token': AuthToken.objects.create(user)[1]
            })
        except Exception as e:
            return Response({'error': str(e)})
            
            
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            user = serializer.validated_data
            return Response({
                "user":UserSerializer(user,
                                      context=self.get_serializer_context()).data,
                                      "token":AuthToken.objects.create(user)[1]})
        else:
            return Response(status=status.code)
            
            
class UserAPI(generics.RetrieveAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    def get_object(self):
        return self.request.user 


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def changePasswordView(request):
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        
        if not user.check_password(old_password):
            return Response({'error':'your old password is incorrect'})
        
        user.set_password(new_password)
        user.save()
        return Response({'message':'password change successfully'})
    return Response(serializer.errors)



class ResetPasswordAPI(APIView):
    serializer_class = ResetPasswordSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid():
            user = serializer.user
            email = serializer.validated_data['email']  
            uid = serializer.uid
            token = serializer.token
            
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string("user/reset_password_email.html",{
                'user' : user,
                'domain' : current_site.domain,
                'uid' : uid,
                'token': token,
                
            })
            to_email = email
            email= EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            
            return Response({'message':'password reset email has sent'})
        
        return Response(serializer.errors)
    
        
    
class SetNewPasswordAPI(APIView):
    serializer_class = SetNewPasswordSerializer
    
    def post(self, request, uid, token):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.set_new_password(uid, token)
            if user:
                return Response({'message':'password reset Successfully'})
            return Response({"message":"invalid Token"})
        
        
        
# class ListUsersView(generics.ListAPIView):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer
    
    
@api_view(['GET'])
def ListUsersView(request):
    data = UserProfile.objects.all()
    serializer = UserProfileSerializer(data, many=True) 
    return Response(serializer.data)


@api_view(['GET'])
def detailUsersView(request, pk):
    data = UserProfile.objects.get(id=pk)
    serializer = UserProfileSerializer(data)
    return Response(serializer.data)


@api_view(['POST'])
def updateUserView(request, pk):
    profile = UserProfile.objects.get(id=pk)
    data = request.data
    serializer = UserProfileSerializer(instance = profile, data = data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteUser(request, pk):
    try:
        
        user = User.objects.get(id=pk)
        user.delete()
        return Response({'message':'User deleted successfully'}) 
    
    except User.DoesNotExist:
        return Response({'message':'User does not exist'}) 





#______________________Target___________________

@api_view(['GET'])
def listTarget(reqeust):
    target = Target.objects.all()
    serializer = TargetSerializer(target, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def detailTarget(reqeust, pk):
    data = Target.objects.get(id = pk)
    serializer = TargetSerializer(data)
    return Response(serializer.data)



@api_view(['POST'])
def createTarget(request):
    data = request.data 
    serializer = TargetSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

@api_view(['POST'])
def updateTarget(request, pk):
    target = Target.objects.get(id=pk)
    data = request.data
    serializer = TargetSerializer(instance=target, data=data, partial = True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    

@api_view(['DELETE'])
def deleteTarget(request,pk):
    data = Target.objects.get(id=pk)
    data.delete()
    return Response({'message' : 'DELETED'})




class searchUserOnTarget(generics.ListAPIView):
    queryset = Target.objects.all().order_by('-id')
    serializer_class = TargetSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']
    