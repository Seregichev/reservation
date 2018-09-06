# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

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


class CustomUser(User):

    company = models.ForeignKey(Company, blank=True, null=True, default=None, verbose_name=u"Компания",
                             on_delete=models.CASCADE)

    objects = UserManager()


def create_custom_user(sender, instance, created, **kwargs):
    if created:
        values = {}
        for field in sender._meta.local_fields:
            values[field.attname] = getattr(instance, field.attname)
        user = CustomUser(**values)
        user.save()

post_save.connect(create_custom_user, User)

# TODO: Создать модель мастеров и клиентов
# TODO: Создать модель брони с полями datetime времени начала брони и конца брони, категории брони: заявка, принято, отменено, выполнено, привязка к мастеру и клиенту (если зарегистрирован)
# TODO: Проверка при добавлении заявки - Если нет начала или конца существующей брони от начала до конца планируемой брони отсортированной в порядке возрастания