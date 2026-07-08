from django.db import models

from django.utils.translation import gettext_lazy as _

from utils.validation import validate_phone_number


class banks_Gate(models.Model):
    name=models.CharField(_("name"), max_length=30 )
    description=models.TextField(_("description") , blank="")
    avatar=models.ImageField(verbose_name=_("avatar"), blank=True , null=True , upload_to="banks/")
    is_enable=models.BooleanField(_('is enable') , default=True)
    credentials=models.TextField(verbose_name=_("credentials") , blank=True)
    created_time=models.DateTimeField(verbose_name=_("created time") , auto_now_add=True)
    updated_time=models.DateTimeField(verbose_name=_("update time") , auto_now=True)
    class Meta:
        db_table="banks Gate"
        verbose_name="bank gate"
        verbose_name_plural="banks Gate"

    def __str__(self):
        return self.name


class transaction(models.Model):
    status_init=0
    STATUS_PAID=100
    STATUS_FAIL=200
    STATUS_CANCELLED=300
    STATUS_REFUND=400
    STATUS_TYPE=(   
        (status_init , _("INITIAL")),
        (STATUS_PAID , _("SUCCESSFUL")),
        (STATUS_FAIL , _("FAILED")),
        (STATUS_CANCELLED , _("CANCELLED")),
        (STATUS_REFUND , _("REFUND")),
    )

    status_massage={
        status_init:"you transaction procces are beggining",
        STATUS_PAID:"your transaction were successful",
        STATUS_FAIL:"your transaction were failure",
        STATUS_CANCELLED:"you cancelled the procces",
        STATUS_REFUND:"your money get back to your account",

    }

    user=models.ForeignKey("User.User" , on_delete=models.CASCADE , verbose_name=_("user"))#if you want you can add related_name=
    package=models.ForeignKey("subscriptions.plans" , verbose_name=_("package") , on_delete=models.CASCADE )
    bank_port=models.ForeignKey(banks_Gate , verbose_name=_("bank_port") , on_delete=models.CASCADE)
    status=models.PositiveSmallIntegerField(verbose_name=_("status") , choices=STATUS_TYPE, default=status_init , db_index=True)
    price=models.PositiveIntegerField(_('price'), default=0)
    phone_number=models.BigIntegerField(_('phone number'),validators=[validate_phone_number,] ,db_index=True)
    token=models.CharField(max_length=512 , null=True) #میتونه هر تایپی باشه
    consumed_code=models.PositiveIntegerField(_('tracking code'), null=True, db_index=True)
    created_time=models.DateTimeField(_("creation time") , auto_now_add=True, db_index=True)
    updated_time=models.DateTimeField(_('modification time'), auto_now=True)
    class Meta:
        db_table="transaction"
        verbose_name=_("transaction")
        verbose_name_plural=_("transactions")







