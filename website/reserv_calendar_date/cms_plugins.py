# -*- coding: utf-8 -*-
from django.db import models
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

import calendar
import datetime
import locale
from dateutil.relativedelta import relativedelta
from colorfield.fields import ColorField
locale.setlocale(locale.LC_NUMERIC, "ru_RU")


CHOISES_TIME_DELTA = (
        (datetime.timedelta(minutes=30), _('30 m')),
        (datetime.timedelta(hours=1), _('1 h')),
    )

# Плагин приветсвия
@python_2_unicode_compatible
class Reserv_Calendar_Time_PluginSetting(CMSPlugin):
    num_of_month = models.IntegerField(_('Number of months together') , default=3, null=True, blank=True)
    show_weeks_number = models.BooleanField (_('Show number of weeks'), default=False)
    show_year = models.BooleanField(_('Show year'), default=True)
    busy_time_color = ColorField(_('Color busy time sell'), default='#dc3545', null=True, blank=True)
    free_time_color = ColorField(_('Color free time sell'), default='#28a745', null=True, blank=True)
    start_time = models.TimeField(_('Start time'), default='8:00:00')
    end_time = models.TimeField(_('End time'), default='17:00:00')
    time_delta = models.DurationField(_('Time Delta'), choices=CHOISES_TIME_DELTA, default=datetime.timedelta(hours=1))
    tag_class = models.CharField(_('HTML class'), max_length=256, null=True, blank=True, default='')
    tag_style = models.CharField(_('HTML style'), max_length=256, null=True, blank=True, default='')

    def get_title(self):
        return str(self.id) + str(_(' Reservation Calendar Time Plugin'))

    def __str__(self):
        return self.get_title()


@plugin_pool.register_plugin
class Reserv_Calendar_Time_Plugin(CMSPluginBase):

    module = _("Plugins")
    name = _("Reservation Calendar Time Plugin")
    model = Reserv_Calendar_Time_PluginSetting
    render_template = "plugins/reserv_calendar_time_plugin.html"

    def render(self, context, instance, placeholder):
        context = super(Reserv_Calendar_Time_Plugin, self).render(context, instance, placeholder)

        # --- Формирование календаря для вывода во фронтенде ---
        months = ()  # Инициализируем список выборки по месяцам
        start_month = datetime.datetime.now()  # месяц начала вывода равна текущей дате
        end_month = datetime.datetime.now() + relativedelta(months=+instance.num_of_month)  # месяц конца вывода
        e = 1  # ватчдог
        while start_month.month <= end_month.month and e < 100:
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

# TODO: Создать шаблон вывода времени

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
