# order_book

## Installation
### Requirement
- virtualenv
- python3
- mysql
- redis

## Setup Environment

modify settings.py, set up your mysql username and password in &lt;username&gt;, &lt;password&gt;
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'order_book',
        'USER': '<user>',
        'PASSWORD': '<password>',
    }
}
```
create database in mysql name 'order_book'
```
mysql -u <username> -p
<your password>
>> create database order_book;
```
set up django environment
```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
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
python manage.py archive_trades
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
## install Web server
```
npm install live-server
```

## Start Web server
```
live-server ./web
```
