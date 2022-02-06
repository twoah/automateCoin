##Single Moving Average Strategy##
from signal import raise_signal

def sma_is_buysignal(df, price): #single moving average(5)
    last_ma5 = df['ma5'].iloc[-2]
    last_ma14 = df['ma14'].iloc[-2]
    if price > last_ma5 and price > last_ma14 : 
        return True 
    else :
        return False

def rsi_isbuysignal(prev) : 
    prev_rsi5 = prev['rsi5']
    prev_rsi14 = prev['rsi14']
    if prev_rsi5 > 30 and prev_rsi5 < 80 and prev_rsi14 > 30 and prev_rsi14 < 80 : 
        return True
    return False

def is_buysignal(df, fixed_percent): 
    buy_signal = False 
    prev_rsi = df['rsi5'].iloc[-1]
    prev = df.iloc[-1]
    print(prev)

    if sma_is_buysignal(df, prev['close']) is True and prev_rsi > 30 and prev_rsi < 70 :
        buy_signal = True    
    return buy_signal
    
    # if sma_is_buysignal(df, row['open']) is True and prev_rsi > 30 and prev_rsi < 80 : # today open == prev close
    #     fixed_percent = 1.02
    #     buy_signal = True
    #     df.loc[idx,'buy_signal'] = buy_signal
            
    #     if buy_signal is True : 
    #         if row['high'] < row['open'] * fixed_percent : 
    #             df.loc[idx,'earn_percent'] =  (fixed_percent - 1) * 100
    #             earn_sum += (fixed_percent - 1) * 100
    #             df.loc[idx,'earn_percent_sum'] += earn_sum
    #         else :
    #             df.loc[idx,'earn_percent'] =  ( row['close'] / row['open'] ) *  100  - 100.1
    #             earn_sum += (row['close'] / row['open']  * 100 ) - 100.1
    #             df.loc[idx,'earn_percent_sum'] += earn_sum

def is_buysignal_backtest(df) : 
    earn_sum = 0
    cnt = 0
    for idx, row in df.iterrows():    
        if cnt > 0 : 
            if sma_is_buysignal(df, row['open']) is True and rsi_isbuysignal(row) is True: # today open == prev close
                fixed_percent = 1.02
                buy_signal = True
                df.loc[idx,'buy_signal'] = buy_signal
                df.loc[idx,'earn_percent'] = row['high'] / row['open'] *  100  - 100.1
                # if buy_signal is True : 
                #     if row['high'] > row['open'] * fixed_percent : 
                #         df.loc[idx,'earn_percent'] =  (fixed_percent - 1) * 100
                #         earn_sum += (fixed_percent - 1) * 100
                #         df.loc[idx,'earn_percent_sum'] += earn_sum
                    # else :
                    #     df.loc[idx,'earn_percent'] =  ( row['close'] / row['open'] ) *  100  - 100.1
                    #     earn_sum += (row['close'] / row['open']  * 100 ) - 100.1
                    #     df.loc[idx,'earn_percent_sum'] += earn_sum
        cnt += 1
 
    return df

##Volatility Breakout Strategy##
def get_target_price(prev, K):
    prev_close = prev['close']
    prev_high = prev['high']
    prev_low = prev['low']
    target = prev_close - (prev_high - prev_low) * K
    return target

def volatility_is_buysignal(df):

    K = 0.6  #K = df.loc[idx, 'noise']
    target = get_target_price(df.iloc[-1], K)

    return False

def volatility_is_buysignal_backtest(df) : 
    earn_sum = 0
    cnt = 0

    
    for idx, row in df.iterrows() : 
        buy_signal = False
        if cnt > 0 : 
            K = 0.6  #K = df.loc[idx, 'noise']
            target = get_target_price(df.iloc[cnt-1], K)
            df.loc[idx,'target'] = target 
            
            if target <= row['high'] and target >= row['low']  and rsi_isbuysignal(row) is True : # and sma_is_buysignal(df, row['open']) is True 
                buy_signal = True
                df.loc[idx,'buy_signal'] = buy_signal

                if buy_signal is True : 
                    df.loc[idx,'earn_percent'] = row['close'] / target * 100 - 100.1
                    earn_sum += row['close'] / target  * 100  - 100.1
                    df.loc[idx,'earn_percent_sum'] += earn_sum
        cnt += 1
    return 

