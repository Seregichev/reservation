# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from .views import login_view, logout_view

urlpatterns = [
    url(r'^login/$', login_view, name='login_view'),
    url(r'^logout/$', logout_view, name='logout_view'),
]
