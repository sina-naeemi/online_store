from django.shortcuts import render

from .serializer import plans_serializer , subscription_serilizer
from .models import plans , subscription

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class plans_View(APIView):
    def get(self , request):
        all_plans=plans.objects.filter(is_enable=True )
        serializer=plans_serializer(all_plans , many=True)
        return Response(serializer.data)
    
class subscription_View(APIView):
    permission_classes=[IsAuthenticated]
    def get(self , request):
        sub=subscription.objects.filter(user=request.user)
        serializer=subscription_serilizer(sub , many=True)
        return Response(serializer.data)
    