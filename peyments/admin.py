from django.contrib import admin

from .models import banks_Gate , transaction

@admin.register(banks_Gate)
class Admin_banks_Gate(admin.ModelAdmin):
    list_display=["id","name","description" , "is_enable" , "updated_time"]

@admin.register(transaction)
class Admin_transaction(admin.ModelAdmin):
    list_display=["id",'user', 'package', 'bank_port', 'price', 'status', 'phone_number', 'created_time']
    list_filter=['status', 'bank_port', 'package']
    search_fields=["user" , "phone_number"]
