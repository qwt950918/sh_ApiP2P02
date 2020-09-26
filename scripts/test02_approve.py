import unittest

import requests

from api import log
from api.api_approve import ApiApprove
from api.api_reg_login import ApiRegLogin
from tools import common_assert


class TestApprove(unittest.TestCase):
    def setUp(self) -> None:
        # 获取session对象
        self.session = requests.session()
        # 获取ApiRegLogin对象
        self.login = ApiRegLogin(self.session)
        # 获取ApiApprove对象
        self.api = ApiApprove(self.session)

    def tearDown(self) -> None:
        # 关闭session
        self.session.close()

    # 1. 认证测试方法
    def test01_approve(self):
        realname = "张三"
        card_id = "110101199007071599"
        # 1. 登录
        self.login.api_login("13600001111", "q123456")
        # 2. 调用认证接口
        r = self.api.api_approve(realname, card_id)
        log.info("认证结果：{}".format(r.json()))
        try:
            # 3. 断言认证结果
            common_assert(self, r, status=200)
        except Exception as e:
            log.error(e)
            raise

    # 2. 认证信息测试方法 成功
    def test02_approve_info(self):
        # 1. 登录
        self.login.api_login("13600001111", "q123456")
        # 2. 调用认证信息接口
        r = self.api.api_approve_info()
        # 3. 断言
        log.info("认证信息查询结果：{}".format(r.json()))
        try:
            # 3. 断言认证结果
            common_assert(self, r)
        except Exception as e:
            log.error(e)
            raise
