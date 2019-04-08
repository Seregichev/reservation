# -*- coding: utf-8 -*-
from django.core.exceptions import FieldError
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from .models import Reservation
from django.utils import timezone
from .forms import ReservationForm, UpdateStatusForm, DetailForm
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Sum
from goods.models import Product
import datetime

class ListViewReservation(ListView):
    model = Reservation
    template_name = "apps/reservation_list_view.html"
    context_object_name = 'reservations'
    # paginate_by = 10
    # def get_paginate_by(self, queryset):
    #     return self.request.GET.get('paginate_by', self.paginate_by)

    def get_context_data(self, **kwargs):
        context = super(ListViewReservation, self).get_context_data(**kwargs)

        if self.request.user.administrator:
            if self.request.user.company:
                reservation_list = Reservation.objects.filter(master__company=self.request.user.company)
            elif self.request.user.is_superuser:
                reservation_list = Reservation.objects.all()
            else:
                reservation_list = None
        elif self.request.user.master:
            reservation_list = Reservation.objects.filter(master=self.request.user)
        else:
            reservation_list = Reservation.objects.filter(client=self.request.user)

        ordering = self.request.GET.get('ordering', 'start_time')
        reservation_list = reservation_list.order_by(ordering)

        reservation_list = reservation_list.exclude(end_datetime__lt=timezone.now())
        reservation_list = reservation_list.exclude(status='Canceled')

        # paginator = Paginator(reservation_list, self.paginate_by, orphans=3, allow_empty_first_page=True)
        #
        # page = self.request.GET.get('page')
        #
        # try:
        #     reservation_list = paginator.page(page)
        # except PageNotAnInteger:
        #     reservation_list = paginator.page(1)
        # except EmptyPage:
        #     reservation_list = paginator.page(paginator.num_pages)

        context['reservations'] = reservation_list
        return context


class DetailViewReservation(DetailView):
    # Детальное отображдение бронирования
    model = Reservation
    template_name = "apps/reservation_detail_view.html"


class CreateViewReservation(CreateView):
    # Создание записи бронирования
    form_class = ReservationForm
    model = Reservation
    template_name = "apps/reservation_create_view.html"
    success_url = reverse_lazy('view_reservation:list-reservations')


class ChangeViewReservation(UpdateView):
    # Обновление информации записи бронирования
    form_class = ReservationForm
    model = Reservation
    template_name = "apps/reservation_change_view.html"
    success_url = reverse_lazy('view_reservation:list-reservations')


class UpdateStatusReservation(UpdateView):
    # Обновление статуса записи бронирования
    form_class = UpdateStatusForm
    template_name = "apps/reservation_confirm_update_status.html"
    model = Reservation
    success_url = reverse_lazy('view_reservation:list-reservations')


class DeleteReservation(DeleteView):
    # Удаление записи бронирования
    model = Reservation
    template_name = "apps/reservation_confirm_delete.html"
    success_url = reverse_lazy('view_reservation:list-reservations')


def check_reservation_time(request):
    return_dict = dict()
    if settings.DEBUG:
        print(request.POST)

    if request.POST:
        products = request.POST['products'] or None
        date = request.POST['date'] or None
        date = datetime.datetime.strptime(date, '%x')
        products = [int(n) for n in products.split(',')[:-1]]
        busy_time_list = User.objects.filter(customuser__products__in=Product.objects.filter(id__in=products),
                                             reserve_master__start_date=date) \
            .values_list('reserve_master__start_time', 'reserve_master__end_time') \
            .order_by('reserve_master__start_datetime')

        return_dict['busy_time_list'] = [time for time in busy_time_list]
        print(return_dict['busy_time_list'])

    return JsonResponse(return_dict)