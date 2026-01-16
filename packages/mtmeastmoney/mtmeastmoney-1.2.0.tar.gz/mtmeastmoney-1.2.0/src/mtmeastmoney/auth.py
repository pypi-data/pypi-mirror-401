import re
import time
import random
import datetime

import requests
import ddddocr

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

def ocr_code(vertify_code_url):
    for _ in range(5):
        ocr = ddddocr.DdddOcr(show_ad=False)
        rsp = requests.get(vertify_code_url)
        res = ocr.classification(rsp.content)
        verify_code = res.replace("z", "2").replace("o", "0")
        if len(verify_code) == 4:
            return verify_code
        else:
            time.sleep(1)
    raise Exception("无法识别出正确的验证码")


class EastMoneyAuth:
    def __init__(self, userId, password, duration=1440):
        self.host = "https://jywg.18.cn"
        self.session = requests.Session()
        self.userId = userId
        self.password = password
        self.login_duration = duration
        self.random_number = random.random()
        self.vertify_code_url = self.host + f"/Login/YZM?randNum={self.random_number}"
        self.validate_key = ""

    def _get_validate_key(self):
        url = self.host + "/Trade/XzsgBatPurchase"
        rsp = self.session.get(url)
        validatekey_list = re.findall("<input id=\"em_validatekey\"[^>]*value=\"([^\"]*)\"", rsp.text)
        if not len(validatekey_list):
            raise Exception("获取验证秘钥：登录失败")
        return validatekey_list[0]

    def _login(self):
        data = {
            "userId": str(self.userId),
            "password": str(self.password),
            "randNumber": str(self.random_number),
            "identifyCode": ocr_code(self.vertify_code_url),
            "duration": str(self.login_duration),
            "authCode": "",
            "type": "Z"
        }
        print(data)
        url = self.host + "/Login/Authentication?validatekey="
        rsp = self.session.post(url, data)
        return rsp.json()
    
    def login(self, max_times=3, wait_second=5):
        """
        Performs login with retries.
        Returns a dictionary containing cookies and validate_key.
        """
        for _ in range(max_times):
            try:
                if (rsp_json:=self._login())["Status"] == 0:
                    break
            except Exception:
                pass
            time.sleep(wait_second)
        else:
            raise Exception("登录失败")
        
        self.validate_key = self._get_validate_key()
        rsp_data = rsp_json["Data"][0]
        request_ts = datetime.datetime.strptime(rsp_data["Date"] + rsp_data["Time"], "%Y%m%d%H%M%S").timestamp()
        
        return {
            "real_name": rsp_data["khmc"],
            "user_id": self.userId,
            "validate_key": self.validate_key,
            "expire_from": request_ts,
            "expire_to": int(request_ts + self.login_duration * 60),
            "cookies": self.session.cookies.get_dict(),
        }