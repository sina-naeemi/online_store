from rest_framework import serializers

from .models import banks_Gate , transaction


class Serializer_bank_gate(serializers.ModelSerializer):
    class Meta:
        model=banks_Gate
        fields=["id","name", "description" , "avatar"] #برای نشون دادن به کاربر همین قدر اطلاعات کافیه

        
class serilizer_callback(serializers.Serializer):
    token=serializers.CharField()
    status=serializers.IntegerField()



        