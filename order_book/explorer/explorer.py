from book.models import Order, Trade, HistoryTrade, Token
from django.core.cache import cache
from django.conf import settings
from django.core import serializers
from django.db.models import Q
from operator import attrgetter
from operator import itemgetter
from django.forms.models import model_to_dict
import time
import json

def get_user_order_list(page_size, user_id):
    total_orders = cache.get_many(cache.keys('Order_*')).items()
    total_orders = [x[1] for x in total_orders]
    user_orders = []
    for i in total_orders:
        if i.user_id == user_id:
            order = {}
            order['type'] = i.type
            order['token_id'] = i.token_id
            order['price'] = i.price
            order['amount'] = i.amount
            order['timestamp'] = i.timestamp
            user_orders.append(order)
    sorted_user_orders = sorted(user_orders, key=itemgetter('timestamp'), reverse=True)[0:page_size]
    order_list = {'order':sorted_user_orders}
    order_list = json.dumps(order_list)
    order_list = json.loads(order_list)
    return order_list

def get_user_trade_list(page_size, user_id):
    total_trades = cache.get_many(cache.keys('Trade_*')).items()
    total_trades = [x[1] for x in total_trades]
    user_trades = [[],[]]
    for i in total_trades:
        if i.buyer == user_id:
            type = 0
            trade = {}
            trade['type'] = type
            trade['token_id'] = i.token_id
            trade['price'] = i.price
            trade['amount'] = i.amount
            trade['timestamp'] = i.timestamp
            user_trades[type].append(trade)
        if i.seller == user_id:
            type = 1
            trade = {}
            trade['type'] = type
            trade['token_id'] = i.token_id
            trade['price'] = i.price
            trade['amount'] = i.amount
            trade['timestamp'] = i.timestamp
            user_trades[type].append(trade)
    user_trades[0] = sorted(user_trades[0], key=itemgetter('timestamp'), reverse=True)[0:page_size]
    user_trades[1] = sorted(user_trades[1], key=itemgetter('timestamp'), reverse=True)[0:page_size]
    trade_list = {'order': user_trades}
    trade_list = json.dumps(trade_list)
    trade_list = json.loads(trade_list)
    return trade_list

def get_order_book(page_size, token_id):
    keys  = cache.keys('Order_' + str(token_id) + '_*')
    total_orders = cache.get_many(keys).items()
    total_orders = [x[1] for x in total_orders]
    order_list = [[],[]]
    for i in total_orders:
        order = {}
        order['price'] = i.price
        order['amount'] = i.amount
        order_list[int(i.type)].append(order)
    order_list[0] = sorted(order_list[0], key=itemgetter('price'), reverse=False)[0:page_size]
    order_list[1] = sorted(order_list[0], key=itemgetter('price'), reverse=True)[0:page_size]
    for i in range(0,2):
        order_list[i] = json.dumps(order_list[i])
        order_list[i] = json.loads(order_list[i])
    return order_list


time_interval = settings.ORDER_BOOK_SETTINGS['archive_time_interval']

def get_trade_record(since, until, token_id):
    since = since - (since % time_interval)
    if until > int(time.time()): until = int(time.time())
    if int((until - since)/time_interval) > cache.get('archive_number_' + str(token_id)):
        keys = cache.keys('Archive_' + str(token_id) + '_*')
    else:
        time_list = list(range(since, until + 1, time_interval))
        keys = list(map(lambda x: 'Archive_' + str(token_id) + '_' + str(x), time_list))
    trade_list = cache.get_many(keys).items()
    trade_list = [x[1] for x in trade_list]
    trade_list = sorted(trade_list, key=attrgetter('timestamp'), reverse=False)
    trade_records = []
    for i in trade_list:
        if i.timestamp < since or i.timestamp > until:
            continue
        record = {}
        record['price'] = round(i.price, 4)
        record['total'] = i.amount
        record['timestamp'] = i.timestamp
        trade_records.append(record)
    trade_records = json.dumps(trade_records)
    trade_records = json.loads(trade_records)
    return trade_records