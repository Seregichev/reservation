# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from .models import Reservation
from django.utils import timezone


class ListViewReservation(ListView):
    model = Reservation
    template_name = "apps/reservation_list_view.html"
    context_object_name = 'reservations'
    paginate_by = 10

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by)

    def get_context_data(self, **kwargs):
        context = super(ListViewReservation, self).get_context_data(**kwargs)

        if self.request.user.administrator:
            if self.request.user.company:
                reservation_list = Reservation.objects.filter(master__company=self.request.user.company)
            else:
                reservation_list = Reservation.objects.all()
        elif self.request.user.master:
            reservation_list = Reservation.objects.filter(master=self.request.user)
        else:
            reservation_list = Reservation.objects.filter(client=self.request.user)

        reservation_list = reservation_list.order_by('start_time').exclude(end_time__lt=timezone.now())
        paginator = Paginator(reservation_list, self.paginate_by, orphans=3, allow_empty_first_page=True)

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
    template_name = "apps/reservation_detail_view.html"

class DeleteReservation(DeleteView):
    model = Reservation
    template_name = "apps/reservation_confirm_delete.html"
    success_url = reverse_lazy('view_reservation:reservations-list')

# TODO: Сделать CreateView, UpdateView  модели Reservation
# TODO: Добавить в ListView выпадающий список текущего статуса брони и формы делающую UpdateView
# TODO: В DetailView сделать возможность редактирования для мастера, удаления для администратора, а для клиента возможность запроса отмены