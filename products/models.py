from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    parent=models.ForeignKey('self', verbose_name="parent" , on_delete=models.CASCADE , null=True , blank=True)
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
    
    def __str__(self):
        return self.title
    

class Product(models.Model):
    PRODUCT_MOVIE=1
    PRODUCT_AUIDO=2
    PRODUCT_FILE=3
    PRODUCT_TYPYE=(
        (PRODUCT_MOVIE , _("movie")),
        (PRODUCT_AUIDO , _("audio")),
        (PRODUCT_FILE ,_("file"))
    )
    # PRODUCT_GENRE=[
    #     ("romance" , _("عاضقانه")),
    #     ("action" , _("اکشن")),
    #     ("drama" , _("درام")),
    #     ("fantesy" , _("فانتزی")),
    #     ()
    # ]


    title=models.CharField(verbose_name=_("title") , max_length=50)
    description=models.TextField(verbose_name=_("description") , blank=True , )
    genre=models.CharField(_("genre"),max_length=50 )
    product_type=models.PositiveSmallIntegerField("produc type" , choices=PRODUCT_TYPYE,default=PRODUCT_MOVIE)
    avatar=models.ImageField(verbose_name=_("picture") ,blank=True,upload_to="products/" )
    is_enable=models.BooleanField(default=False)
    Categories=models.ManyToManyField("Category" , verbose_name=_("categories") , blank=True)
    created_time=models.DateTimeField(verbose_name=_("created_time"),auto_now_add=True)
    updated_time=models.DateTimeField(verbose_name=_("updated_time"),auto_now=True)


    class Meta:
        db_table="products"
        verbose_name=_("product")
        verbose_name_plural=_("products")

    def __str__(self):
        return self.title
    


class File(models.Model):
    product=models.ForeignKey("Product" , verbose_name= "product" , on_delete=models.CASCADE)#related_name <<< استفاده نمود file_set میتوان از این برای تغییر نام 
    title=models.CharField(verbose_name=_("title") , max_length=50)
    file=models.ImageField(verbose_name=_("picture") ,blank=True,upload_to="files/%Y/%m/%d/" )
    is_enable=models.BooleanField(default=False)
    created_time=models.DateTimeField(verbose_name=_("created_time"),auto_now_add=True)
    updated_time=models.DateTimeField(verbose_name=_("updated_time"),auto_now=True)

    def __str__(self):
        return self.title


    class Meta:
        db_table="files"
        verbose_name=_("file")
        verbose_name_plural=_("files")