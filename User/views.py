import random
import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User , User_manager ,Device

from django.core.cache import cache


from drf_spectacular.utils import (extend_schema,extend_schema_view)

class UserRegister(APIView):
    @extend_schema(
        tags=["Authentication"],
        summary="Register user",
        description="Create a new user if needed and send a 5-digit OTP to the user's email."
    )

    def post(self , request):
        phone_number=request.data.get("phone_number" )
        username = request.data.get("username")
        email = request.data.get("email")

        if not email:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data="email is required")
        if not phone_number :
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE , data="phone number is required")
        
        try:
            user=User.objects.get(email=email)
        except User.DoesNotExist:
            user=User.objects.create_user(phone_number=phone_number , username=username , email=email)
            Device.objects.create(for_user=user ,UUID=uuid.uuid4()) 

        #هر گز نام متغیری که برای ذخیره استفاده می کنی را با نام کلاس مدل یکسان نگذار

        code= int(random.randint(10000,99999))

        # میتونی متود رو بدون انتساب به متغیر و فقط با فراخوانی متود پیاده سازی کنی
        cache.set(F"otp_{email}" , code , timeout=2*60) 
        # برای استفاده از حافظه موقت از این دستور(شامل ۳ آرگومان) استفاده میکنیمز

        user.email_sending("کد ورود شما", f"کد تایید شما: {code}")
        return Response(status=status.HTTP_200_OK, data="code sent to your email")
         # send message (email)


 
class GetToken(APIView):
    @extend_schema(
    tags=["Authentication"],
    summary="Verify OTP",
    description="Verify the OTP code and return JWT access and refresh tokens.",
    )
    def post(self , request):    
        # phone_number=request.data.get("phone_number")
        email = request.data.get("email")
        code=request.data.get("code")
        cache_info=cache.get(F"otp_{email}")

        if not email:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data="email is required")
        
        if cache_info is None:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data="code expired or not requested")
        if str(code) != str(cache_info):
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data="code is wrong")
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data="user not found")

        refresh = RefreshToken.for_user(user)
        cache.delete(f"otp_{email}")

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })
        

    


    
