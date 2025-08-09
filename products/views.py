from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Category , Product , File

from .serializer import productserializer ,fileserializer,categoryserializer

class Listproducts(APIView):
    
    
    def get(self , request):
        products=Product.objects.all()
        serializer=productserializer(products , many=True , context={"request":request})
        return Response(serializer.data)


