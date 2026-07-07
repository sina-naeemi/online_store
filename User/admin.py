from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User , Profile , habitations ,Device
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.admin import UserAdmin



class InlineProfile(admin.TabularInline):
    model=Profile
    fields=["user" , "nickname" , "Gender" , "birthday" , "avatar"]
    extra=0


class AdminUser(UserAdmin):
    fieldsets=(
        (None,{"fields":("username" , "password")}),
        ("personal information",{"fields":("email" , "phone_number" , "first_name" , "last_name")}),
        ("acc info" ,{"fields":("date_joined" , "last_login"  )} ),
        ("permission" , {"fields": ("is_staff","is_active","is_superuser")})
          #این فیلد ها بر اساس فیلدهای کلاس یوز و همچنین فیلد های موجود در کلاس های ارث بری شده آن نوشته شده اند
    )

    add_fieldsets=(
        (None , {"classes":"wide" ,
                    "fields" :("username" , "phone_number" ,"email", "password1" ,"password2")}),
    ) 

    list_display=("username" , "phone_number" , "email" , "last_login" )
    search_fields=("username__iexact" ,"phone_number")
    ordering=("id",)
    list_filter=('is_staff', 'is_superuser')
    inlines=[InlineProfile]

    # را بازنویسی می کنیم search_fields متود مربوط به 
    def get_search_results(self, request, queryset, search_term): # با این بخش از کد ،متود ،قابلیت های سابق سرچش را حفظ می کند
        queryset , may_have_duplicates = super().get_search_results(request, queryset, search_term)
        try:
            search_term_as_int=int(search_term) # در این بخش ، ویژگی جدید به متود سرچ اضافه می شود

        except ValueError:
            pass
        else :
            queryset |= self.model.objects.filter(phone_number=search_term_as_int)
        return queryset , may_have_duplicates
    






admin.site.register(User , AdminUser)
admin.site.register(habitations)
admin.site.unregister(Group)

admin.site.register(Device)