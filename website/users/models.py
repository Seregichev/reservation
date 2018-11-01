# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from weekday_field import fields as weekday_field
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

@python_2_unicode_compatible
class Company(models.Model):
    short_name = models.CharField(max_length=128, blank=True, null=True, default=None,
                                  verbose_name=_('Short name'))
    name = models.CharField(max_length=128, blank=True, null=True, default=None, verbose_name=_('Full name'))
    tax = models.DecimalField(max_digits=3, decimal_places=1, default=18.0, verbose_name=_('Tax'))
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name=_('Updated'))

    def __str__(self):
        return "%s" % (self.short_name)

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Сompanies')

@python_2_unicode_compatible
class CustomUser(User):

    company = models.ForeignKey(Company, blank=True, null=True, default=None, verbose_name=_('Company'),
                             on_delete=models.CASCADE, related_name='company')

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message=_("Phone number must be entered in the format: '+79999999999'. Up to 15 digits allowed."))
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, verbose_name=_('Phone number'))

    avatar = models.ImageField(upload_to='avatar_images/', blank=True, null=True, default=None, verbose_name=_('Avatar'),
                               )

    weekdays = weekday_field.WeekdayField(blank=True, null=True, default=None, verbose_name=_('Weekdays'),)

    master = models.BooleanField(blank=True, default=False, verbose_name=_('Master'),
                                 help_text=_('Check if the user can be a master'))

    administrator = models.BooleanField(blank=True, default=False, verbose_name=_('Administrator'),
                                 help_text=_('Check if the user can be a administrator'))

    objects = UserManager()

    def __str__(self):
        return "%s %s %s %s" % (self.id, self.company, self.first_name, self.last_name)

    def is_master(self):
        return self.master

    def is_administrator(self):
        return self.administrator

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar', False)
        if avatar:
            if avatar._size > 4 * 1024 * 1024:
                raise ValidationError(_("Image file too large ( > 4mb )"))
            return avatar
        else:
            raise ValidationError(_("Couldn't read uploaded image"))

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = 'avatar_images/noavatar.png'
        super(CustomUser, self).save(*args, **kwargs)


def create_custom_user(sender, instance, created, **kwargs):
    if created:
        values = {}
        for field in sender._meta.local_fields:
            values[field.attname] = getattr(instance, field.attname)
        user = CustomUser(**values)
        user.save()

post_save.connect(create_custom_user, User)

# user.objects.filter(username='olga').first().customuser.weekdays[10]

# TODO: Создать модель мастеров и клиентов
# TODO: Создать модель брони с полями datetime времени начала брони и конца брони, категории брони: заявка, принято, отменено, выполнено, привязка к мастеру и клиенту (если зарегистрирован)
# TODO: Проверка при добавлении заявки - Если нет начала или конца существующей брони от начала до конца планируемой брони отсортированной в порядке возрастания