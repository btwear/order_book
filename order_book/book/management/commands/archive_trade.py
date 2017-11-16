from django.core.management.base import BaseCommand, CommandError
from book.models import Trade, Token, HistoryTrade
import time
import datetime

time_interval = 15

class Command(BaseCommand):
    def handle(self, *args, **options):
        last_timestamp = 0
        token_list = Token.objects.all()
        trade_buffer = []
        for i in token_list:
            trade_buffer.append([])
        if HistoryTrade.objects.exists():
            last_timestamp = list(HistoryTrade.objects.all().order_by('timestamp'))[-1].timestamp + time_interval

        while True:
            if (time.time() > (last_timestamp + time_interval + 5)):
                for ti in range(0, len(token_list)):
                    trade_buffer[ti] = Trade.objects.filter(timestamp__gte=last_timestamp, token_id=token_list[ti].id).order_by('timestamp')
                    if not trade_buffer[ti]:
                        continue
                    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' archive: timestamp=' + str(last_timestamp))
                    last_timestamp = int(trade_buffer[ti][0].timestamp / time_interval) *time_interval
                    trade_buffer[ti] = trade_buffer[ti].filter(timestamp__lt=last_timestamp+time_interval)
                    history_trade = reduce_to_history(list(trade_buffer[ti]), last_timestamp)
                    history_trade.save(force_insert=True)
                    last_timestamp = last_timestamp + time_interval
            else:
                time.sleep(5)



def reduce_to_history(trade_list, timestamp):
    volumn = sum((i.price * i.amount) for i in trade_list)
    amount = sum(i.amount for i in trade_list)
    history_trade = HistoryTrade(price=volumn/amount,
                                 amount=amount,
                                 timestamp=timestamp,
                                 token_id=trade_list[0].token_id,
                                 volumn=volumn)
    return history_trade