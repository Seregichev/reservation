# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Reservation


class ReservationAdmin(admin.ModelAdmin):

    list_display = [field.name for field in Reservation._meta.fields]
    exclude = ['start_date','end_date','start_time','end_time']


    class Meta:
        model = Reservation


admin.site.register(Reservation, ReservationAdmin)
