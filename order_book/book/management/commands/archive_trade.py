from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache
from django.conf import settings
from book.models import Trade, Token, HistoryTrade
import time
import datetime

time_interval = settings.ORDER_BOOK_SETTINGS['archive_time_interval']

class Command(BaseCommand):
    def handle(self, *args, **options):
        token_object_list = list(Token.objects.all())
        token_list = []
        for i in token_object_list:
            token_list.append(i.id)
        archive_number = []
        for i in token_list:
            archive_number_key = 'archive_number_' + str(i)
            archive_number.append(cache.get_or_set(archive_number_key, -1, timeout=None))
        while True:
            for i, ti in enumerate(token_list):
                trade_number_key = 'trade_number_' + str(ti)
                trade_number = cache.get_or_set(trade_number_key, -1)
                if archive_number[i] < trade_number:
                    archive_number_key = 'archive_number_' + str(ti)
                    trade_keys = list(map(lambda x: 'Trade_' + str(ti) + '_' + str(x), range(archive_number[i] +1, trade_number +1)))
                    trades = cache.get_many(trade_keys).items()
                    trade_list = [x[1] for x in trades]
                    archive_number[i] = trade_number
                    cache.set(archive_number_key, trade_number, timeout=None)
                    for trade in trade_list:
                        ts = trade.timestamp
                        ts = int(ts - (ts % time_interval))
                        archive_key = 'Archive_' + str(ti) + '_' + str(ts)
                        ts_archieve = cache.get_or_set(archive_key, HistoryTrade(price=0,amount=0,timestamp=ts,token_id=ti,volumn=0), timeout=None)
                        ts_archieve.amount += trade.amount
                        ts_archieve.volumn += trade.amount * trade.price
                        ts_archieve.price = ts_archieve.volumn/ts_archieve.amount
                        cache.set(archive_key, ts_archieve, timeout=None)
                        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' archive: timestamp=' + str(ts))
            time.sleep(1)



def reduce_to_history(trade_list, timestamp):
    volumn = sum((i.price * i.amount) for i in trade_list)
    amount = sum(i.amount for i in trade_list)
    history_trade = HistoryTrade(price=volumn/amount,
                                 amount=amount,
                                 timestamp=timestamp,
                                 token_id=trade_list[0].token_id,
                                 volumn=volumn)
    return history_trade