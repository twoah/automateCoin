#Run
import os,pyupbit
from pyupbit.exchange_api import Upbit
import numpy as np
import alg, volatility
global server_url , access_key, secret_key, upbit

server_url = "https://api.upbit.com"
access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
upbit = Upbit(access_key, secret_key)

def run(): 
    idx = 0
    tickers = pyupbit.get_tickers(fiat="KRW")
    for ticker in tickers : 
        if idx == 1 : 
            df = volatility.init(ticker)
            volatility.run_volatility(df)
            print(ticker,'\n', df)
        idx+=1
run()