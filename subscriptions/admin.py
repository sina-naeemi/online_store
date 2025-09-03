from django.contrib import admin

from .models import plans , subscription

@admin.register(plans)
class Admin_plane(admin.ModelAdmin):
    list_display=["title","price","is_enable","start_time","duration"]
    list_filter=["title","price"]
    ordering=("sku",)

@admin.register(subscription)
class Admin_subscription(admin.ModelAdmin):
    list_display=["user" , "pack" , 'active_time' ,'expire_time' ]
    readonly_fields = ['active_time']

# admin.site.register(subscription , Admin_subscription)
