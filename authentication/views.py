from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import UserSerializer
from django.contrib.auth.models import User


class AuthenticationViewSet(ViewSet):

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={
            201: openapi.Response('User is successfully created'),
            400: openapi.Response('Bad request'),
            404: openapi.Response('Not found'),
        },
    )
    def register(self, request, *args, **kwargs):
        username = request.data.get('username')
        if username is None:
            return Response("Username is required", status=status.HTTP_404_NOT_FOUND)

        first_name = request.data.get("first_name")
        if first_name is None:
            return Response("Please provide your first name", status=status.HTTP_404_NOT_FOUND)

        last_name = request.data.get("last_name")
        if last_name is None:
            return Response("Please provide your last name", status=status.HTTP_404_NOT_FOUND)

        email = request.data.get("email")
        if email is None:
            return Response("Please provide your email", status=status.HTTP_404_NOT_FOUND)

        password = request.data.get("password")
        if password is None:
            return Response("Please provide your password", status=status.HTTP_404_NOT_FOUND)

        user = User.objects.filter(email=email).first()
        if user is not None:
            return Response({"error": "This username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        hashed_password = make_password(password)
        new_user = User.objects.create(username=username, first_name=first_name, last_name=last_name,
                                       password=hashed_password, email=email)
        new_user.save()

        return Response({"message": "User is successfully created"}, status=status.HTTP_201_CREATED)
