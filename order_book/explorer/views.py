from django.shortcuts import render
from django.http import HttpResponse
from .explorer import *
import json

# Create your views here.
def get_order_book_view(request):
    token_id = int(request.GET.get('token_id', '-1'))
    page_size = int(request.GET.get('page_size', 25))
    order_data = get_order_book(page_size=page_size, token_id=token_id)
    order_book = {}
    order_book['sell'] = order_data[0]
    order_book['buy'] = order_data[1]
    order_book['total'] = [len(order_data[0]), len(order_data[1])]
    return HttpResponse(json.dumps(order_book), content_type="application/json")

def get_user_order_view(request, user_id):
    page_size = int(request.GET.get('page_size', 25))
    order = get_user_order_list(page_size=page_size, user_id=user_id)
    return HttpResponse(json.dumps(order), content_type="application/json")

def get_trade_data_view(request):
    since = int(request.GET.get('sicne', '0'))
    until = int(request.GET.get('until', '0'))
    token_id = int(request.GET.get('token_id', '-1'))
    trade = get_trade_record(since=since, until=until, token_id=token_id)
    return HttpResponse(json.dumps(trade), content_type="application/json")