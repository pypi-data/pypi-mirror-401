from datetime import datetime
from .eastmoney import EastMoney, URL_TRADE_SUBMIT_BATCH, URL_TRADE_SUBMIT


class EastMoneyStrategies:
    def __init__(self, eastmoney_client: EastMoney):
        self.client = eastmoney_client

    def buy_today_convertible_bonds(self):
        """Buys all convertible bonds available for purchase today."""
        json_data = self.client.query_market_convertible_bonds_list()
        json_data = [
            bond
            for bond in json_data
            if bond["PURCHASEDATE"] == datetime.now().strftime("%Y%m%d")
        ]
        if not len(json_data):
            return "今日无可买可转债"
        data = [
            {
                "StockCode": bond["SUBCODE"],
                "StockName": bond["SUBNAME"],
                "Price": bond["PARVALUE"],
                "Amount": int(bond["LIMITBUYVOL"]),
                "TradeType": "B",
                "Market": bond["Market"],
            }
            for bond in json_data
        ]
        url = self.client.url_add_validate_key(URL_TRADE_SUBMIT_BATCH)
        # Using internal helper from client instance
        message = self.client._post_order(url, data)
        return message

    def sell_old_convertible_bonds(self):
        """Sells all convertible bonds that are currently held."""
        json_data = self.client.query_asset_stocks_list()
        json_data = [i for i in json_data if int(i["Kysl"]) > 0]
        if not len(json_data):
            return ""
        data = [
            {
                "stockCode": i["Zqdm"],
                "price": 80,
                "amount": int(i["Kysl"]),
                "tradeType": "S",
                "zqmc": i["Zqmc"],
                "gddm": i["Gddm"],
                "market": i["Market"],
            }
            for i in json_data
            if "债" in i["Zqmc"] or "转2" in i["Zqmc"]
        ]
        url = self.client.url_add_validate_key(URL_TRADE_SUBMIT)
        message_list = [
            f"卖单提交: {i['zqmc']} {i['amount']} {self.client._post_order(url, i)}"
            for i in data
            if i["amount"] > 0
        ]
        return "\n".join(message_list)

    def auto_trade_bonds(self, is_sell=False):
        """Automatically buys new bonds and optionally sells old ones."""
        try:
            message = self.buy_today_convertible_bonds()
        except Exception as e:
            message = str(e)
        if is_sell:
            message += "\n"
            try:
                message += self.sell_old_convertible_bonds()
            except Exception as e:
                message += str(e)
        if message.endswith("\n"):
            message = message[:-1]
        return message
