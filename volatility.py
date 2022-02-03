#Volatility Breakout
import os,pyupbit
from pyupbit.exchange_api import Upbit
import numpy as np
import alg

def get_target_price(today, prev, K):
    today_open = today['open']
    prev_high = prev['high']
    prev_low = prev['low']
    target = today_open + (prev_high - prev_low) * K
    return target

def get_noise(price) :
    price_open = price['open']
    price_close = price['close']
    price_high = price['high']
    price_low = price['low']
    K = 1- (abs(price_open - price_close) / (price_high - price_low))
    return K

def init(ticker) : 
    df = pyupbit.get_ohlcv(ticker, interval="minutes60", count = 60, to="20220108 09:00:00")
    if df is None : 
        return 
    del df['value']
    del df['volume']
    df['target'] = 0
    df['noise'] = 0
    df['noise_ma20'] = 0
    df['earn_percent'] = 0
    df['earn_percent_sum'] = 0
    df['buy_signal'] = False
    for idx, row in df.iterrows() : 
        df.loc[idx, 'noise'] = get_noise(df.loc[idx]) 
    df['noise_ma20'] = df['noise'].rolling(window=20).mean()

    return df

def run_volatility(df) : 
    earn_sum = 0
    cnt = 0

    for idx, row in df.iterrows() : 
        buy_signal = False
        if cnt > 0 : 
            K = df.loc[idx, 'noise']
            target = get_target_price(df.iloc[cnt], df.iloc[cnt-1], K)
            df.loc[idx,'target'] = target 
            
            if target <= row['high'] and target >= row['low'] and alg.sma_bull_market(df, row['open']) is True : 
                buy_signal = True
                df.loc[idx,'buy_signal'] = buy_signal   
            
                if buy_signal is True : 
                    df.loc[idx,'earn_percent'] = row['close'] / row['open'] * 100 - 100.05
                    earn_sum += row['close'] / row['open']  * 100  - 100.05
                    df.loc[idx,'earn_percent_sum'] += earn_sum
        cnt += 1
    return df