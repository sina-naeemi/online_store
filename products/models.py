from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Category(models.Model):
    parent=models.ForeignKey("self" , verbose_name=_('main field') , on_delete=models.CASCADE , blank=True , null=True)
    title=models.CharField(_("title"),max_length=50)
    description=models.TextField(verbose_name=_("description") , blank=True , )
    avatar=models.ImageField(verbose_name=_("picture") ,blank=True,upload_to="categories/" )
    is_enable=models.BooleanField(default=False)
    created_time=models.DateTimeField(verbose_name=_("created_time"),auto_now_add=True)
    updated_time=models.DateTimeField(verbose_name=_("updated_time"),auto_now=True)

    class Meta:
        db_table="categories"
        verbose_name=_("category")
        verbose_name_plural=_("categories")
    

class Product(models.Model):
    title=models.CharField(verbose_name=_("title") , max_length=50)
    description=models.TextField(verbose_name=_("description") , blank=True , )
    avatar=models.ImageField(verbose_name=_("picture") ,blank=True,upload_to="products/" )
    is_enable=models.BooleanField(default=False)
    Categories=models.ManyToManyField("Category" , verbose_name=_("categories") , blank=True)
    created_time=models.DateTimeField(verbose_name=_("created_time"),auto_now_add=True)
    updated_time=models.DateTimeField(verbose_name=_("updated_time"),auto_now=True)

    class Meta:
        db_table="products"
        verbose_name=_("product")
        verbose_name_plural=_("products")
    


class File(models.Model):
    product=models.ForeignKey("Product" , verbose_name= "product" , on_delete=models.CASCADE)
    title=models.CharField(verbose_name=_("title") , max_length=50)
    avatar=models.ImageField(verbose_name=_("picture") ,blank=True,upload_to="files/%Y/%m/%d/" )
    is_enable=models.BooleanField(default=False)
    created_time=models.DateTimeField(verbose_name=_("created_time"),auto_now_add=True)
    updated_time=models.DateTimeField(verbose_name=_("updated_time"),auto_now=True)

    class Meta:
        db_table="files"
        verbose_name=_("file")
        verbose_name_plural=_("files")