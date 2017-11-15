# order_book

## Installation
### Requirement
- virtualenv
- python3

## Setup Environment
```
virtualenv -p python3 venv
source venv/bin/activate
pip install django
cd order_book
python manage.py makemigrations
python manage.py migrate
```

## Setup Server
```
python manage.py runserver
```

## Start maching
```
python manage.py match_order
```

## Archive trade record
```
python manage.py archive_trade
```

## Generate random order or trade
First start python in django shell
```
python manage.py shell
```
Then call random order generate function
```
from book.orderbook import *
mk_random_orders(n)
```
Which n is number of order

If you want to generate random trade
```
from book.orderbook import *
mk_random_trade(n)
```
