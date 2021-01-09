import os, sched, sys, time
from datetime import datetime
from models.CoinbasePro import CoinbasePro

action = 'wait'
last_action = ''

def executeJob(sc, market, granularity): 
    global action, last_action

    #print(datetime.now(), 'retrieving market data for', market, 'for analysis')
    coinbasepro = CoinbasePro(market, granularity)
    coinbasepro.addEMABuySignals()
    coinbasepro.addMACDBuySignals()
    df = coinbasepro.getDataFrame()

    df_last = df.tail(1)
    #sma50 = float(df_last['sma50'].values[0])
    #sma200 = float(df_last['sma200'].values[0])
    ema12gtema26co = bool(df_last['ema12gtema26co'].values[0])
    macdgtsignal = bool(df_last['macdgtsignal'].values[0])
    ema12ltema26co = bool(df_last['ema12ltema26co'].values[0])
    macdltsignal = bool(df_last['macdltsignal'].values[0])
    obv_pc = float(df_last['obv_pc'].values[0])

    if ema12gtema26co == True and macdgtsignal == True and obv_pc >= 2 and last_action != 'buy':
        action = 'buy'
    elif ema12ltema26co == True and macdltsignal == True and last_action != 'sell':
        action = 'sell'
    else:
        action = 'wait'

    print(df_last.index.format(), 'ema12:' + str(df_last['ema12'].values[0]), 'ema26:' + str(df_last['ema26'].values[0]), ema12gtema26co, ema12ltema26co, 'macd:' + str(df_last['macd'].values[0]), 'signal:' + str(df_last['signal'].values[0]), macdgtsignal, macdltsignal, obv_pc, action)
    #print(datetime.now(), 'current action for', market, 'is to', action)

    if action == 'buy':
        print ('>>> BUY <<<')
        print (df_last)
    elif action == 'buy':
        print ('>>> SELL <<<')
        print (df_last)

    last_action = action
    s.enter(granularity - 1, 1, executeJob, (sc, market, granularity))

try:
    market = 'BTC-GBP'
    granularity = 3600 # 1 hour

    print("Python Crypto Bot using Coinbase Pro API\n")
    print(datetime.now(), 'started for market', market, 'using interval', granularity)

    s = sched.scheduler(time.time, time.sleep)
    s.enter(1, 1, executeJob, (s, market, granularity))
    s.run()
except KeyboardInterrupt:
    print(datetime.now(), 'closed')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)