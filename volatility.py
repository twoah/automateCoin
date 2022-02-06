import alg
#Volatility Breakout
def get_target_price(prev, K):
    prev_close = prev['close']
    prev_high = prev['high']
    prev_low = prev['low']
    target = prev_close + (prev_high - prev_low) * K
    return target

def is_buysignal(df) : 
    earn_sum = 0
    cnt = 0
    for idx, row in df.iterrows() : 
        buy_signal = False
        if cnt > 0 : 
            K = df['noise_ma14'].iloc[cnt-1]
            target = get_target_price(df.iloc[cnt-1], K)
            df.loc[idx,'target'] = target
        cnt += 1

    cnt = 0
    for idx, row in df.iterrows():    
        if cnt > 0 : 
            prev_rsi = df['rsi'].iloc[cnt-1]
            if alg.sma_bull_market(df, row['open']) is True and prev_rsi > 30: # today open == prev close
                fixed_percent = 1.02
                buy_signal = True
                df.loc[idx,'buy_signal'] = buy_signal
                    
                if buy_signal is True : 
                    if row['high'] < row['open'] * fixed_percent : 
                        df.loc[idx,'earn_percent'] =  (fixed_percent - 1) * 100
                        earn_sum += (fixed_percent - 1) * 100
                        df.loc[idx,'earn_percent_sum'] += earn_sum
                    else :
                        df.loc[idx,'earn_percent'] =  ( row['close'] / row['open'] ) *  100  - 100.1
                        earn_sum += (row['close'] / row['open']  * 100 ) - 100.1
                        df.loc[idx,'earn_percent_sum'] += earn_sum
        cnt += 1
 
    return df