from rest_framework import serializers

from .models import User


class user_serializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username" , "phone_number" , "email"]

class requestOTPserializer(serializers.Serializer):
    email = serializers.EmailField()
    phone_number = serializers.IntegerField()
    username = serializers.CharField(required=False)


class verifyOTPserializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.IntegerField()