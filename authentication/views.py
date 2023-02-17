from logging import exception
from django.shortcuts import render
from rest_framework import generics, status, views,  permissions
from rest_framework.authentication import TokenAuthentication

from .serializers import *
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import redirect
from rest_framework.views import APIView
from django.http import HttpResponsePermanentRedirect
import os
from rest_framework.authtoken.models import Token
import json
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from uuid import getnode as get_mac
import uuid


# Create your views here.
class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):

        user = request.data
        serializer = self.serializer_class(data=user)
        if serializer.is_valid():
            serializer.save()
        else: 
            return Response({'status':False, 'message':'This email already exists ', 'data':None, 'accessToken': None, 'refreshToken':None },status=status.HTTP_200_OK)
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = Token.objects.create(user = user)
        user33 = auth.authenticate(email= user.email, password= user.password)
        
        
        return Response({'status': True,
                         'message':'email created', 'data':user_data,"accessToken":token.key, 'refreshToken':token.key } , status=status.HTTP_201_CREATED)

class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY , algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        #except jwt.exceptions.DecodeError as identifier:
         #   return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if 'accessTokens' in serializer.data.keys():
        
            return Response({'status':True ,'message':'logged successfully','data':serializer.data}, status= status.HTTP_200_OK)
        else:
            r = serializer.data.get('email')
            return Response({'status':False ,'message': r ,'data':{}}, status= status.HTTP_200_OK)

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'pages:restPassword', kwargs={'uidb64': uidb64, 'token': token})

            absurl = 'http://' + current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                         absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
            return Response({'status':True,'message': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        return Response({'status':False,'message': 'this email is not register'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):


        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error':'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success':True , 'message': 'credentials Valid', 'uidb64':uidb64, 'token':token },status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
                if not PasswordResetTokenGenerator():
                    return Response({'error': 'Token is not valid, please request a new one'},
                                status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({'status':True,'message':'logout done'},status=status.HTTP_200_OK)
        else:
            return Response({'status':False,'message':'invalid refresh token'},status=status.HTTP_200_OK)



