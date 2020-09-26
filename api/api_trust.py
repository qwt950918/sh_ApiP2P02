from config import HOST_URL
from tools import parser_html


class ApiTrust:
    # 1. 初始化
    def __init__(self, session):
        self.session = session
        # 1. 开户url
        self.__url_trust = HOST_URL + "/trust/trust/register"
        # 2. 充值验证码url
        self.__url_verify_code = HOST_URL + "/common/public/verifycode/{}"
        # 3. 充值验证码url
        self.__url_recharge = HOST_URL + "/trust/trust/recharge"

    # 2. 开户 接口封装
    def api_trust(self):
        return self.session.post(self.__url_trust)

    # 3. 充值验证码 接口封装
    def api_recharge_verify_code(self, random):
        return self.session.post(self.__url_verify_code.format(random))

    # 4. 充值 接口封装
    def api_recharge(self, amount, valicode):
        data = {"paymentType": "chinapnrTrust",
                "formStr": "reForm",
                "amount": amount,
                "valicode": valicode}
        return self.session.post(self.__url_recharge, data=data)

    # 开户业务方法
    def api_trust_all(self):
        # 1. 调用开户 url
        r = self.api_trust()
        # 2. 调用三方开户
        result = parser_html(r)
        return self.session.post(url=result[0],data=result[1])

    # 充值业务方法
    def api_recharge_all(self):
        # 1. 获取充值验证码
        self.api_recharge_verify_code(12312312)
        # 2. 调用充值
        r = self.api_recharge(1000, 8888)
        # 3. 三方充值
        result = parser_html(r)
        return self.session.post(url=result[0], data=result[1])