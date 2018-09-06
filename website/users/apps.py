# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = _('Users')
