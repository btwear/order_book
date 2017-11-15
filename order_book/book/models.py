from django.db import models
from django.conf import settings

order_book_settings = settings.ORDER_BOOK_SETTINGS

# Create your models here.
class Order(models.Model):
    user_id = models.CharField(max_length=32)
    type = models.IntegerField(default=-1)
    price = models.IntegerField(default=-1)
    amount = models.IntegerField(default=-1)
    timestamp = models.IntegerField(default=0)
    token_id = models.IntegerField(default=-1)

class Trade(models.Model):
    buyer = models.CharField(max_length=32)
    seller = models.CharField(max_length=32)
    price = models.IntegerField(default=-1)
    amount = models.IntegerField(default=-1)
    timestamp = models.IntegerField(default=-1)
    token_id = models.IntegerField(default=-1)

#record trade in the time interval
class HistoryTrade(models.Model):
    price = models.FloatField(default=-1)
    amount = models.IntegerField(default=-1)
    timestamp = models.IntegerField(default=-1)
    token_id = models.IntegerField(default=-1)
    volumn = models.IntegerField(default=-1)

class Token(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=32)

    @classmethod
    def create_token(cls, token_id, token_name):
        token = cls.objects.create(id=token_id, name=token_name)
        return token
