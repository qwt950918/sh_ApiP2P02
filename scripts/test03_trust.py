import unittest

import requests
import random
from api import log
from api.api_reg_login import ApiRegLogin
from api.api_trust import ApiTrust
from tools import common_assert, parser_html


class TestTrust(unittest.TestCase):
    # 初始化
    def setUp(self) -> None:
        # 1. 获取session
        self.session = requests.session()
        # 2. 获取ApiRegLogin对象
        self.login = ApiRegLogin(self.session)
        # 3. 获取ApiTrust对象
        self.api = ApiTrust(self.session)
        # 4. 登录
        self.login.api_login("13600001111", "q123456")

    # 结束
    def tearDown(self) -> None:
        # 关闭 session
        self.session.close()

    # 1. 开户测试 方法
    def test01_trust(self):
        # 1. 请求 开户
        r = self.api.api_trust()
        log.info("开户结果为：{}".format(r.json()))
        print("结果为：", r.json())
        try:
            common_assert(self, r, status=200)
        except Exception as e:
            log.error(e)
        # 2. 调用三方开户
        result = parser_html(r)
        log.info("解析开户数据结果为：{}".format(result))
        r = self.session.post(url=result[0],data=result[1])
        print("三方开户结果为：", r.text)
        log.info("三方开户的结果为：{}".format(r.text))
        self.assertIn("OK", r.text)

    # 2. 充值验证码 方法
    def test02_verify_code(self):
        r = self.api.api_recharge_verify_code(random.random())
        common_assert(self,r)

    # 3. 充值
    def test03_recharge(self):
        amount, valicode = 1000 ,8888
        # 1. 获取图片验证码
        self.api.api_recharge_verify_code(random.random())

        # 2. 调用充值接口
        self.api.api_recharge(amount,valicode)

        # 3. 调用三方充值接口
        result = parser_html(r)
        r = self.session.post(url=result[0],data=result[1])

        print("三方开户结果为：", r.text)
        log.info("三方开户的结果为：{}".format(r.text))
        self.assertIn("OK", r.text)