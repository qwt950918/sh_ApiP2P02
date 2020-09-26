import unittest

import requests

from api import log
from api.api_loan import ApiLoan
from api.api_reg_login import ApiRegLogin
from api.api_trust import ApiTrust
from tools import clear_test_data


class TestTrustAll(unittest.TestCase):
    def setUp(self) -> None:
        # 0. 清除数据
        clear_test_data()
        # 1. 获取session
        self.session = requests.session()
        # 2. 获取登录注册对象
        self.reg_login = ApiRegLogin(self.session)
        # 3. 获取开户充值对象
        self.trust = ApiTrust(self.session)
        # 4. 获取投资对象
        self.loan = ApiLoan(self.session)

    def tearDown(self) -> None:
        # 1. 关闭session
        self.session.close()
        # 2. 清除 数据
        clear_test_data()

    # 1. 投资业务流程
    def test01_all(self):
        # 1. 注册业务
        r = self.reg_login.api_register_all()
        print("注册业务结果为：{}".format(r.json()))
        log.info("注册业务结果为：{}".format(r.json()))
        self.assertEqual(200, r.json().get("status"))
        self.assertIn("成功", r.json().get("description"))

        # 2. 登录业务
        r = self.reg_login.api_login_all()
        print("登录业务结果为：{}".format(r.json()))
        log.info("登录业务结果为：{}".format(r.json()))
        self.assertEqual(200, r.json().get("status"))
        self.assertIn("成功", r.json().get("description"))
        # 3.  开户业务
        r = self.trust.api_trust_all()
        print("开户业务结果为：{}".format(r.text))
        log.info("开户业务结果为：{}".format(r.text))
        self.assertIn("OK", r.text)

        # 4. 充值业务
        r = self.trust.api_recharge_all()
        print("充值业务结果为：{}".format(r.text))
        log.info("充值业务结果为：{}".format(r.text))
        self.assertIn("OK", r.text)

        # 5.  投资业务
        r = self.loan.api_loan_all()
        print("投资业务结果为：{}".format(r.text))
        log.info("投资业务结果为：{}".format(r.text))
        self.assertIn("OK", r.text)
