from .models import *
import random
from django.core.cache import cache

def create_token(token_id, token_name):
    Token.objects.create(id=token_id, name=token_name)

#make a order
def order(user_id, token_id, type, price, amount, timestamp):
    token_list = list(Token.objects.all())
    token_id_list = []
    for i in token_list:
        token_id_list.append(i.id)
    if token_id not in token_id_list:
        raise Exception('no such token')
    else:
        key = cache.get_or_set('order_number_' + str(token_id), -1, timeout=None)
        key += 1
        order = Order(user_id=user_id,token_id=token_id,type=type,price=price,amount=amount,timestamp=timestamp)
        cache.get_or_set('Order_' + str(token_id) + '_' + str(key), order, timeout=None)
        return cache.incr('order_number_' + str(token_id))

def mk_random_orders(n, user_list = [], token_id = 0,type_prob = 0.5, price_bias = 2000, price_fluct = 0.1, amount_bias = 500, amount_fluct = 0.5, timestamp_start = 0, time_interval = 10):
    if not Token.objects.exists():
        create_token(0, 'test')
    if not user_list:
        user_list.append('random')
    else:
        user_list = list(user_list)
        tmp_list = []
        for user in user_list:
            tmp_list.append(str(user))
        user_list = tmp_list
    timestamp = timestamp_start
    for i in range(0, n):
        user_id = random.choice(user_list)
        type = 0
        if(random.random() > type_prob):
            type = 1
        price = random.randint(int(price_bias * (1 - price_fluct)), int(price_bias * (1 + price_fluct)))
        amount = random.randint(int(amount_bias * (1 - amount_fluct)), int(amount_bias + (1 + amount_fluct)))
        order(user_id=user_id,
              token_id=token_id,
              type=type,
              price=price,
              amount=amount,
              timestamp=timestamp)
        timestamp = timestamp + time_interval

def mk_random_trades(n, user_list = [], token_id = 0, price_bias = 2000, price_fluct = 0.1, amount_bias = 500, amount_fluct = 0.5, timestamp_start = 0, time_interval = 1):
    trade_number = cache.get_or_set('trade_number', -1, timeout=None)
    if not Token.objects.exists():
        create_token(0, 'test')
    if not user_list:
        user_list.append('random')
    else:
        user_list = list(user_list)
        tmp_list = []
        for user in user_list:
            tmp_list.append(str(user))
        user_list = tmp_list
    timestamp = timestamp_start
    price = price_bias
    for i in range(0, n):
        buyer = random.choice(user_list)
        seller = random.choice(user_list)
        price = random.randint(int(price * (1 - price_fluct)), int(price * (1 + price_fluct)))
        amount = random.randint(int(amount_bias * (1 - amount_fluct)), int(amount_bias + (1 + amount_fluct)))
        trade = Trade(buyer=buyer,seller=seller,token_id=token_id,price=price,amount=amount,timestamp=timestamp)
        trade_number = cache.incr('trade_number')
        trade_key = 'Trade_' + str(trade_number)
        cache.get_or_set(trade_key, trade)
        timestamp = timestamp + time_interval

def clean_table(tables):
    for table in tables:
        table.objects.all().delete()

def clean_database():
    clean_table([Order, Trade, HistoryTrade, Token])