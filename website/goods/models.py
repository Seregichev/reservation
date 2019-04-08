# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from filer.fields.image import FilerImageField


@python_2_unicode_compatible
class ProductCategory(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name=_('Name'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is active ?'))

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name=_('Category')
        verbose_name_plural=_('Categories')

@python_2_unicode_compatible
class Product(models.Model):
    name = models.CharField(max_length=256, blank=True, null=True, default=None, verbose_name=_('Name'))
    price = models.DecimalField(max_digits=64, decimal_places=2, default=0, verbose_name=_('Price'))
    currency = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name=_('Currency'))
    description = models.TextField(blank=True, null=True, default=None, verbose_name=_('Description'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is active ?'))
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name=_('Updated'))

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


@python_2_unicode_compatible
class ProductImage(models.Model):
    product = models.ForeignKey(Product, blank=True, null=True, default=None, verbose_name=_('Product'))
    image = FilerImageField(null=True, blank=True,related_name="product_image")
    is_main = models.BooleanField(default=False, verbose_name=_('Is main ?'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is active ?'))
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name=_('Updated'))

    def __str__(self):
        return "%s" % (self.id,)

    class Meta:
        verbose_name=_('Photo')
        verbose_name_plural=_('Photos')
