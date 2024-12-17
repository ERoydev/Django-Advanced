from django.contrib.auth import get_user_model
from rest_framework import serializers


UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    # write_only => is not returned in response
    # read_only => i cannot send it like a data

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password']

    # UserModel.objects.create(**credentials)   I override to avoid this because i need to hash my password with
    # UserModel.objects.create_user(**credentials) build-it create function that hashes my password
    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        # we do this in order to hash the password

        return user

"""
    I do the Login in two serializers (request, response);
        for the swagger documentation that way in swagger i can get more
        precise data about each action.
"""
class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    # accessToken, refreshToken


class LoginResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    message = serializers.CharField()


# The idea is on the logout to delete the refresh token and put it in the blacklist for security purposes
class LogoutRequestSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class LogoutResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
