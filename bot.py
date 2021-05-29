import websocket
import json
import pprint

SOCKET = "wss://stream.binance.com:9443/ws/btcbusd@kline_1m"
FSOCKET = "wss://dstream.binancefuture.com/ws/btcusd@markPriceKline_1m"

def on_open(ws):
    print('connecting...')

def on_close(ws):
    print('---disconnected---')

def on_message(ws, message):
    print('get data:')
    json_message = json.loads(message)
    pprint.pprint(json_message)

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()