import random
import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User , User_manager ,Device

from django.core.cache import cache


from drf_spectacular.utils import (extend_schema,extend_schema_view)

from .serializer import requestOTPserializer , verifyOTPserializer

class UserRegister(APIView):
    @extend_schema(
        tags=["Authentication"],
        summary="Register user",
        description="Create a new user if needed and send a 5-digit OTP to the user's email.",
        request=requestOTPserializer,
    )

    def post(self , request):
        serilalizer=requestOTPserializer(data=request.data)
        serilalizer.is_valid(raise_exception=True)#اگه داده ها معتبر نبودند خودکار ارور 400 برمیگردونه raise_exception=True با

        phone_number=serilalizer._validated_data["phone_number"]
        username = serilalizer.validated_data["username"]
        email =serilalizer.validated_data["email"]

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
    request=verifyOTPserializer
    )
    def post(self , request):    
        serializer=verifyOTPserializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code=serializer.validated_data["code"]

        cache_info=cache.get(F"otp_{email}")

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
        

    


    
