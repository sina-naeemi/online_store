from rest_framework import serializers

from .models import User


class user_serializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username" , "phone_number" , "email"]