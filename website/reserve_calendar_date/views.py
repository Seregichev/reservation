# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from .models import Reservation

class ListViewReservation(ListView):
    model = Reservation
    template_name = "apps/listviewreservation.html"
    context_object_name = 'reservations'
    paginate_by = 10

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by)

    def get_context_data(self, **kwargs):
        context = super(ListViewReservation, self).get_context_data(**kwargs)
        context['reservations'] = Reservation.objects.filter(client=self.request.user).order_by('start_time').reverse()

        reservation_list = Reservation.objects.filter(client=self.request.user).order_by('start_time').reverse()
        paginator = Paginator(reservation_list, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            reservation_list = paginator.page(page)
        except PageNotAnInteger:
            reservation_list = paginator.page(1)
        except EmptyPage:
            reservation_list = paginator.page(paginator.num_pages)

        context['reservations'] = reservation_list
        return context

class DetailViewReservation(DetailView):
    model = Reservation
    template_name = "apps/detailviewreservation.html"

# TODO: Сделать ListView для мастера
# TODO: В DetailView сделать возможность редактирования как для мастера так и клиента