# -*- coding: utf-8 -*-
from django.db import models
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

import calendar
import datetime
import locale
from dateutil.relativedelta import relativedelta
from colorfield.fields import ColorField
locale.setlocale(locale.LC_NUMERIC, "ru_RU")


CHOICES_TIME_DELTA = (
        (datetime.timedelta(minutes=15), _('15 minutes')),
        (datetime.timedelta(minutes=30), _('30 minutes')),
        (datetime.timedelta(minutes=45), _('45 minutes')),
        (datetime.timedelta(hours=1), _('1 hour')),
        (datetime.timedelta(hours=2), _('2 hours')),
        (datetime.timedelta(hours=3), _('3 hours')),
        (datetime.timedelta(hours=4), _('4 hours')),
        (datetime.timedelta(hours=5), _('5 hours')),
        (datetime.timedelta(hours=6), _('6 hours')),
        (datetime.timedelta(hours=7), _('7 hours')),
        (datetime.timedelta(hours=8), _('8 hours')),
        (datetime.timedelta(hours=9), _('9 hours')),
        (datetime.timedelta(hours=10), _('10 hours')),
        (datetime.timedelta(hours=11), _('11 hours')),
        (datetime.timedelta(hours=12), _('12 hours')),
        (datetime.timedelta(hours=24), _('1 day')),
    )

# Плагин приветсвия
@python_2_unicode_compatible
class ReserveCalendarTimePluginSetting(CMSPlugin):
    masters = models.ManyToManyField(User, verbose_name=_('Choice masters:'), related_name="reserv_masters_plugin",
                                     blank=False, )
    text_before_calendars = models.CharField(_('Text before calendars'), default=_('1. Select a free day of the month'),
                                             null=True, blank=True, max_length=256,)
    text_before_time_intervals = models.CharField(_('Text before time intervals'), default=_('2. Choose a free time'),
                                             null=True, blank=True, max_length=256,)
    text_style = models.CharField(_('HTML text style'), max_length=256, null=True, blank=True, default='margin: 1em;')
    num_of_month = models.IntegerField(_('Number of months to show'), default=3, null=True, blank=True)
    show_weeks_number = models.BooleanField(_('Show number of weeks'), default=False)
    show_year = models.BooleanField(_('Show year'), default=True)
    allow_choose_several_days = models.BooleanField(_('Allow choose several days'), default=False)
    busy_time_color = ColorField(_('Color busy time sell'), default='#dc3545', null=True, blank=True)
    free_time_color = ColorField(_('Color free time sell'), default='#28a745', null=True, blank=True)
    start_time = models.TimeField(_('Start time'), default='8:00:00')
    end_time = models.TimeField(_('End time'), default='17:00:00')
    time_delta = models.DurationField(_('Time Delta'), choices=CHOICES_TIME_DELTA, default=datetime.timedelta(hours=1))
    tag_class = models.CharField(_('HTML class'), max_length=256, null=True, blank=True, default='')
    tag_style = models.CharField(_('HTML style'), max_length=256, null=True, blank=True, default='')

    def get_title(self):
        return str(self.id) + str(_(' Reservation Calendar Time Plugin'))

    def __str__(self):
        return self.get_title()

    def clean(self):
        if self.end_time < self.start_time:
            raise ValidationError(_("Wrong time. The end time can't less the start time."))
        if self.num_of_month <= 0:
            raise ValidationError(_("Wrong the number of month. The number have to is more zero"))
        if self.time_delta < datetime.timedelta(minutes=15):
            raise ValidationError(_("Wrong the Time Delta. The Time Delta have to is more or equal 15 minutes"))
        if self.time_delta < datetime.timedelta(hours=24):
            if self.allow_choose_several_days:
                raise ValidationError(_("Can't select 'Allow choose several days' when Time Delta don't equal a day"))


