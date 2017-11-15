from django.core.management.base import BaseCommand, CommandError
from book.models import Trade, Token, HistoryTrade
import time

time_interval = 15

class Command(BaseCommand):
    def handle(self, *args, **options):
        last_timstamp = 0
        token_list = Token.objects.all()
        trade_buffer = []
        for i in token_list:
            trade_buffer.append([])
        if not HistoryTrade.objects.exists():
            first_trade = Trade.objects.all()[0]
            last_timestamp = int(first_trade.timestamp/time_interval) * time_interval
        else:
            last_timestamp = HistoryTrade.objects.all()[-1].timestamp + time_interval

        while True:
            next_timestamp = last_timestamp + time_interval
            if (time.time() > (last_timestamp + int(time_interval / 3))):
                for ti in range(0, len(token_list)):
                    trade_buffer[ti] = Trade.objects.filter(timestamp__gte=last_timestamp, timestamp__lt=next_timestamp, token_id=token_list[ti].id)
                    if not trade_buffer[ti]:
                        continue
                    else:
                        history_trade = reduce_to_history(trade_buffer[ti], last_timestamp)
                        history_trade.save(force_insert=True)
            else:
                time.sleep(int(time_interval/6))
                continue
            last_timestamp = next_timestamp



def reduce_to_history(trade_list, timestamp):
    volumn = sum((i.price * i.amount) for i in trade_list)
    amount = sum(i.amount for i in trade_list)
    history_trade = HistoryTrade(price=volumn/amount,
                                 amount=amount,
                                 timestamp=timestamp,
                                 token_id=trade_list[0].token_id,
                                 volumn=volumn)
    return history_trade