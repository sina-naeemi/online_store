from django.contrib import admin

from .models import Category,Product,File
# Register your models here.


@admin.register(Category)
class categoryAdmin (admin.ModelAdmin):
    list_display=["title",'is_enable' ,"created_time" , "parent"]
    list_filter=['is_enable' , 'parent']
    search_fields=["title"]



class fileAdmin(admin.StackedInline):
    model=File
    fields=["title" , "is_enable" , "file"]
    extra=0

@admin.register(Product)
class productAdmin(admin.ModelAdmin):
    list_display=["title",'is_enable' ,"created_time"  ]
    list_filter=["is_enable"]
    search_fields=["title"]
    filter_horizontal=["Categories"]
    inlines=[fileAdmin]

