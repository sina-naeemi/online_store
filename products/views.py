from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status

from rest_framework.permissions import IsAuthenticated 


from .models import Category , Product , File

from .serializer import (productserializer ,fileserializer,categoryserializer ,
                          product_Detail_serializer , Genre_serializer)#category_Detail_serializer

from subscriptions.models import subscription
class CategoryListView(APIView):

    def get(self , request):
        category=Category.objects.all()
        seilizer=categoryserializer(category , many=True , context={"request":request})
        return Response(seilizer.data)
    

class AllGenre(APIView):
    
    def get(self , request , pk):
        try:
            subject=Product.objects.filter(Categories__id=pk)

        except Category.DoesNotExist:
            return Response(data="این کتگوری وجود نداره",status=status.HTTP_404_NOT_FOUND)
        
        serilizer=Genre_serializer(subject , many=True,context={"request":request})
        return Response(serilizer.data)

class Listproducts(APIView):
    # permission_classes=[IsAuthenticated]
    
    
    
    def get(self , request):
        products=Product.objects.all()
        serializer=productserializer(products , many=True , context={"request":request})           
        # print(request.user)
        # print(request.auth)
        return Response(serializer.data)
    
class Detailproduct(APIView):
    # permission_classes=[IsAuthenticated]

    def get(self ,request, pk):
        # if not subscription.objects.filter(user=request.user).exists:
        #     return Response(data="you dont have subscription to access this data" , status=status.HTTP_406_NOT_ACCEPTABLE)
        try:
            product=Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer=product_Detail_serializer(product , context={"request":request})
        return Response(serializer.data)
    
class ProductByGenre(APIView):
    
    def get(seld , request , genre_name):
        products = Product.objects.filter(genre=genre_name)
        if not products.exists():
            return Response({"error": "No products found for this category"},status=status.HTTP_404_NOT_FOUND)
        serializer = productserializer(products, many=True, context={"request": request})
        return Response(serializer.data)
class ProductByCategory(APIView):

    def get(self, request , category_id):
        product=Product.objects.filter(Categories__id=category_id)
        
        if not product.exists():
            return Response({"error": "No products found for this category"},status=status.HTTP_404_NOT_FOUND)
        
        serializer = productserializer(product, many=True, context={"request": request})
        return Response(serializer.data)




class FileListView(APIView):
    # permission_classes=[IsAuthenticated]
    
    def get(self , request , product_id ) :
        # if not subscription.objects.filter(user=request.user).exists:
        #     return Response(data="you dont have subscription to access this data" , status=status.HTTP_406_NOT_ACCEPTABLE)
        file=File.objects.filter(product_id=product_id)
        serializer=fileserializer(file , many=True , context={"request":request})
        return Response(serializer.data)
    
class FileDetailView(APIView):
    
    def get(self , request , product_id , pk):
        try:
            file=File.objects.get(product_id=product_id , pk=pk)
        except File.DoesNotExist:
            return Response(data="not found",status=status.HTTP_404_NOT_FOUND)
        
        serializer=fileserializer(file ,context={"request":request} )
        return Response(serializer.data)
