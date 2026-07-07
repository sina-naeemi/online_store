from django.utils.translation import gettext_lazy as _

from django.db import models

from utils.validation import validate_sku

class plans(models.Model):
    # gateways=models.ManyToManyField("peyments.banks_Gate",verbose_name="gateways" , on_delete=models.SET_NULL)
    title=models.CharField(verbose_name=_("title"),max_length=60)
    sku=models.CharField(_("code adnbar")    , db_index=True , validators=[validate_sku])#stock keeping units
    avatar=models.ImageField(_("picture"  ), upload_to="planes/" , blank=True , null=True)
    discreaption=models.TextField(_("discreaption"),blank=True )
    price=models.IntegerField(_("price"))
    is_enable=models.BooleanField(_("is enable"),default=True)
    start_time=models.DateTimeField(_("active time"),auto_now_add=True )
    duration=models.DurationField(_("duration"), blank=True , null=True,)
    updated_time=models.DateTimeField(_("updated time"), auto_now=True)

    class Meta:
        db_table="plans"
        verbose_name="plan"
        verbose_name_plural="plans"

    def __str__(self):
        return self.title

class subscription(models.Model):
    user=models.ForeignKey("User.User",on_delete=models.CASCADE , )#app name.model name
    pack=models.ForeignKey("plans" , on_delete=models.CASCADE )
    active_time=models.DateTimeField(verbose_name=_("active time"),auto_now_add=True)
    expire_time=models.DateTimeField(_("expire"), blank=True , null=True )

    class Meta:
        db_table="user subscriptions"
        verbose_name="subscription"
        verbose_name_plural="subscriptions"


