from django.shortcuts import render
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from.orderbook import *
import json
# Create your views here.

def order_view(request):
    try:
        data = request.POST
        user_id = data['user_id']
        token_id = data['token_id']
        type = data['type']
        price = data['price']
        amount = data['amount']
        timestamp = data['timestamp']
        order(user_id=user_id,
              token_id=token_id,
              type=type,
              price=price,
              amount=amount,
              timestamp=timestamp)
        return HttpResponse(1)
    except Exception:
        return HttpResponse(0)