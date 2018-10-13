"""Module for rest and websocket utilities"""
import re
import time
from datetime import datetime

def create_cid():
    """Create a new Client order id. Based on timestamp multiplied to 100k to
    make it improbable that two actions are assigned the same cid.

    Returns
    -------
    int
        A integer number equal to the current timestamp * 10 mill.
    """
    now = datetime.utcnow()
    return int(float(now.strftime("%s.%f"))*10000000)

def cid_to_date(cid):
    """Converts a cid to date string YYYY-MM-DD

    Parameters
    ----------
    cid : int
        A cid as it is generated by the function ``utils.create_cid()``

    Returns
    -------
    str
        A string formated date (e.g. YYYY-MM-DD, 2018-10-01)
    """
    return datetime.utcfromtimestamp(
        cid/10000000.0
    ).strftime("%Y-%m-%d")

def get_nonce(multiplier):
    """Returns a nonce used in authentication.
    Nonce must be an increasing number. If other frameworks have used
    higher numbers you might need to increase the nonce_multiplier.
    """
    return str(float(time.time()) * multiplier)

TRADE_SYMBOL_MISSING = re.compile(r"^[a-zA-Z]{6}$")
"""Regular explression used to match trade symbols without a leading t (e.g. BTCUSD)"""

FUNDING_SYMBOL_MISSING = re.compile(r"^[a-zA-Z]{3}$")
"""Regular explression used to match funcing symbols without a leading f (e.g. BTC)"""

def order_symbol(symbol, capital=True):
    """Convinience function for skipping t or f before symbols for trade and
    funding orders.

    Parameters
    ----------
    symbol : str
        Symbol as a string. For example BTCUSD for trades or BTC for funding.

    capital : bool
        Boolean to capitalize trading and funding symbols. Capilat symbols are
        required in v2 of the Bitfinex API. Default: True
    """
    if capital:
        _symbol = symbol.upper()
    else:
        _symbol = symbol

    if TRADE_SYMBOL_MISSING.match(symbol):
        return "t{}".format(_symbol)
    elif FUNDING_SYMBOL_MISSING.match(symbol):
        return "f{}".format(_symbol)

    return symbol
