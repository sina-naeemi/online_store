from django.shortcuts import render

from .serializer import plans_serializer , subscription_serilizer
from .models import plans , subscription

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import (extend_schema,extend_schema_view)

class plans_View(APIView):
    @extend_schema(
    tags=["Subscriptions"],
    summary="Subscription plans",
    description="Return all enabled subscription plans.",
    responses=plans_serializer(many=True),
    )
    def get(self , request):
        all_plans=plans.objects.filter(is_enable=True )
        serializer=plans_serializer(all_plans , many=True)
        return Response(serializer.data)
    
class subscription_View(APIView):
    permission_classes=[IsAuthenticated]
    @extend_schema(
    tags=["Subscriptions"],
    summary="My subscription",
    description="Return the authenticated user's subscriptions.",
    responses=subscription_serilizer(many=True)
    )
    def get(self , request):
        sub=subscription.objects.filter(user=request.user)
        serializer=subscription_serilizer(sub , many=True)
        return Response(serializer.data)
    