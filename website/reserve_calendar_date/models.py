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
                                on_delete=models.CASCADE, related_name="reserve_master")

    client = models.ForeignKey(User, blank=True, null=True, default=None, verbose_name=_('Client'),
                               on_delete=models.CASCADE, related_name="reserve_client")

    client_name = models.CharField(max_length=256, blank=True, null=True, default=None, verbose_name=_('Client Name'))

    client_email = models.CharField(max_length=256, blank=True, null=True, default=None, verbose_name=_('Client Email'))

    client_phone = models.TextField(max_length=64, blank=True, null=True, default=None, verbose_name=_('Client Phone'))

    start_datetime = models.DateTimeField(verbose_name=_('Start time'), help_text=_('Start time for the reservation'),)

    end_datetime = models.DateTimeField(verbose_name=_('End time'), help_text=_('End time for the reservation'),)

    duration_time = models.DurationField(verbose_name=_('Duration'), default=None, blank=True, null=True,
                                         help_text=_('Field with auto filling'),)

    start_date = models.DateField(verbose_name=_('Start date'), help_text=_('Auto filling field'), default=None, blank=True, null=True)

    end_date = models.DateField(verbose_name=_('End date'), help_text=_('Auto filling field'), default=None, blank=True, null=True)

    start_time = models.TimeField(verbose_name=_('Start time'), help_text=_('Auto filling field'), default=None, blank=True, null=True)

    end_time = models.TimeField(verbose_name=_('End time'), help_text=_('Auto filling field'), default=None, blank=True, null=True)

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
        ordering = ['-start_datetime']

    def save(self, *args, **kwargs):
        self.clean()
        self.duration_time = self.end_datetime - self.start_datetime
        self.id = self.number
        self.start_date = self.start_datetime.date()
        self.end_date = self.end_datetime.date()
        self.start_time = self.start_datetime.time()
        self.end_time = self.end_datetime.time()
        super(Reservation, self).save(*args, **kwargs)


    def clean(self):
        if self.end_datetime < self.start_datetime:
            raise ValidationError(_("Wrong time of reservation. The end time can't less the start time."))

        if self.start_datetime < timezone.now():
            raise ValidationError(_("Wrong time of reservation. The start time can't less now."))

        reservation = Reservation.objects.filter(master=self.master, end_datetime__gt=timezone.now()).exclude(id=self.id)

        previous_reservation = reservation.filter(start_datetime__lte=self.start_datetime).order_by('start_datetime').reverse().first()
        if previous_reservation and self.start_datetime < previous_reservation.end_datetime:
            raise ValidationError(_('Wrong start time of reservation.  Time is busy. ')+str(self.start_datetime))

        next_reservation = reservation.filter(end_datetime__gte=self.end_datetime).order_by('end_datetime').first()
        if next_reservation and self.end_datetime > next_reservation.start_datetime:
            raise ValidationError(_('Wrong end time of reservation. Time is busy.')+str(self.end_datetime))

        if reservation.filter(start_datetime__gte=self.start_datetime, end_datetime__lte=self.end_datetime).exists():
            raise ValidationError(_('Wrong time of reservation. Time is busy.')+str(self.start_datetime))

    def get_absolute_url(self):
        return '%s' % self.id


#TODO: Добавить def в модель юзера, который выводит список занятого времени мастера
#TODO: В плагине при выводе даты календаря, проверить на наличие свободного времени в текущем дне и вывести во фронтенд
#TODO: Во фронтенде при выборе даты блокировать занятое время выбранного дня (проверка джавой по клику на кнопке со списком занятого времени
