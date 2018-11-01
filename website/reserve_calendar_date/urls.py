# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.ListViewReservation.as_view(),  name='reservations-list'),
    url(r'(?P<pk>\d+)$', views.DetailViewReservation.as_view(), name='reservations-detail'),
    # url(r'^create/$', views.CreatePostView.as_view(), name='create'),
    # url(r'^update/(?P<pk>\d+)/', views.UpdatePostView.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/delete/', views.DeleteReservation.as_view(), name='delete-reservations'),
]