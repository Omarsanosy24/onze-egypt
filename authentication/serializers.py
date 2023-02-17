from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from .models import User
from django_session_jwt.middleware.session import SessionMiddleware
from django.contrib import auth
import json
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from uuid import getnode as get_mac
from rest_framework import status
from rest_framework.authtoken.models import Token
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'phone','year', 'device' ]

    def validate(self, attrs):
        email = attrs.get('email', '')

        

        

        return attrs

    def create(self, validated_data):

        return User.objects.create_user(**validated_data)

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=5555555555555555555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email= serializers.EmailField(max_length=2000, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=2000, min_length=3, read_only=True)
    accessTokens = serializers.CharField(max_length=200000, min_length=6, read_only=True)
    refreshTokens = serializers.CharField(max_length=200000, min_length=6, read_only=True)
    mac = serializers.CharField(max_length = 200, write_only = True)
    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'accessTokens', 'id','refreshTokens', 'mac']

    def validate(self, attrs):
        email=attrs.get('email','')
        password=attrs.get('password','')
        try:
            user = auth.authenticate(email= email, password= password)
            tt , token = Token.objects.get_or_create(user = user)
            if not user:
                if not User.objects.filter(email = email).exists():
                   return {
                        'email':"you are not register",
                        'username': "user.username",
                
                    } 
                return {
                'email':" your password is incorrect",
                'username': "user.username",
                
            }
            mac = attrs.get('mac')
            if user.device == None:
                user.device = mac
                user.save()
            if user.device != mac:
                return {
                'email':"you can't login use this email",
                'username': "user.username",
                
            }

            if not user.is_verified:
                return {
                'email':"you can't login use this email",
                'username': "user.username",
                
            }


            if not user.is_active:
                return {
                'email':"your email is closed, call the owner",
                'username': "user.username",
                
            }

            return {
                'email':user.email,
                'username': user.username,
                'accessTokens':tt.key,
                'refreshTokens':tt.key,
            }
            return super().validate(attrs)

        except:
            
            if not user:
                raise AuthenticationFailed({'status':False, "message":'Invalid credentials, try again', 'data': {} })
            tt , token = Token.objects.get_or_create(user = user)
            
            mac = attrs.get('mac')
            if user.device == None:
                user.device = mac
                print (user.device)
                user.save()
                print(user.device)
            if user.device != mac:
                raise AuthenticationFailed({'status':False, "message":'you can not login use this phone', 'data': {}})

            if not user.is_verified:
                raise AuthenticationFailed({'status':False, "message":'you can not login use this email', 'data': {}})


            if not user.is_active:
                raise AuthenticationFailed({'status':False, "message":'this account is closed','data': {}})
            return {
                'email':user.email,
                'username': user.username,
                'accessTokens':tt.key,
                'refreshTokens':tt.key,
            }
            return super().validate(attrs)


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)


    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')
        

