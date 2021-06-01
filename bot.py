import websocket
import json
import pprint
import talib
import numpy

#binance trading API
from binance.client import Client
from binance.enums import *
#create trading client
import config #from config.py
client = Client(config.API_KEY, config.API_SECRET, tld='us')

#spot trading
SOCKET = "wss://stream.binance.com:9443/ws/btcbusd@kline_1m"
#future trading
FSOCKET = "wss://dstream.binancefuture.com/ws/btcusd_perp@markPriceKline_1m"

closes = [] #for getting closed price

#for TA-Lib
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'BTCBUSD'
TRADE_QUANTITY = 0.05

in_position = False

def on_open(ws):
    print('connecting...')

def on_close(ws):
    print('---disconnected---')

def on_message(ws, message):
    global closes

    print('get data:')
    json_message = json.loads(message)
    pprint.pprint(json_message) #pretty format

    candle = json_message['k'] #retrive data from wss:
    
    is_candle_closed = candle['x'] #return 'False'
    close = candle['c'] #return '35794.18000000'

    if is_candle_closed:
        print("price closed at {}".format(close))
        close.append(float(close))
        print(closes)

        if len(closes) > RSI_PERIOD: #start trading when data > 14
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            last_rsi = rsi[-1] #grab the last RSI for trading

            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print("SELL SIGNAL")
                    #binance sell order logic below
            
            if last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("already in position")
                print("BUY SIGNAL")
                #binance buy order logic below

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()