from rest_framework import serializers
from .models import Category , Product , File

class categoryserializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=("title" , 'is_enable' , "avatar")


class fileserializer(serializers.ModelSerializer):
    class Meta:
        model=File
        fields=("id","title" , "file")


class productserializer(serializers.HyperlinkedModelSerializer):
    Categories=categoryserializer(many=True)
    file_set=fileserializer(many=True)
   
    Gadid=serializers.SerializerMethodField()
    product_type=serializers.SerializerMethodField() # برای نشان دادن متن های مربوط به نوع محصول ایجاد شده

    class Meta:
        model=Product
        fields=("id","title" , "description" , "avatar" , "Categories" ,"file_set" , "Gadid", "product_type" , "url")


    def get_Gadid(self , obj):
        return obj.id
    
    def get_product_type(self , obj):
        return obj.get_product_type_display()
