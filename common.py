
import pyupbit
import pandas
from datetime import datetime

def init(ticker, interval) : 
    df = pyupbit.get_ohlcv(ticker, interval, count = 240)
    if df is None : 
        return 
    del df['value']
    del df['volume']
    df['target'] = 0
    df['ma5'] = df['close'].rolling(5).mean()
    df['ma14'] = df['close'].rolling(14).mean()
    df['earn_percent'] = 0
    df['earn_percent_sum'] = 0
    df['buy_signal'] = False
    rsi(df)
    
    df['noise'] = 0
    df['noise_ma14'] = 0
    for idx, row in df.iterrows() : 
        df.loc[idx, 'noise'] = get_noise(df.loc[idx]) 
    df['noise_ma14'] = df['noise'].rolling(window=14).mean()
    return df

def rsi(df):
    period = 5
    closedata = df['close']
    delta = closedata.diff()
    ups, downs = delta.copy(), delta.copy()
    ups[ups < 0] = 0 
    downs[downs > 0] = 0
    au = ups.ewm(com = period-1, min_periods = period).mean() 
    ad = downs.abs().ewm(com = period-1, min_periods = period).mean()
    RS = au/ad 
    RSI = pandas.Series(100 - (100/(1+RS)))
    df['rsi5'] = RSI

    period = 14
    closedata = df['close']
    delta = closedata.diff()
    ups, downs = delta.copy(), delta.copy()
    ups[ups < 0] = 0 
    downs[downs > 0] = 0
    au = ups.ewm(com = period-1, min_periods = period).mean() 
    ad = downs.abs().ewm(com = period-1, min_periods = period).mean()
    RS = au/ad 
    RSI = pandas.Series(100 - (100/(1+RS)))
    df['rsi14'] = RSI
    return df

def get_noise(price) :
    price_open = price['open']
    price_close = price['close']
    price_high = price['high']
    price_low = price['low']

    if price_high - price_low != 0 : 
        K = 1- abs(price_open - price_close) / (price_high - price_low)
    else :
        K = 0.5
    return K

def df_to_excel(ticker, df): 
    excel_name = ticker + "_" + str(datetime.today().strftime("%Y%m%d")) + ".xlsx"
    df.to_excel(excel_name)
    return 

#시작시간 
def get_start_time(ticker, interval): 
    df = pyupbit.get_ohlcv(ticker, interval=interval, count=1)
    start_time = df.index[0]
    return start_time 

#현재 가격 가져오기
def get_current_price(ticker) : 
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

