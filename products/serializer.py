from rest_framework import serializers
from .models import Category , Product , File

class categoryserializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=("title" , 'is_enable' , "avatar")

class productserializer(serializers.ModelSerializer):
    Categories=categoryserializer(many=True)

    class Meta:
        model=Product
        fields=("title" , "description" , "avatar" , "Categories")

class fileserializer(serializers.ModelSerializer):
    class Meta:
        model=File
        fields=("title" , "file")


