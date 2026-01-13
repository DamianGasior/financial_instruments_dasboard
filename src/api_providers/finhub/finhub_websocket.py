import websocket
import json
import streamlit as st
from queue import Queue
from src.utils import data_finhub_websocket
from src.api_providers.finhub import finhub_python
# from src.session_init import init_session_state



if "ws_open" not in st.session_state:
    st.session_state.ws_open = False

quotes_queue = Queue()


ws_connection = None

# symbols_set = set()


# symbols_set_indices = set()


# symbols_observed = ["AAPL", "AMZN","MSFT"]

symbol_quotes = {}  # niech do tego odowolouje sie st.sessionState
symbol_quotes_indices = {}
symbol_quotes_fx_pairs = {}
symbol_quotes_cmdty = {}
symbol_quotes_bond_yields = {}


print("Load module finhub_websocket...")

# if "latest_message" not in st.session_state:
#     st.session_state.latest_message = None


def size():
    size = quotes_queue.qsize()
    # print("Size is:", size)
    return size


def get_last_message():
    last_message = quotes_queue.get()
    print("last_message", last_message)
    return last_message


def get_specific_symbol():
    last_trades = get_last_message()
    if last_trades.get("type") == "trade":
        last_data = last_trades.get("data")
        print("cleaned_data", last_data)
        # tu od tej linni trzeba cos zaimplementowac co bedzie wylapwyalo wszsytkie uniwue symble z danego data
        for data in last_data:
            symbol = data.get("s")
            price = round(data.get("p"), 4)
            # symbols_set.add(symbol)
            if symbol in data_finhub_websocket.symbols_req_cryptos:
                symbol_quotes[symbol] = price
            elif symbol in data_finhub_websocket.symbols_oanda_indices:
                symbol_quotes_indices[symbol] = price
            elif symbol in data_finhub_websocket.symbols_oanda_ccy_pairs:
                symbol_quotes_fx_pairs[symbol] = price
            elif symbol in data_finhub_websocket.symbols_oanda_cmdty:
                symbol_quotes_cmdty[symbol] = price
            elif symbol in data_finhub_websocket.symbols_oanda_bond_yields:
                symbol_quotes_bond_yields[symbol] = price

        return (symbol, price)


def on_message(ws, message):
    message_loaded = json.loads(message)
    quotes_queue.put(message_loaded)


def on_error(ws, error):
    print(error)


def on_close(ws):
    st.session_state.ws_open = False
    print("### closed ###")


def on_open(ws):

    st.session_state.ws_open = True
    print("### websocket opened ###")

    for symbol in data_finhub_websocket.symbols_req_cryptos:
        ws.send(json.dumps({"type": "subscribe", "symbol": symbol}))

    for symbol in data_finhub_websocket.symbols_req_indices:
        ws.send(json.dumps({"type": "subscribe", "symbol": symbol}))

    for symbol in data_finhub_websocket.symbols_oanda_ccy_pairs:
        ws.send(json.dumps({"type": "subscribe", "symbol": symbol}))

    for symbol in data_finhub_websocket.symbols_oanda_cmdty:
        ws.send(json.dumps({"type": "subscribe", "symbol": symbol}))

    for symbol in data_finhub_websocket.symbols_oanda_bond_yields:
        ws.send(json.dumps({"type": "subscribe", "symbol": symbol}))

    # ws.send('{"type":"subscribe","symbol":"AMZN"}')
    # ws_connection.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')
    # ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}')


def start_web_socket():

    global ws_connection

    websocket.enableTrace(True)

    ws_connection = websocket.WebSocketApp(
        "wss://ws.finnhub.io?token=d4ee4ppr01qrumpf24fgd4ee4ppr01qrumpf24g0",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws_connection.on_open = on_open
    ws_connection.run_forever()
   
    # ws_connection.run_forever()



# zrobic jakas dokumentacje jak dziala ten caly webscoket i callbacki , by to ladnie zrozumiec.
