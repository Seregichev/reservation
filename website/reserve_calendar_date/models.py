# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from random import randint


STATUS_CHOICES = (
    ('New', _('New')),  # Необработанная
    ('Accepted', _('Accepted')),  # Бронь подтверждена
    ('Done', _('Done')),  # Выполено/Завершено
    ('Waiting to cancel', _('Waiting to cancel')),  # Ожидание отмены
    ('Canceled', _('Canceled')),  # Отменено
    ('Deleted', _('Deleted')),  # Удалено
)


@python_2_unicode_compatible
class Reservation(models.Model):

    number = models.IntegerField(default=randint(1, 999999), unique=True, verbose_name=_('Number Reservation'))

    master = models.ForeignKey(User, verbose_name=_('Master'),
                                on_delete=models.CASCADE, related_name="reserv_master")

    client = models.ForeignKey(User, blank=True, null=True, default=None, verbose_name=_('Client'),
                               on_delete=models.CASCADE, related_name="reserv_client")

    client_name = models.CharField(max_length=256, blank=True, null=True, default=None, verbose_name=_('Client Name'))

    client_email = models.CharField(max_length=256, blank=True, null=True, default=None, verbose_name=_('Client Email'))

    client_phone = models.TextField(max_length=64, blank=True, null=True, default=None, verbose_name=_('Client Phone'))

    start_time = models.DateTimeField(verbose_name=_('Start time'), help_text=_('Start time for the reservation'),)

    end_time = models.DateTimeField(verbose_name=_('End time'), help_text=_('End time for the reservation'),)

    duration_time = models.DurationField(verbose_name=_('Duration'), default=None, blank=True, null=True,
                                         help_text=_('Field with auto filling'),)

    product = models.CharField(max_length=128, blank=True, null=True, default=None, verbose_name=_('Product'))

    price = models.DecimalField(max_digits=64, decimal_places=2, default=0.00, verbose_name=_('Price'))

    comment = models.TextField(max_length=256, blank=True, null=True, default=None, verbose_name=_('Comment'))

    status = models.CharField(choices=STATUS_CHOICES, max_length=32, blank=True, null=True, default='New',
                                    verbose_name=_('Status'))

    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name=_('Updated'))

    def __str__(self):
        return _('Reservation ') + str(self.id)

    class Meta:
        verbose_name = _('Reservation')
        verbose_name_plural = _('Reservations')
        ordering = ['-start_time']

    def save(self, *args, **kwargs):
        self.duration_time = self.end_time - self.start_time
        self.id = self.number
        super(Reservation, self).save(*args, **kwargs)


    def clean(self):
        if self.end_time < self.start_time:
            raise ValidationError(_("Wrong time of reservation. The end time can't less the start time."))

        if self.start_time < timezone.now():
            raise ValidationError(_("Wrong time of reservation. The start time can't less now."))

        reservation = Reservation.objects.filter(master=self.master, end_time__gt=timezone.now()).exclude(id=self.id)

        previous_reservation = reservation.filter(start_time__lte=self.start_time).order_by('start_time').reverse().first()
        if previous_reservation and self.start_time < previous_reservation.end_time:
            raise ValidationError(_('Wrong start time of reservation. Time is busy.'))

        next_reservation = reservation.filter(end_time__gte=self.end_time).order_by('end_time').first()
        if next_reservation and self.end_time > next_reservation.start_time:
            raise ValidationError(_('Wrong end time of reservation. Time is busy.'))

        if reservation.filter(start_time__gte=self.start_time, end_time__lte=self.end_time).exists():
            raise ValidationError(_('Wrong time of reservation. Time is busy.'))

    def get_absolute_url(self):
        return '%s' % self.id
