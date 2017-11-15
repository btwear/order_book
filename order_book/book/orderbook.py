from .models import *
import random

def order(user_id, token_id, type, price, amount, timestamp):
    Order.objects.create(user_id=user_id,
                              token_id=token_id,
                              type=type,
                              price=price,
                              amount=amount,
                              timestamp=timestamp)

def mk_random_orders(n, token_id = 0,type_prob = 0.5, price_bias = 2000, price_fluct = 0.1, amount_bias = 500, amount_fluct = 0.5, timestamp_start = 0, time_interval = 10):
    user_id='random'
    timestamp = timestamp_start
    for i in range(0, n):
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

def mk_random_trade(n, token_id = 0, price_bias = 2000, price_fluct = 0.1, amount_bias = 500, amount_fluct = 0.5, timestamp_start = 0, time_interval = 1):
    user_id = 'random_trade'
    timestamp = timestamp_start
    price = price_bias
    for i in range(0, n):
        price = random.randint(int(price * (1 - price_fluct)), int(price * (1 + price_fluct)))
        amount = random.randint(int(amount_bias * (1 - amount_fluct)), int(amount_bias + (1 + amount_fluct)))
        trade = Trade(user_id=user_id,token_id=token_id,price=price,amount=amount,timestamp=timestamp)
        trade.save(force_insert=True)
        timestamp = timestamp + time_interval

def clean_table(tables):
    for table in tables:
        table.objects.all().delete()

def clean_database():
    clean_table([Order, Trade, HistoryTrade, Token])