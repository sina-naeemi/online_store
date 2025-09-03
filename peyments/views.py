import uuid
from django.shortcuts import render , redirect

from .models import banks_Gate , transaction
from .serializer import Serializer_bank_gate
from subscriptions.models import plans ,subscription

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.utils import timezone
from datetime import timedelta

import requests




class  bank_gate_view(APIView):

    def get(self , request):
        all_gate=banks_Gate.objects.filter(is_enable=True)
        serializer=Serializer_bank_gate(all_gate , many=True)
        return Response(serializer.data)
    
class payment(APIView):
    permission_classes=[IsAuthenticated]

    def get(self , request):
        bank_port_id=request.query_params.get("port")
        pack_id=request.query_params.get("package")
        
        try :
            pack=plans.objects.get(pk=pack_id , is_enable=True)
            port=banks_Gate.objects.get(pk=bank_port_id ,is_enable=True )
        except (plans.DoesNotExist or banks_Gate.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        obj=transaction.objects.create(
            user=request.user,
            package=pack,
            bank_port=port,
            status=0 ,
            price=pack.price,
            phone_number=request.user.phone_number,
            token=str(uuid.uuid4())
            )
        #return redirect()
        return Response(data={"token":obj.token , 'bank gate url':"" })#هم میتوان اضافه نمود call back url 
    def post(self , request):
        tk=request.data.get("token")
        st=request.data.get("status")
        try:
            obj=transaction.objects.get(token=tk)
        except obj.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if st != 10:
            obj.status=obj.STATUS_CANCELLED
            obj.save
            return Response(data="payment get cancelled"    ,status=status.HTTP_406_NOT_ACCEPTABLE)
        verify=requests.post("bank_verify_url" , data={}) #این بخش نیاز به یادگیری دارد
        if verify.status_code // 100 !=2: #این خط کد ، رقم صدگان کد وضعیت گرفته شده را نشان میددهد
            obj.status=obj.STATUS_FAIL
            obj.save
            return Response (data="the transaction failed",status=status.HTTP_400_BAD_REQUEST)
        obj.status=obj.STATUS_PAID
        obj.save()

        subscription.objects.create(
            user=obj.user,
            pack=obj.package,
            expire_time=timezone.now() + timedelta(days=obj.package.duration)
        )
        return Response (data="payment is sucsessful")
    

        
    

        
        



