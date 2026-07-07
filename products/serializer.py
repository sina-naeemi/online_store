from rest_framework import serializers
from .models import Category , Product , File

class categoryserializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=("id","title" ,"description" , 'is_enable' , "avatar")

    
class Genre_serializer(serializers.ModelSerializer):
    # Categories=categoryserializer(many=True)
    class Meta:
        model=Product
        fields=["id","genre" ]

class fileserializer(serializers.ModelSerializer):
    class Meta:
        model=File
        fields=("id","title" , "file")



class productserializer(serializers.HyperlinkedModelSerializer):
    Categories=categoryserializer(many=True)
    # file_set=fileserializer(many=True)
   
    # Gadid=serializers.SerializerMethodField()
    product_type=serializers.SerializerMethodField() # برای نشان دادن متن های مربوط به نوع محصول ایجاد شده

    class Meta:
        model=Product
        fields=("id","title"  , "avatar" , "Categories" , "product_type" , "url")#file_set , Gadid


    # def get_Gadid(self , obj):
    #     return obj.id
    
    def get_product_type(self , obj):
        return obj.get_product_type_display()


class product_Detail_serializer(serializers.HyperlinkedModelSerializer):
    Categories=categoryserializer(many=True)
    file_set=fileserializer(many=True)
   
    # Gadid=serializers.SerializerMethodField()
    product_type=serializers.SerializerMethodField() # برای نشان دادن متن های مربوط به نوع محصول ایجاد شده

    class Meta:
        model=Product
        fields=("id","title" , "description" , "avatar" , "Categories" , "product_type","file_set" )#file_set , Gadid


    # def get_Gadid(self , obj):
    #     return obj.id
    
    def get_product_type(self , obj):
        return obj.get_product_type_display()



