from finlab.market import Market
from .tw import TWMarket
from .us import USMarket
from .rotc import ROTCMarket

def get_market_by_name(name:str) -> Market:
    if name.lower() == 'tw_stock':
        return TWMarket()
    if name.lower() == 'us_stock':
        return USMarket()
    if name.lower() == 'rotc_stock':
        return ROTCMarket()
    raise ValueError('Unknown market name.')