from config import HOST_URL
from tools import parser_html


class ApiLoan:
    # 初始化
    def __init__(self, session):
        self.session = session
        # 投资详情url
        self.__url_loan_info = HOST_URL + "/common/loan/loaninfo"
        # 投资 url
        self.__url_loan = HOST_URL + "/trust/trust/tender"
        # 我的投资列表
        self.__url_loan_list = HOST_URL + "/loan/tender/mytenderlist"

    # 1. 投资详情
    def api_loan_info(self, id):
        data = {
            "id": id
        }
        return self.session.post(self.__url_loan_info, data=data)

    # 2. 投资
    def api_loan(self, id, amount):
        data = {
            "id": id,
            "depositCertificate":"-1",
            "amount":amount
        }
        return self.session.post(self.__url_loan, data=data)

    # 3. 我的投资列表
    def api_my_loan_list(self):
        data = {
            "status": "tender"
        }
        return self.session.post(self.__url_loan_list, data=data)

    # 投资业务
    def api_loan_all(self):
        # 1. 投资
        r =  self.api_loan(642,1000)
        # 2. 三方投资
        result = parser_html(r)
        return self.session.post(url=result[0], data=result[1])