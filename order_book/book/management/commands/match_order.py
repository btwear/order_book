from django.core.management.base import BaseCommand, CommandError
from book.models import Order, Trade, Token, HistoryTrade
from operator import attrgetter
from itertools import chain
import time

BUY = 0
SELL = 1
class Command(BaseCommand):
    def handle(self, *args, **options):
        order_buffer = []
        #sell_pk, buy_pk is last pk that has been load to buffer
        order_pk = [0, 0]
        token_list = Token.objects.all()
        for token in token_list:
            order_buffer.append([[],[]])

        while True:
            #每一種幣別都需做一次
            for ti in range(0, len(order_buffer)):
                # 同步資料庫Order資料
                for i in [BUY, SELL]:
                    query_list = list(Order.objects.filter(pk__gt=order_pk[i], type=i, token_id=token_list[ti].id))
                    if not query_list:
                        break
                    order_buffer[ti][i] = list(chain(order_buffer[ti][i], query_list))
                    order_pk[i] = query_list[-1].pk
                    order_buffer[ti][i] = sorted(order_buffer[ti][i], key=attrgetter('price', 'pk'), reverse=not bool(i))
                #撮合交易
                while True:
                    buy = order_buffer[ti][BUY][0]
                    sell = order_buffer[ti][SELL][0]
                    #if match ok
                    if buy.price >= sell.price:
                        trade = Trade(buyer=buy.user_id,
                                      seller=sell.user_id,
                                      price=int((buy.price + sell.price) / 2),
                                      amount=min(buy.amount, sell.amount),
                                      timestamp=int(time.time()),
                                      token_id=token_list[ti].id)

                        #get small amount one in min_list[0], bigger one in min_list[1]
                        min_list = sorted([buy, sell], key=attrgetter('amount'))
                        min_list[1].amount -= trade.amount
                        #update order_buffer, delete
                        del order_buffer[ti][min_list[0].type][0]
                        order_buffer[ti][min_list[1].type][0] = min_list[1]

                        #update database
                        min_list[0].delete()
                        min_list[1].save()
                        trade.save(force_insert=True)
                    else:
                        break
                ti = ti + 1
            time.sleep(0.5)

