import re
import json
import logging
from enum import Enum
from datetime import date
from typing import Optional, Dict, List, Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .auth import EastMoneyAuth

# URL Constants
URL_TRADE_SUBMIT = "/Trade/SubmitTradeV2"
URL_TRADE_SUBMIT_BATCH = "/Trade/SubmitBatTradeV2"
URL_STOCK_CURRENT_INFO = "https://push2.eastmoney.com/api/qt/stock/get"
URL_STOCK_KLINE = "http://push2his.eastmoney.com/api/qt/stock/kline/get"
URL_GET_STOCK_LIST = "/Search/GetStockList"
URL_TRADE_GET_ALL_NEED_TRADE_INFO = "/Trade/GetAllNeedTradeInfo"
URL_SEARCH_GET_HIS_DEAL_DATA = "/Search/GetHisDealData"
URL_CONVERTIBLE_BOND_LIST = "/Trade/GetConvertibleBondListV2"
URL_QUERY_ASSET_POSITION = "/Com/queryAssetAndPositionV1"
URL_QUERY_HIS_MATCH_MERGE = "/Search/queryHisMatchMergeWEB"
URL_QUERY_HIS_ORDER_MERGE = "/Search/queryHisOrderMergeWEB"
URL_QUERY_TODAY_MATCH = "/Search/queryTodayMatchWEB"
URL_QUERY_TODAY_ORDER_MERGE = "/Search/queryTodayOrderMergeWEB"
URL_FUNDS_FLOW = "/Search/GetFundsFlow"

# Logger configuration
logger = logging.getLogger(__name__)


class TradeType(Enum):
    LIMIT_BUY = "B"
    LIMIT_SELL = "S"
    MARKET_CANCEL_BUY = "0d"  # 最优五档剩余撤销买入
    MARKET_CANCEL_SELL = "0i"  # 最优五档剩余撤销卖出


