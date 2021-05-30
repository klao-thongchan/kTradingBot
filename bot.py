import websocket
import json
import pprint

#spot trading
SOCKET = "wss://stream.binance.com:9443/ws/btcbusd@kline_1m"
#future trading
FSOCKET = "wss://dstream.binancefuture.com/ws/btcusd@markPriceKline_1m"

def on_open(ws):
    print('connecting...')

def on_close(ws):
    print('---disconnected---')

def on_message(ws, message):
    print('get data:')
    json_message = json.loads(message)
    pprint.pprint(json_message) #pretty format

    candle = message['k'] #retrive data from wss:
    
    is_candle_closed = candle['x'] #return 'False'
    close = candle['c'] #return '35794.18000000'

    if is_candle_closed:
        print("price closed at {}".format(close))

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()