# -*- coding: utf-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

@apphook_pool.register
class ViewReservationApphook(CMSApp):
    app_name = 'view_reservation'
    name = _('View Reservation')

    def get_urls(self, page=None, language=None, **kwargs):
        return ["reserve_calendar_date.urls"]

# TODO: Сделать cms_app вывода информации о бронировании по ссылке на рандомный id