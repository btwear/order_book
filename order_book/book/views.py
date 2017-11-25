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
        token_id = int(data['token_id'])
        type = int(data['type'])
        price = int(data['price'])
        amount = int(data['amount'])
        timestamp = int(data['timestamp'])
        suss = order(user_id=user_id,
                     token_id=token_id,
                     type=type,
                     price=price,
                     amount=amount,
                     timestamp=timestamp)
        return HttpResponse(suss)
    except Exception:
        return HttpResponse(suss)