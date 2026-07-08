import random
import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User , User_manager ,Device

from django.core.cache import cache

class UserRegister(APIView):
    def post(self , request):
        phone_number=request.data.get("phone_number" )
        username = request.data.get("username")
        email = request.data.get("email")
        if not phone_number :
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        try:
            user=User.objects.get(phone_number=phone_number)
            return Response("this user already register")
        except User.DoesNotExist:
            user=User.objects.create_user(phone_number=phone_number , username=username , email=email)
            

        Device_pass=Device.objects.create(for_user=user ,UUID=uuid.uuid4()) 
        #هر گز نام متغیری که برای ذخیره استفاده می کنی را با نام کلاس مدل یکسان نگذار

        code= int(random.randint(10000,99999))

        # میتونی متود رو بدون انتساب به متغیر و فقط با فراخوانی متود پیاده سازی کنی
        cache_pass=cache.set(F"otp_{phone_number}" , code , timeout=2*60) 
        # برای استفاده از حافظه موقت از این دستور(شامل ۳ آرگومان) استفاده میکنیمز

        # send message (sms or email)
        return Response({"code":code})

 
class GetToken(APIView):
    def post(self , request):    
        phone_number=request.data.get("phone_number")
        code=request.data.get("code")
        cache_info=cache.get(F"otp_{phone_number}")
        if code != cache_info:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE ,data="code is wrong")
        # u=Device.objects.get(for_user=request.user)
        # if u.UUID==
        ramz=uuid.uuid4()
        return Response({"token":ramz})

    


    
