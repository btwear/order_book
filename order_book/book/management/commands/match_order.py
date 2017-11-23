from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache
from book.models import Order, Trade, Token, HistoryTrade
from operator import attrgetter
from itertools import chain
import time
import datetime

BUY = 0
SELL = 1
class Command(BaseCommand):
    def handle(self, *args, **options):
        order_buffer = []
        #sell_pk, buy_pk is last pk that has been load to buffer
        token_object_list = list(Token.objects.all())
        token_list = []
        for i in token_object_list:
            token_list.append(i.id)
            order_buffer.append([[],[]])

        while True:
            #build up order_buffer
            for i, ti in enumerate(token_list):
                keys = cache.keys('Order_' + str(ti) + '_*')
                tmp_order_list = cache.get_many(keys).items()
                order_buffer[ti] = [[],[]]
                #add new orders into order_buffer
                for ord in tmp_order_list:
                    sell = int(ord[1].type)
                    #insert order into sorted order_buffer
                    idx = -1
                    for idx, j in enumerate(order_buffer[ti][sell]):
                        order = j[1]
                        if (not sell and (ord[1].price > order.price)) or (sell and (ord[1].price < order.price)):
                            idx -= 1
                            break
                    idx += 1
                    order_buffer[i][sell].insert(idx, list(ord))

            for i, ti in enumerate(token_list):
                #match trade
                trade_number = cache.get_or_set('trade_number_' + str(ti), -1, timeout=None)
                while True:
                    try:
                        buy = order_buffer[i][BUY][0][1]
                        sell = order_buffer[i][SELL][0][1]
                    except:
                        pass
                        break
                    #if match ok
                    if buy.price >= sell.price:
                        trade = Trade(buyer=buy.user_id,
                                      seller=sell.user_id,
                                      price=int((buy.price + sell.price) / 2),
                                      amount=min(buy.amount, sell.amount),
                                      timestamp=int(time.time()),
                                      token_id=ti)

                        #get small amount one in min_list[0], bigger one in min_list[1]
                        min_list = sorted([buy, sell], key=attrgetter('amount'))
                        min_list[1].amount -= trade.amount
                        #update order_buffer, delete
                        order_key_to_delete = order_buffer[i][min_list[0].type][0][0]
                        order_key_to_update = order_buffer[i][min_list[1].type][0][0]
                        del order_buffer[i][min_list[0].type][0]
                        order_buffer[i][min_list[1].type][0][1] = min_list[1]

                        #update cache
                        cache.delete(order_key_to_delete)
                        cache.set(order_key_to_update, min_list[1], timeout=None)
                        trade_number = cache.incr('trade_number_' + str(ti))
                        trade_key = 'Trade_' + str(ti) + '_' + str(trade_number)
                        cache.set(trade_key, trade, timeout=None)
                        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' match: price=' + str(trade.price) + ', amount = ' + str(trade.amount))
                    else:
                        break
            time.sleep(0.5)

