import datetime
import pandas as pd
from finlab import data
from finlab.market import Market


class ROTCMarket(Market):
    """興櫃股票市場類別
    
    興櫃股票的特性：
    - 沒有還原價（無除權息、增減資等公司行為調整）
    - 交易時間與上市櫃相同
    - 資料來源為 rotc_price 系列
    
    使用方式：
        from finlab.markets.rotc import ROTCMarket
        from finlab.backtest import sim
        
        close = data.get('rotc_price:收盤價')
        position = ...  # 計算持倉
        
        report = sim(position=position, market=ROTCMarket(), ...)
    """

    @staticmethod
    def get_freq():
        return '1d'

    @staticmethod
    def get_name():
        return 'rotc_stock'

    @staticmethod
    def get_benchmark() -> pd.Series:
        return data.get('benchmark_return:發行量加權股價報酬指數').squeeze()

    @staticmethod
    def get_asset_id_to_name():
        """取得興櫃股票代碼對應名稱
        
        注意：興櫃股票可能沒有在 security_categories 中，
        此方法會嘗試從 rotc_price 的欄位名稱推斷
        """
        try:
            # 先嘗試從 security_categories 取得
            categories = data.get('security_categories')
            stock_names = dict(
                zip(categories.reset_index()['stock_id'], categories['name']))
            return stock_names
        except Exception:
            return {}
    
    @staticmethod
    def get_industry():
        """取得興櫃股票產業分類
        """
        try:
            categories = data.get('security_categories')
            industry = dict(
                zip(categories.reset_index()['stock_id'], categories['category']))
            return industry
        except Exception:
            return {}

    def get_price(self, trade_at_price, adj=True):
        """取得興櫃股票價格
        
        Args:
            trade_at_price: 價格類型 ('open', 'close', 'high', 'low', 'volume') 
                           或 pd.DataFrame/pd.Series
            adj: 是否使用還原價（興櫃股票無還原價，此參數會被忽略）
            
        Returns:
            pd.DataFrame: 興櫃股票價格資料
            
        Note:
            興櫃股票沒有還原價，因此 adj 參數會被忽略，
            永遠返回原始價格。
        """
        if isinstance(trade_at_price, pd.Series):
            return trade_at_price.to_frame()

        if isinstance(trade_at_price, pd.DataFrame):
            return trade_at_price

        if isinstance(trade_at_price, str):
            if trade_at_price == 'volume':
                return data.get('rotc_price:成交股數')

            # 興櫃股票沒有還原價，永遠使用原始價格
            price_name = {
                'open': '開盤價', 
                'close': '收盤價', 
                'high': '最高價', 
                'low': '最低價'
            }[trade_at_price]

            price = data.get(f'rotc_price:{price_name}')
            return price

        raise ValueError('trade_at_price is not allowed (accepted types: pd.DataFrame, pd.Series, str).')

    @staticmethod
    def get_market_value():
        """興櫃股票市值"""
        return pd.DataFrame()
    
    def market_close_at_timestamp(self, timestamp=None):
        """取得市場收盤時間"""
        if not isinstance(timestamp, pd.Timestamp) and timestamp is not None:
            timestamp = pd.Timestamp(timestamp).tz_localize('Asia/Taipei')

        if timestamp is None:
            timestamp = pd.Timestamp.now().tz_localize('Asia/Taipei')

        if timestamp.tzinfo is None:
            timestamp = timestamp.tz_localize('Asia/Taipei')
        
        market_close = pd.Timestamp(timestamp.date()) + pd.Timedelta('15:00:00')
        return market_close.tz_localize('Asia/Taipei')
    
    @staticmethod
    def tzinfo():
        return datetime.timezone(datetime.timedelta(hours=8))
    
    def get_reference_price(self) -> dict:
        """取得興櫃股票參考價"""
        try:
            # 使用最近一日的收盤價作為參考價
            close = data.get('rotc_price:收盤價')
            if close is not None and not close.empty:
                return close.iloc[-1].dropna().to_dict()
        except Exception:
            pass
        return {}

    @staticmethod
    def get_odd_lot():
        return 1000
    
    @staticmethod
    def get_board_lot_size():
        return 1000
