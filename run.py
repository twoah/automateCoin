#Run
import os,pyupbit
from pyupbit.exchange_api import Upbit
import alg, common, order
import time, datetime
global server_url, access_key, secret_key, upbit
global ticker, interval

server_url = "https://api.upbit.com"
access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
upbit = Upbit(access_key, secret_key)

ticker = "KRW-XRP"
interval = "minute60"
rate_minus = 0.95

def alg_backtest(ticker, df): 
    sum = 0
    #alg.is_buysignal(df, 0.2)
    alg.volatility_is_buysignal_backtest(df)

    if df['earn_percent_sum'].iloc[-1] != 0 :
        sum += df['earn_percent_sum'].iloc[-1] 
        print(ticker, df['earn_percent_sum'].iloc[-1])

    print(ticker, '\n', df)
    common.df_to_excel(ticker, df)

def alg(df, start_time, end_time): 

    i = 0    
    K = 0.6     #K = df.loc[idx, 'noise']
    prev = df.iloc[-1]
    target = alg.get_target_price(df.iloc[-1], K)

    while i <3 : 
        now = datetime.date.now() 
        current_price = alg.get_current_price(ticker)
        time.sleep(0.5)

        #매수 1차
        if i==0 and target * 0.98 < current_price < target * 1.02 and alg.rsi_isbuysignal(prev) is True: 
            order.buy_market_order(ticker, 10)
            buy_average = order.get_buy_average(ticker)
            time.sleep(1)
            i+=1 
            print("매수 1차 : OK , 매수평균가 : ", buy_average, " 현재 시가: ", current_price)

        #매수 2차    
        if i==1 and current_price < buy_average * rate_minus : 
            upbit.buy_market_order(ticker, 10)
            time.sleep(1)
            buy_average = order.get_buy_average(ticker)
            i+= 1 
            print("매수 2차 : OK , 매수평균가 : ", buy_average, " 현재 시가: ", current_price)
        
        if i==2 and current_price < buy_average * rate_minus : 
            upbit.buy_market_order(ticker, 10)
            time.sleep(1)
            buy_average = order.get_buy_average(ticker)
            i+= 1 
            print("매수 3차 : OK , 매수평균가 : ", buy_average, " 현재 시가: ", current_price)

        if now > end_time :
            coin = order.get_balance(ticker)
            upbit.sell_market_order(ticker, coin)
            time.sleep(1)                
        
    return 

def run() : 
    while True : 
        start_time = common.get_start_time(ticker, interval)
        now = datetime.datetime.now() 
        end_time = start_time + datetime.timedelta(minutes=60)-datetime.timedelta(seconds=5)
        print(start_time, now, end_time)
        
        if start_time < now < end_time : 
            df = common.init(ticker, interval)
            #alg(df, start_time, end_time)
            print(df)
        time.sleep(60)

run()
