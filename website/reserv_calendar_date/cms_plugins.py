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

# Плагин приветсвия
@python_2_unicode_compatible
class Reserv_Calendar_Time_PluginSetting(CMSPlugin):
    num_of_month = models.IntegerField(_('Number of months together') , default=3, null=True, blank=True)
    show_weeks_number = models.BooleanField (_('Show number of weeks'), default=False)
    show_year = models.BooleanField(_('Show year'), default=True)
    busy_time_color = ColorField(_('Color busy time sell'), default='#dc3545', null=True, blank=True)
    free_time_color = ColorField(_('Color free time sell'), default='#28a745', null=True, blank=True)
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

        months = ()  # Инициализируем список выборки по месяцам
        i = 1  # Объявдяем счетчик кол-ва месяцев для цикла while
        while i <= instance.num_of_month:  # Обходим циклом заданное кол-во месяцев от текущего
            now = datetime.datetime.now() + relativedelta(months=+(i-1))  # Формируем текущую дату

            this_month = calendar.Calendar(firstweekday=0)  # получаем календарь с первым днем недели Пн
            this_month = this_month.itermonthdays2(now.year, now.month)  # Получаем кортедж из дня и номера дня недели

            day_in_this_month = ()  # Инициализируем многомерный список дней в этом месяце
            for day, day_of_week in this_month: # Обходим циклом кортедж
                if day > 0:
                    this_day = day
                else:
                    this_day = 1
                number_of_week = datetime.date(now.year, now.month, this_day).strftime("%V")
                day_in_this_month += ((day, day_of_week, number_of_week),)  # и получаем список (день, номер дня, номер недели)

            name_month = _(now.strftime('%B'))  # получаем название текущего месяца в переводе на локаль
            the_year = now.year  # Получаем текущий год
            num_month = i   # Получаем порядковый номер месяца из выдачи

            months += ((day_in_this_month, name_month, the_year, num_month),)  # Заносим все в список выборки по месяцам

            i += 1  # Увеличиваем счетчик

        # Выводим все полученные данные во фронтенд
        context['months'] = months
        context['today'] = datetime.datetime.now().day
        context['day_abbr'] = calendar.day_abbr
        return context


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

# TODO: Создать модель мастеров и клиентов
# TODO: Создать модель брони с полями datetime времени начала брони и конца брони, категории брони: заявка, принято, отменено, выполнено, привязка к мастеру и клиенту (если зарегистрирован)
# TODO: Проверка при добавлении заявки - Если нет начала или конца существующей брони от начала до конца планируемой брони отсортированной в порядке возрастания