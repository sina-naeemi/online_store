from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status


from .models import Category , Product , File

from .serializer import productserializer ,fileserializer,categoryserializer

class CategoryListView(APIView):

    def get(self , request):
        category=Category.objects.all()
        seilizer=categoryserializer(category , many=True , context={"request":request})
        return Response(seilizer.data)
    

class CategoryDetailView(APIView):
    
    def get(self , request , pk):
        try:
            category=Category.objects.get(pk=pk)
        except category.DoseNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serilizer=categoryserializer(category , context={"request":request})
        return Response(serilizer.data)

class Listproducts(APIView):
    
    
    def get(self , request):
        products=Product.objects.all()
        serializer=productserializer(products , many=True , context={"request":request}) 
        return Response(serializer.data)
    
class Detailproduct(APIView):

    def get(self ,request, pk):
        try:
            product=Product.objects.get(pk=pk)
        except product.DoseNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer=productserializer(product , context={"request":request})
        return Response(serializer.data)



class FileListView(APIView):
    
    def get(self , request , product_id ) :
        file=File.objects.filter(product_id=product_id)
        serializer=fileserializer(file , many=True , context={"request":request})
        return Response(serializer.data)
    


class FileDetailView(APIView):
    
    def get(self , request , product_id , pk):
        try:
            file=File.objects.get(product_id=product_id , pk=pk)
        except file.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer=fileserializer(file ,context={"request":request} )
        return Response(serializer.data)
