from django.conf.urls import url
from django.views.i18n import JavaScriptCatalog

from .views import *

urlpatterns = [
    url(r'^order$', get_order_book_view, name='order_list'),
    url(r'^order/(?P<user_id>[0-9a-zA-Z]+)$', get_user_order_view, name='user_order'),
    url(r'^trade', get_trade_data_view),
]
