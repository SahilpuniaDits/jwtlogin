from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from rest_framework import status
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    ChangePasswordSerializer
    # UserListSerializer
)
import jwt
from .models import User


class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }

            return Response(response, status=status_code)
class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'email': serializer.data['email'],
                    # 'role': serializer.data['role']
                }
            }

            return Response(response, status=status_code)


class idView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        decode = jwt.decode(serializer.data['access'], options={
                            "verify_signature": False})
        print(">>>>>>>>>>>>>>>>>", decode)
        id = decode.get("user_id")

        if valid:
            status_code = status.HTTP_200_OK

            response = {
               'id':id,
                }
            

            return Response(response, status=status_code)

# change password 
class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    permission_classes = (AllowAny, )

    # def put(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #     valid = serializer.is_valid(raise_exception=True)
    #     decode = jwt.decode(serializer.data['access'], options={
    #                         "verify_signature": False})
    #     print(">>>>>>>>>>>>>>>>>", decode)
    #     id = decode.get("user_id")
    #     if valid:
    #         status_code = status.HTTP_200_OK

    #         response = {
    #            'id':id,
    #             }
          
    #         return Response(response, status=status_code)
    
    


     # try:
        # acces = Serializer.data['access'] 
        # print("hellooooooo<<<<<<<<<<<<<<<<<<<<<<",acces)
        # jwt.decode(acces, "SECRET_KEY", algorithms=["HS256"])
        # decodedPayload = jwt.decode(token,None,None) 
    # except Exception as e:
    #     import traceback
    #     print("<<<<<", traceback.format_exc())
    #     print(">>>>>>>excption", e)                