class EastMoney:
    def __init__(
        self,
        userId: Optional[str] = None,
        password: Optional[str] = None,
        randomNumber: Optional[float] = None,
        duration: int = 15,
        authentication: Optional[Dict] = None,
        host: str = "https://jywg.18.cn",
        retries: int = 3,
    ) -> None:
        """
        Initialize EastMoney API client.

        Args:
            userId: User ID for login.
            password: Password for login (encrypted or plain, depends on auth implementation).
            randomNumber: Random number for login flow (legacy).
            duration: Session duration in minutes.
            authentication: Pre-existing authentication dict (cookies, validate_key).
            host: API host URL.
            retries: Number of retries for network requests.
        """
        self.host = host
        self.session = requests.Session()

        # Configure retries
        retry_strategy = Retry(
            total=retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "POST", "OPTIONS"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

        if not authentication:
            if not userId or not password:
                raise ValueError(
                    "Authentication credentials (userId, password) or authentication object required."
                )
            logger.info("Logging in with userId: %s", userId)
            authentication = EastMoneyAuth(userId, password, duration).login()

        self.session.cookies.update(authentication["cookies"])
        self.validate_key = authentication["validate_key"]
        logger.debug("EastMoney client initialized successfully.")

    def url_add_host(self, url: str) -> str:
        return (self.host + url) if "https" not in url else url

    def url_add_validate_key(self, url: str) -> str:
        url = self.url_add_host(url)
        url = (url + "?") if "?" not in url else url
        return url + f"validatekey={self.validate_key}"

    def _request(
        self,
        method: str,
        url: str,
        data: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
    ) -> Any:
        """Internal request handler with unified error handling."""
        try:
            if method.upper() == "POST":
                # For some APIs that expect JSON string in data vs actual JSON body
                if json_data:
                    # Specific headers for JSON payload if needed, usually requests handles it with 'json='
                    # But legacy code used data=json.dumps(data) with explicit header
                    headers = {"Content-Type": "application/json"}
                    rsp = self.session.post(
                        url, data=json.dumps(json_data), headers=headers
                    )
                else:
                    rsp = self.session.post(url, data=data)
            else:
                rsp = self.session.get(url, params=data)

            rsp.raise_for_status()

            # Try to parse JSON
            try:
                json_resp = rsp.json()
            except json.JSONDecodeError:
                logger.error("Failed to parse JSON response from %s", url)
                logger.debug("Response text: %s", rsp.text)
                raise Exception(f"Invalid JSON response from {url}")

            # Check for API-level errors if 'Status' field exists
            if isinstance(json_resp, dict) and "Status" in json_resp:
                if json_resp["Status"] != 0:
                    msg = json_resp.get("Message", "Unknown API error")
                    logger.warning(
                        "API returned error status: %s, Message: %s",
                        json_resp["Status"],
                        msg,
                    )
                    # We return the response even on error status because sometimes the caller needs to handle it (e.g. order failure)

            return json_resp

        except requests.exceptions.RequestException as e:
            logger.error("Network request failed: %s", str(e))
            raise Exception(f"Network request failed: {e}")

    def query(self, url: str, data: Optional[Dict] = None) -> Any:
        """Execute a query and return the 'Data' field."""
        rsp_json = self._request("POST", url, data=data)

        # Legacy behavior: expect "Data" field.
        # If "Data" is missing or None, it might be an error or empty result.
        if "Data" not in rsp_json:
            logger.error("Response missing 'Data' field: %s", rsp_json)
            raise Exception("Invalid API response: missing 'Data' field")

        return rsp_json["Data"]

    def _post_order(self, url: str, data: Dict) -> Any:
        """Helper to post order data formatted as JSON string."""
        # The legacy post_order function sent data as a JSON string within the body?
        # Actually checking common.py/old code: data=json.dumps(data), headers={'Content-Type': 'application/json'}
        # So it's a standard JSON POST.
        rsp_json = self._request("POST", url, json_data=data)
        return rsp_json.get("Message", rsp_json)

    @staticmethod
    def is_oneday_trade_day(date_str: str, stock_code: str = "000001") -> bool:
        recent_trade_day = EastMoney.recent_trade_day(date_str, stock_code)
        return recent_trade_day == date_str

    @staticmethod
    def recent_trade_day(date_str: str, stock_code: str = "000001") -> str:
        klines_dict = EastMoney.query_stock_klines(
            stock_code, limit=1, end_date=date_str, is_data_frame=False
        )
        if not klines_dict or "klines" not in klines_dict:
            return ""
        # klines format: "date,open,close,..."
        recent_trade_day = [i.split(",") for i in klines_dict["klines"]][-1][0]
        return recent_trade_day

    @staticmethod
    def query_stock_klines(
        stock_code: str,
        limit: int = 1,
        end_date: str = "2050-01-01",
        is_data_frame: bool = False,
    ) -> Any:
        url = URL_STOCK_KLINE
        market = (
            "1"
            if (
                stock_code.startswith("6")
                or stock_code.startswith("5")
                or stock_code.startswith("11")
            )
            else "0"
        )

        payload = {
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
            "klt": "101",
            "fqt": "0",
            "lmt": limit,
            "secid": f"{market}.{stock_code}",
            "end": end_date.replace("-", ""),
        }

        # Use simple requests here since it's a public API (no session/auth needed usually)
        # But we could use self.session if instance method. Since it's static, new request.
        try:
            resp = requests.get(url, params=payload)
            resp.raise_for_status()
            data = resp.json().get("data")
        except Exception as e:
            logger.error("Failed to query klines: %s", e)
            return None if not is_data_frame else __import__("pandas").DataFrame()

        if not is_data_frame:
            return data.copy() if data else {}
        else:
            import pandas as pd

            if data is None:
                return pd.DataFrame()
            df = pd.DataFrame([i.split(",") for i in data["klines"]])
            if len(df) == 0:
                return df

            df.columns = [
                "日期",
                "开盘",
                "收盘",
                "最高",
                "最低",
                "成交量",
                "成交额",
                "振幅",
                "涨跌幅",
                "涨跌额",
                "换手率",
            ]
            df["股票代码"] = data["code"]
            df["股票名称"] = data["name"]
            df["市场代码"] = data["market"]
            return df

    @staticmethod
    def query_stock_current_info(stock_code: str) -> Dict:
        url = URL_STOCK_CURRENT_INFO
        market = (
            "1" if (stock_code.startswith("6") or stock_code.startswith("5")) else "0"
        )
        payload = {
            "fields": "f43,f44,f45,f46,f47,f48,f49,f161,f51,f52,f57,f58,f59",
            "secid": f"{market}.{stock_code}",
        }
        key_dict = {
            "f43": "最新价",
            "f44": "最高",
            "f45": "最低",
            "f46": "今开",
            "f47": "总手",
            "f48": "金额",
            "f49": "外盘",
            "f161": "内盘",
            "f51": "涨停",
            "f52": "跌停",
            "f57": "股票代码",
            "f58": "股票名称",
            "f59": "价格精度",
        }
        try:
            resp = requests.get(url, params=payload)
            resp.raise_for_status()
            json_resp = resp.json()
            if "data" not in json_resp or not json_resp["data"]:
                logger.warning("No data found for stock code: %s", stock_code)
                return {}
            data = json_resp["data"]
            return {key_dict.get(key, key): val for key, val in data.items()}
        except Exception as e:
            logger.error("Error querying stock info: %s", e)
            raise

    def query_stock_trade_info(self, stock_code: str) -> Dict:
        url = self.url_add_validate_key(URL_TRADE_GET_ALL_NEED_TRADE_INFO)
        return self.query(url, data={"stockCode": stock_code})["ZqInfo"]

    def query_trade_history(
        self, start_date: str, end_date: str, count: int = 10000
    ) -> List[Dict]:
        url = self.url_add_validate_key(URL_SEARCH_GET_HIS_DEAL_DATA)
        return self.query(
            url, data={"st": start_date, "et": end_date, "qqhs": count, "dws": ""}
        )

    def query_market_convertible_bonds_list(self) -> List[Dict]:
        url = self.url_add_validate_key(URL_CONVERTIBLE_BOND_LIST)
        return self.query(url)

    def query_asset_stocks_list(self) -> List[Dict]:
        url = self.url_add_validate_key(URL_GET_STOCK_LIST)
        return self.query(url)

    def query_history_match_merge_web(
        self, start_date: str, end_date: str, count: int = 10000
    ) -> List[Dict]:
        url = self.url_add_validate_key(URL_QUERY_HIS_MATCH_MERGE)
        return self.query(
            url,
            data={
                "strdate": start_date,
                "enddate": end_date,
                "count": count,
                "poststr": "",
            },
        )

    def query_history_order_merge_web(
        self, start_date: str, end_date: str, count: int = 10000
    ) -> List[Dict]:
        url = self.url_add_validate_key(URL_QUERY_HIS_ORDER_MERGE)
        return self.query(
            url,
            data={
                "strdate": start_date,
                "enddate": end_date,
                "count": count,
                "poststr": "",
            },
        )

    def query_today_match_web(self, count: int = 10000) -> List[Dict]:
        url = self.url_add_validate_key(URL_QUERY_TODAY_MATCH)
        return self.query(url, data={"qqhs": count, "dws": ""})

    def query_today_order_merge_web(self, count: int = 10000) -> List[Dict]:
        url = self.url_add_validate_key(URL_QUERY_TODAY_ORDER_MERGE)
        return self.query(url, data={"qqhs": count, "dws": ""})

    def query_funds_flow(
        self, start_date: str, end_date: str, count: int = 10000
    ) -> List[Dict]:
        url = self.url_add_validate_key(URL_FUNDS_FLOW)
        return self.query(
            url, data={"st": start_date, "et": end_date, "qqhs": count, "dwc": ""}
        )

    def query_asset_and_position(self, money_type: str = "RMB") -> List[Dict]:
        url = self.url_add_validate_key(URL_QUERY_ASSET_POSITION)
        return self.query(url, data={"moneyType": money_type})

    def query_is_new_convertible_bond_available_today(self) -> bool:
        today_str = date.today().strftime("%Y-%m-%d %H:%M:%S")
        url = "https://datacenter-web.eastmoney.com/api/data/v1/get?sortColumns=PUBLIC_START_DATE&sortTypes=-1&pageSize=10&pageNumber=1&reportName=RPT_BOND_CB_LIST&columns=PUBLIC_START_DATE"

        try:
            resp = self.session.get(url)
            resp.raise_for_status()
            result = re.search(today_str, resp.text)
            return result is not None
        except Exception as e:
            logger.error("Failed to check new convertible bonds: %s", e)
            return False

    def place_order(
        self, stock_code: str, amount: int, trade_type: TradeType, price: float = None
    ) -> Any:
        """Standardized order placement.

        Args:
            stock_code: Stock Code
            amount: Quantity (must be positive integer)
            trade_type: TradeType Enum (LIMIT_BUY, LIMIT_SELL, etc.)
            price: Price (float). If None, calculated based on trade_type defaults.

        Returns:
            API response message or object.
        """
        # Input Validation
        if amount <= 0:
            raise ValueError("Amount must be a positive integer.")
        if not stock_code or not isinstance(stock_code, str):
            raise ValueError("Invalid stock_code.")

        url = self.url_add_validate_key(URL_TRADE_SUBMIT)

        # Ensure we have stock info for precision formatting
        _infos = self.query_stock_current_info(stock_code)
        if not _infos:
            raise ValueError(f"Could not fetch info for stock code: {stock_code}")

        precision = _infos.get("价格精度", 2)
        price_fmt = "{:." + str(precision) + "f}"

        if price is None:
            if trade_type == TradeType.MARKET_CANCEL_BUY:
                price_limit_up = _infos["涨停"] / 10**precision
                price = price_limit_up
            elif trade_type == TradeType.MARKET_CANCEL_SELL:
                price_limit_down = _infos["跌停"] / 10**precision
                price = price_limit_down
            else:
                raise ValueError("Price must be specified for LIMIT orders.")

        # Automatically format price string
        formatted_price = price_fmt.format(price)

        trade_type_val = (
            trade_type.value if isinstance(trade_type, TradeType) else trade_type
        )

        data = {
            "stockCode": stock_code,
            "price": formatted_price,
            "amount": int(amount),
            "tradeType": trade_type_val,
        }
        return self._post_order(url, data)

    # Legacy alias for backward compatibility (optional)
    def order_(self, stock_code, amount, trade_type, price=None):
        try:
            tt = TradeType(trade_type)
        except ValueError:
            tt = trade_type

        return self.place_order(stock_code, amount, tt, price)
