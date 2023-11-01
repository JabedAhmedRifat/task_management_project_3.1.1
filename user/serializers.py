from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth import authenticate

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from django.contrib.auth.tokens import PasswordResetTokenGenerator




class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['user', 'type', 'score', 'image', 'category']

    def get_user(self, obj):
        user = obj.user
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        }




class CreateUserSerializer(serializers.ModelSerializer):
    type = serializers.CharField(write_only=True, default='member')
    
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'username', 'type']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        user_type = validated_data.get('type', 'member')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        UserProfile.objects.create(user=user, type=user_type)
        return user

    
class UserSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='userprofile.type', read_only=True)
    class Meta:
        model = User
        fields = ['id', 'email','username', 'type']


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, data):
        print("Email:", data['email'])
        print("Password:", data['password'])
        user = authenticate(email=data['email'],password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("wrong Credential")
    
    


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("user with this email does not exist")
        
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)
        
        self.user = user
        self.uid = uid
        self.token = token 
        
        return email
    
    
class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    
    def set_new_password(self, uid, token):
        uid = urlsafe_base64_decode(uid)
        token = str(token)
        try:
            user = User.objects.get(pk=uid)
            
            if PasswordResetTokenGenerator().check_token(user,token):
                new_password = self.validated_data['new_password']
                user.set_password(new_password)
                user.save()
                return user
        except User.DoesNotExist:
            pass
        
        return None