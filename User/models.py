import random

from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin, BaseUserManager, send_mail 

from django.utils.translation import gettext_lazy as _

from django.utils import timezone
from django.core import validators


class User_manager(BaseUserManager):
    use_in_migrations = True
    
    def _create_user(self ,username , email , phone_number, password,is_staff , is_superuser  ,  **extra_fields): #ترتیبی در قرار دادن پارامتر ها وجود ندارد
        if not username:
             raise ValueError("username is necessary")
        email=self.normalize_email(email)
        user=self.model(username=username, email=email , phone_number=phone_number , password=password , is_superuser=is_superuser
                        , is_staff=is_staff , is_active=True , date_joined=timezone.now() , **extra_fields)
        
        if not extra_fields.get("no_password"):
            user.set_password(password)

        user.save(using=self._db)
        return user
    def create_user(self ,username=None , email=None , phone_number=None , password=None,is_staff=None , is_superuser=None  ,  **extra_fields):
        if not username:
            if phone_number:
                username= str(phone_number)[-5:]  +random.choice("qwertyuiopasdfghjklzxcvbnm") #به تصادف یکی از عناصر رشته را انتخاب می کند
            elif email : 
                username=email.split("@" , 1)[0] #  یکبار (۱) ، عملیان تقسیم کردن ایمیل را از @انجام میدهد و بخش ابتدایی را بر میدارد
        while User.objects.filter(username=username).exists():
            username+=str(random.randint(1,100))

        return self._create_user(username, email , phone_number,password , False , False , **extra_fields)


    def create_superuser(self , username , email , phone_number , password , **extra_fields):
        return self._create_user(username , email,phone_number , password ,True , True , **extra_fields)

    
    #def get_phone_number(self , phone_number): # this part = User.object.get(phone_number=phone_number)
        #pass  # User.object.get_by_phone_number('09123456789')


class User(AbstractBaseUser , PermissionsMixin):
    username=models.CharField(_("user name") , max_length=40 , unique=True)
    email=models.EmailField(_("Email"), unique=True , null=True , blank=True)
    phone_number=models.BigIntegerField(_("phone number") , unique=True ,
                                                validators=[validators.RegexValidator(r'^989[0-3,9]\d{8}$',
                                                                        ('Enter a valid mobile number.'),'invalid')] ,
                                                error_messages={"tekrari": _("this user name is already used try another one.")})
    first_name=models.CharField(max_length=40 , blank=True)
    last_name=models.CharField(max_length=40 , blank=True)
    is_staff=models.BooleanField(default=False , help_text=_("تعیین سطح دسترسی برای کاربر"),)
    date_joined=models.DateTimeField(_("date joined"),default=timezone.now)
    last_seen = models.DateTimeField(_('last seen date'), null=True)
    is_active=models.BooleanField(default=True , help_text=_("برای اینکه مشخص شود اکانت فعال است یا خیر") , verbose_name=_("is_active"))
    

    
    USERNAME_FIELD='username'
    REQUIRED_FIELDS=[ "phone_number" , "email"]
    
    objects=User_manager()

    class Meta:
        db_table="Users"
        verbose_name=_("user")
        verbose_name_plural=_("users")


    def get_full_name(self):
        full_name=f"{self.first_name} {self.last_name}".strip()
        return full_name

    def get_short_name(self):
        return self.first_name
    
    def email_sending(self ,subject , message , from_email=None , **kwargs):
        send_mail(subject , message , from_email , [self.email] ,**kwargs)

    @property
    def is_loggedin_user(self):
        """
        Returns True if user has actually logged in with valid credentials.
        """
        return self.phone_number is not None or self.email is not None

    def save(self, *args, **kwargs):
        if self.email is not None and self.email.strip() == '':
            self.email = None
        super().save(*args, **kwargs)

    def __str__(self):
         return self.username



class habitations(models.Model):
    country=models.CharField(max_length=30 , blank=True)
    province=models.CharField(max_length=30 , blank=True)
    city=models.CharField(max_length=30 , blank=True)
    address=models.TextField(max_length=60 , blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    last_modified=models.DateTimeField(auto_now=True)
    
    def __str__(self):
      return f'{self.country}-{self.province}-{self.city}'
    def get_address(self):
        return self.address
    





class Profile(models.Model):
    GENDER_CHOICE=(
        ("MALE" , "آقا"),
        ("FEMALE" , "خانم"),
        ("UNKNOWN" , "عدم تمایل به ذکر")
    )

    user=models.OneToOneField(User ,verbose_name=_("for user") ,on_delete=models.CASCADE )
    nickname=models.CharField(_("nick name") , blank=True , null=True , max_length=40)
    Gender=models.CharField(max_length=20 , choices=GENDER_CHOICE , default="UNKNOWN" , verbose_name=_("جنسیت"))
    birthday=models.DateField(null=True , verbose_name=_("birthday") , blank=True)
    avatar=models.ImageField(verbose_name=_("عکس پروفایل") , blank=True)
    from_at=models.ForeignKey(to=habitations , verbose_name=_("habitation") , null=True , on_delete=models.SET_NULL)
    # phone_number=models.BigIntegerField(_("phone number") , unique=True , 
    #                                             validators=[validators.RegexValidator(r'^989[0-3,9]\d{8}$',
    #                                                                     ('Enter a valid mobile number.'),'invalid')] ,
    #                                             error_messages={"tekrari": -("this user name is already used try another one.")})
# اگر از کلاس یوزر خود جنگو استفاده میکردیم ، میبایستی شماره تلفن را در بخش پروفایل بگیری 
# و دیگه ثبت نام به وسیله شماره تلفن انجام نمی شد
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    @property
    def get_first_name(self):
        return self.user.first_name

    @property
    def get_last_name(self):
        return self.user.last_name

    def get_nickname(self):
        return self.nickname if self.nickname else self.user.username






class Device(models.Model):
    WEB=0
    ANDROID=1
    OS=2
    PC=3
    DEVICE_TYPE=(
        (WEB ,"web"),
        (ANDROID , "android"),
        (OS , "os"),
        (PC , "pc")
    )



    for_user=models.ForeignKey(User , on_delete=models.CASCADE)
    UUID=models.UUIDField(null=True , verbose_name="_unique code")
    Device_type=models.CharField(max_length=8 , choices=DEVICE_TYPE , default=WEB)
    app_version=models.CharField(max_length=30 , blank=True )
    device_model=models.CharField(max_length=30 , blank=True)
    created_time=models.DateTimeField(auto_now_add=True)
 # notify_token = models.CharField(
    #     _('Notification Token'), max_length=200, blank=True,
    #     validators=[validators.RegexValidator(r'([a-z]|[A-z]|[0-9])\w+',
    #                                           _('Notify token is not valid'), 'invalid')]
    # )
    class Meta:
        db_table = 'devices information'
        verbose_name = _('device')
        verbose_name_plural = _('devices')
        unique_together=("for_user" , "UUID") # باید اسم فیلد های نوشته شده ، استفاده بشوند

        