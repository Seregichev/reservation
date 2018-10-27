# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.ListViewReservation.as_view()),
    url(r'(?P<pk>\d+)$', views.DetailViewReservation.as_view()),
]