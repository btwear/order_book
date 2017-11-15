from book.models import Order, Trade, HistoryTrade, Token
from django.core import serializers
import json

def get_user_order_list(page_size, user_id):
    order_list = list(Order.objects.filter(user_id=user_id).values('type', 'token_id', 'price', 'amount', 'timestamp').order_by('-timestamp')[:page_size])
    order_list = {'order':order_list}
    order_list = json.dumps(order_list)
    order_list = json.loads(order_list)
    return order_list

def get_order_book(page_size, token_id):
    order_list = []
    order_list.append(list(Order.objects.filter(type=0, token_id=token_id).values('price', 'amount').order_by('-price')[:page_size]))
    order_list.append(list(Order.objects.filter(type=1, token_id=token_id).values('price', 'amount').order_by('price')[:page_size]))
    for i in range(0,2):
        order_list[i] = json.dumps(order_list[i])
        order_list[i] = json.loads(order_list[i])
    return order_list

def get_trade_record(since, until, token_id):
    trade_record = []
    trade_record = list(HistoryTrade.objects.filter(token_id=token_id, timestamp__gte=since, timestamp__lte=until).order_by('timestamp'))
    trade_record = json.dumps(trade_record)
    trade_record = json.loads(trade_record)
    return trade_record