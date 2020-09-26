import unittest
from time import sleep
from parameterized import parameterized
import requests
import random

from api import log
from api.api_reg_login import ApiRegLogin
from tools import common_assert, read_json


class TestRegLogin(unittest.TestCase):
    # 初始化
    def setUp(self) -> None:
        # 获取session对象 a01
        self.session = requests.session()
        log.info("正在获取session对象：{}".format(self.session))
        # 获取ApiRegLogin对象
        self.api = ApiRegLogin(self.session)
        log.info("正在获取ApiRegLogin对象: {}".format(self.api))

    # 结束
    def tearDown(self) -> None:
        log.info("正在关闭session对象")
        # 关闭session对象
        self.session.close()

    # 1. 注册图片验证码 测试方法
    @parameterized.expand(read_json("register_login.json","img_code_case"))
    def test01_img_code(self, random, expect_code):
        # 调用图片验证码接口
        r = self.api.api_img_code(random)
        # 断言 响应200
        print("响应状态吗：", r.status_code)
        try:
            self.assertEqual(expect_code, r.status_code)
        except Exception as e:
            log.error(e)
            raise

    # 2. 注册 短信验证码
    @parameterized.expand(read_json("register_login.json","sms_code_case"))
    def test02_sms_code(self,phone, imgverifycode,type,expect_code,expect_status,description):
        if phone != "13600001112":
            # 1. 获取图片验证码 目的：使用session对象自动记录cookie
            self.api.api_img_code(random.random())
        # 2. 获取短信验证码
        r = self.api.api_sms_code(phone, imgverifycode, type=type)
        print("获取短信验证码 结果为：", r.json())
        try:
            # 调用断言方法
            common_assert(self, r, response_code=expect_code,status=expect_status,description=description)
        except Exception as e:
            log.error(e)
            raise

    # 3. 注册 测试方法
    @parameterized.expand(read_json("register_login.json", "reg_case"))
    def test03_register(self, phone4, password, imgVerifyCode, phone_code, dy_server, invite_phone, expect_code, status,
                        description):
        # 1. 获取图片验证码
        self.api.api_img_code(random.random())
        # 2. 获取短信验证码
        self.api.api_sms_code(phone4, imgVerifyCode)
        # 3. 调用注册接口
        r = self.api.api_register(phone4,
                                  password,
                                  imgVerifyCode,
                                  phone_code,
                                  dy_server,
                                  invite_phone=invite_phone)
        print(r.json())
        log.info("请求数据：{} 响应结果：{}".format((phone4, password, imgVerifyCode, phone_code, dy_server, invite_phone, expect_code, status,
                        description),r.json()))
        try:
            # 4. 断言注册信息
            common_assert(self, r, response_code=expect_code,status=status,description=description)
        except Exception as e:
            log.error(e)
            raise

    # 4. 登录 测试方法
    @parameterized.expand(read_json("register_login.json", "login_case"))
    def test04_login(self, keywords, password, expect_code):
        r = self.api.api_login(keywords, password)
        log.info("请求数据：{} 响应数据：{}".format((keywords, password, expect_code), r.json()))

        print("登陆结果：", r.json())
        if "error" in password:
            log.info("锁定60验证...")
            r = self.api.api_login(keywords, password)
            log.info("请求数据：{} 响应数据：{}".format((keywords, password, expect_code), r.json()))
            print("登陆结果：", r.json())

            r = self.api.api_login(keywords, password)
            log.info("请求数据：{} 响应数据：{}".format((keywords, password, expect_code), r.json()))
            print("登陆结果：", r.json())

            sleep(60)
            r = self.api.api_login("13600001111", "q123456")
            log.info("请求数据：{} 响应数据：{}".format((keywords, password, expect_code), r.json()))
            print("登陆结果：", r.json())

        try:
            common_assert(self, r, response_code=expect_code)
        except Exception as e:
            log.error(e)
            raise

    # 5. 是否登录 测试方法 is_login_case
    @parameterized.expand(read_json("register_login.json", "is_login_case"))
    def test05_is_login(self, phone4, password, expect_code):
        # 1. 调用登录
        self.api.api_login(phone4, password)
        # 2. 判断是否登录
        r = self.api.api_is_login()
        print("登陆查询结果：", r.json())
        log.info("请求数据：{} 执行结果：{}".format((phone4, password, expect_code), r.json()))
        try:
            common_assert(self, r, status=expect_code)
        except Exception as e:
            log.error(e)
            raise
