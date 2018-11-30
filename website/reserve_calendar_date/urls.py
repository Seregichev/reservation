# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.ListViewReservation.as_view(),  name='list-reservations'),
    url(r'^(?P<pk>\d+)$', views.DetailViewReservation.as_view(), name='detail-reservations'),
    url(r'^create/$', views.CreateViewReservation.as_view(), name='create-reservations'),
    url(r'^(?P<pk>\d+)/update_status/', views.UpdateStatusReservation.as_view(), name='update-status-reservations'),
    url(r'^(?P<pk>\d+)/update/', views.ChangeViewReservation.as_view(), name='change-reservations'),
    url(r'^(?P<pk>\d+)/delete/', views.DeleteReservation.as_view(), name='delete-reservations'),
]