@plugin_pool.register_plugin
class ReserveCalendarTimePlugin(CMSPluginBase):

    module = _("Plugins")
    name = _("Reservation Calendar Time Plugin")
    model = ReserveCalendarTimePluginSetting
    render_template = "plugins/reserve_calendar_time_plugin.html"

    fieldsets = (
        (None, {
            'fields': ('masters',),
        }),
        (_('Text:'), {
            'fields': ('text_before_calendars', 'text_before_time_intervals', 'text_style')
        }),
        (_('Show setting:'), {
            'fields': ('num_of_month', ('show_weeks_number', 'show_year'),)
        }),
        (_('Time setting:'), {
            'fields': (('start_time', 'end_time',),'time_delta',)
        }),
        (_('Other setting:'), {
            'classes': ('collapse',),
            'fields': ('allow_choose_several_days',)
        }),
        (_('Color setting:'), {
            'classes': ('collapse',),
            'fields': ('busy_time_color', 'free_time_color',)
        }),
        (_('HTML attributes:'), {
            'classes': ('collapse',),
            'fields': ('tag_class', 'tag_style',)
        }),
    )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "masters":
            try:
                user_company = request.user.company
            except AttributeError:
                user_company = None
            if user_company:
                kwargs["queryset"] = User.objects.filter(customuser__company=request.user.company).values_list('first_name', 'last_name')
        return super(ReserveCalendarTimePlugin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def render(self, context, instance, placeholder):
        context = super(ReserveCalendarTimePlugin, self).render(context, instance, placeholder)

        # --- Формирование календаря для вывода во фронтенде ---
        months = ()  # Инициализируем список выборки по месяцам
        start_month = datetime.datetime.now()  # месяц начала вывода равна текущей дате
        end_month = datetime.datetime.now() + relativedelta(months=+(instance.num_of_month-1))  # месяц конца вывода
        e = 1  # ватчдог
        while start_month <= end_month and e < 100:
            print(start_month, end_month)
            this_month = calendar.Calendar(firstweekday=0).itermonthdays2(start_month.year, start_month.month)

            day_in_this_month = ()  # Инициализируем многомерный список дней в этом месяце
            for day, day_of_week in this_month:  # Обходим циклом кортедж
                if day > 0:
                    this_day = day
                else:
                    this_day = 1

                date = datetime.date(start_month.year, start_month.month, this_day)  # Получаем текущую дату
                number_of_week = datetime.date(start_month.year, start_month.month, this_day).strftime("%V")
                day_in_this_month += ((day, day_of_week, number_of_week, date.year, date.month, date.day),)  # и получаем список для дня

            name_month = _(start_month.strftime('%B'))  # получаем название текущего месяца в переводе на локаль
            the_year = start_month.year  # Получаем текущий год
            num_month = e   # Получаем порядковый номер месяца из выдачи
            months += ((day_in_this_month, name_month, the_year, num_month),)  # Заносим все в список выборки по месяцам

            start_month = start_month + relativedelta(months=+1)
            e += 1

        # --- Формирование списка времени для вывода во фронтенде ---
        time = ()  # список содержащий перечень времени

        if instance.time_delta < datetime.timedelta(hours=24):
            start_time = instance.start_time  # время начала из настроек плагина
            end_time = instance.end_time  # время завершения из настроек плагина
            e = 0  # ватчдог

            while start_time < end_time and e < 100:
                next_time = (datetime.datetime(year=2000,month=1,day=1, hour=start_time.hour, minute=start_time.minute,
                                               second=start_time.second) + instance.time_delta).time()  # следующее время
                if (start_time.second):
                    title = start_time.strftime('%H:%M:%S') + '-' + next_time.strftime('%H:%M:%S')
                else:
                    title = start_time.strftime('%H:%M') + '-' + next_time.strftime('%H:%M')

                time += ((title,  # текст периода
                          start_time.hour, start_time.minute, start_time.second,  # время начала периода
                          next_time.hour, next_time.minute, next_time.second),)  # время конца периода

                start_time = next_time
                e += 1

        # Выводим все полученные данные во фронтенд
        context['time'] = time  # многомерный список для вывода выборки времени
        context['months'] = months  # многомерный список для вывода в календарь месяцев
        context['today'] = datetime.datetime.now().day  # текущий день
        context['day_abbr'] = calendar.day_abbr  # абревиатуры дня
        return context

# TODO: Создать форму бронирования для отправки


# Плагин приветсвия
@python_2_unicode_compatible
class HelloPluginSetting(CMSPlugin):
    welcome = models.CharField(_('Welcome'), max_length=128, null=True, blank=True)
    afterword = models.TextField(_('Afterword'), max_length=256, null=True, blank=True)
    unnamed_name = models.CharField(_('Name of visitor'), max_length=128, null=True, blank=True)
    tag_class = models.CharField(_(u'HTML class'), max_length=256, null=True, blank=True)
    tag_style = models.CharField(_(u'HTML class'), max_length=256, null=True, blank=True)

    def get_title(self):
        return self.welcome or self.afterword

    def __str__(self):
        return self.get_title()


@plugin_pool.register_plugin
class HelloPlugin(CMSPluginBase):

    module = _("Plugins")
    name = _("Hello Plugin")
    model = HelloPluginSetting
    render_template = "plugins/hello_plugin.html"

    def render(self, context, instance, placeholder):
        context = super(HelloPlugin, self).render(context, instance, placeholder)
        return context
