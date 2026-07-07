from rest_framework import serializers

from .models import plans , subscription

from User.serializer import user_serializer
class plans_serializer(serializers.ModelSerializer):
    class Meta:
        model=plans
        fields=["id","title" , "avatar" , "discreaption" , "price" , "duration"]


class subscription_serilizer(serializers.ModelSerializer):
    pack=plans_serializer()
    user=user_serializer()
    class Meta:

        model=subscription
        fields=["user","pack" ,"active_time" ,"expire_time"]
