# ------Below are symbols which are used as input for websocket on open ----


symbols_req_cryptos = [
    "BINANCE:ETHUSDT",
    "BINANCE:BTCUSDT",
    "BINANCE:SOLUSDT",
    "BINANCE:LTCUSDT",
]


symbols_req_indices = ["^GSPC", "^DJI", "^NDX", "^N100", "^GDAXI", "^FTSE"]


# ------Below are symbols which are mapped to  a specifc broker
# webscoket does provide CFD's for futures for indices, form  Oanda ( which is an US broker for Forex and CFD)
# real data / qutoes from exchanges are very expensive ( what requires hihg fees to exchanges ) so websocket
# isntead of providing quotes for indices does provides quotes for CFD's which are very close to the quotes from exchanges
# for S&P , NASDAQ and so on, Finhub would need to have a paid license
# https://chatgpt.com/c/69287cc3-451c-832a-8393-188c97f83f19

# symbols below will be used as input request used to websocket
# source : https://finnhub.io/api/v1/forex/symbol?exchange=oanda&token=d4ee4ppr01qrumpf24fgd4ee4ppr01qrumpf24g0

symbols_oanda_indices = [
    "OANDA:NAS100_USD",
    "OANDA:DE30_EUR",
    "OANDA:US30_USD",
    "OANDA:UK100_GBP",
    "OANDA:SPX500_USD",
]


symbols_oanda_ccy_pairs = [
    "OANDA:EUR_USD",
    "OANDA:USD_JPY",
    "OANDA:USD_PLN",
    "OANDA:USD_HKD",
]


symbols_oanda_cmdty = [
    "OANDA:XAU_USD",
    "OANDA:XAG_USD",
    "OANDA:WTICO_USD",
    "OANDA:BCO_USD",
    "OANDA:XCU_USD",
    "OANDA:NATGAS_USD",
]


symbols_oanda_bond_yields = ["OANDA:USB02Y_USD", "OANDA:USB05Y_USD", "OANDA:USB10Y_USD"]

# symbol mappings presented as dict, where the mapping is one to many, means  :
# name of the underlying like S&P 500 - can have many  values, as ticks can be provided by different brokers, like oanda, forex.com, etc


symbol_common_names_mappings = {
    "Bitcoin": ["BINANCE:BTCUSDT"],
    "Ether": ["BINANCE:ETHUSDT"],
    "Solana": ["BINANCE:SOLUSDT"],
    "Litecoin": ["BINANCE:LTCUSDT"],
    "S&P 500": ["OANDA:SPX500_USD", "^GSPC"],
    "Dow 30": ["OANDA:US30_USD"],
    "Nasdaq": ["OANDA:NAS100_USD"],
    "FTSE 100": ["OANDA:UK100_GBP"],
    "DAX": ["OANDA:DE30_EUR"],
    "US 2Y": ["OANDA:USB02Y_USD"],
    "US 5Y": ["OANDA:USB05Y_USD"],
    "US 10Y": ["OANDA:USB10Y_USD"],
    "EUR/USD" : ["OANDA:EUR_USD"],
    "USD/JPY" : ["OANDA:USD_JPY"],
    "USD/PLN" : ["OANDA:USD_PLN"],
    "USD/HKD" : ["OANDA:USD_HKD"],
    "Gold" : ["OANDA:XAU_USD"],
    "Silver" : ["OANDA:XAG_USD"],
    "Crude Oil" : ["OANDA:WTICO_USD"],
    "Brent" : ["OANDA:BCO_USD"],
    "NaturalGas" : ["OANDA:NATGAS_USD"],
    "Copper" : ["OANDA:XCU_USD"]
}


def find_the_right_name(ticker_symbol):
    for key, value in symbol_common_names_mappings.items():
        for ticker in value:
            if ticker_symbol == ticker:
                return key




