import unittest

import requests

from api import log
from api.api_loan import ApiLoan
from api.api_reg_login import ApiRegLogin
from tools import common_assert, parser_html


class TestLoan(unittest.TestCase):
    def setUp(self) -> None:
        # 1. session对象
        self.session = requests.session()
        # 2. 登录对象并登录方法
        ApiRegLogin(self.session).api_login("13600001111", "q123456")
        # 3. 投资接口对象
        self.api = ApiLoan(self.session)

    def tearDown(self) -> None:
        self.session.close()

    # 投资详情接口测试方法
    def test01_loan_info(self):
        id = 642
        r = self.api.api_loan_info(id)
        print("投资详情结果：", r.json())
        log.info("投资详情结果为：{}".format(r.json))
        try:
            common_assert(self, r, status=200)
        except Exception as e:
            log.error(e)
            raise
    # 投资接口测试方法
    def test02_loan(self):
        id = 642
        amount = 1000
        r = self.api.api_loan(id, amount)
        print("投资接口响应结果为：", r.json())
        log.info("投资接口响应结果为：{}".format(r.json()))

        # 提取html数据
        result = parser_html(r)
        # 调用三方接口
        r = self.session.post(url=result[0],data=result[1])
        log.info("第三方投资结果为：{}".format(r.text))
        try:
            self.assertIn("OK",r.text)
        except Exception as e:
            log.error(e)
            raise
    # 我的投资列表接口测试方法
    def test03_my_loan_list(self):
        r = self.api.api_my_loan_list()
        print("我的投资列表结果为：", r.json())
        log.info("我的投资列表结果为：{}".format(r.json()))
        try:
            self.assertEqual("642", r.json().get("items")[0].get("loan_id"))
        except Exception as e:
            log.error(e)
            raise