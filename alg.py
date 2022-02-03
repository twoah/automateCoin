##Single Moving Average##
import os,pyupbit
from pyupbit.exchange_api import Upbit
import requests

server_url = "https://api.upbit.com"
access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
upbit = Upbit(access_key, secret_key)

def sma_bull_market(df, price): #single moving average(5)
    ma5 = df['close'].rolling(5).mean()
    ma14 = df['close'].rolling(14).mean()
    last_ma5 = ma5[-2]
    last_ma14 = ma14[-2]
    if price > last_ma5 and price > last_ma14: 
        return True 
    else :
        return False