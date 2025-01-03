from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer

@api_view(['POST'])
def login(request):
    return Response({})


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        user = User.objects.get(username=request.data['username'])
        # I make sure my password is hashed
        user.set_password(request.data['password'])
        user.save()

        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def test_token(request):
    return Response({})