import os
from pyupbit.exchange_api import upbit

def get_balance(ticker): 
    balance  = upbit.get_balance(ticker)
    return balance

def get_buy_average(ticker) : 
    balances = upbit.get_balance(ticker)
    for b in balances : 
        if b['currency'] == ticker:
            if b['avg_buy_price'] is not None:
                return float(b['avg_buy_price'])
            else: 
                return 0
                
def buy_limit_order(ticker, price, amount): 
    order = upbit.buy_limit_order(ticker, price, amount)
    print(ticker , " 지정가 매수 : " , order)

def buy_market_order(ticker, amount):
    order = upbit.buy_market_order(ticker, amount)
    print(ticker , " 시장가 매수 : " , order)

def sell_limit_order(ticker, price, amount): 
    order = upbit.sell_limit_order(ticker, price, amount)
    print(ticker , " 지정가 매도 : " , order)

def sell_market_order(ticker, amount): 
    order = upbit.sell_market_order(ticker, amount)
    print(ticker , " 시장가 매도 : " , order)

def cancel_order(cancel_id):
    cancel_order = upbit.cancel_order(cancel_id)
    print("주문 취소 : " ,cancel_id, " " , cancel_order)
