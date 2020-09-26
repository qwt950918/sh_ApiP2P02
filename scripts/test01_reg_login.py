import unittest
from time import sleep

import requests
import random

from api import log
from api.api_reg_login import ApiRegLogin
from tools import common_assert

phone = "13600001111"
phone2 = "13600001112"
phone3 = "13600001113"
phone4 = "13600001114"
phone5 = "13600001115"
phone6 = "13600001116"
phone7 = "13600001117"
imgVerifyCode = "8888"
password = "q123456"
phone_code = "666666"
dy_server = "on"
invite_phone = "13800001111"


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
    def test01_img_code(self):
        # 调用图片验证码接口
        r = self.api.api_img_code(random.random())
        # 断言 响应200
        print("响应状态吗：", r.status_code)
        try:
            self.assertEqual(200, r.status_code)
        except Exception as e:
            log.error(e)
            raise

    # 2. 注册 短信验证码
    def test02_sms_code(self):
        # 1. 获取图片验证码 目的：使用session对象自动记录cookie
        self.api.api_img_code(random.random())
        # 2. 获取短信验证码
        r = self.api.api_sms_code(phone, imgVerifyCode)
        print("获取短信验证码 结果为：", r.json())
        try:
            # 调用断言方法
            common_assert(self, r, description="发送成功")
        except Exception as e:
            log.error(e)
            raise

    # 3. 注册 测试方法
    def test03_register(self):
        # 1. 获取图片验证码
        self.api.api_img_code(random.random())
        # 2. 获取短信验证码
        self.api.api_sms_code(phone4, imgVerifyCode)
        # 3. 调用注册接口
        r = self.api.api_register(phone4,
                                  password,
                                  imgVerifyCode,
                                  phone_code,
                                  dy_server)
        print(r.json())
        try:
            # 4. 断言注册信息
            common_assert(self, r, description="注册成功")
        except Exception as e:
            log.error(e)
            raise

    # 4. 登录 测试方法
    def test04_login(self):
        r = self.api.api_login(phone4, password)
        print("登陆结果：", r.json())
        try:
            common_assert(self, r, description="登录成功")
        except Exception as e:
            log.error(e)
            raise

    # 5. 是否登录 测试方法
    def test05_is_login(self):
        # 1. 调用登录
        self.api.api_login(phone4, password)
        # 2. 判断是否登录
        r = self.api.api_is_login()
        print("登陆查询结果：", r.json())
        try:
            common_assert(self, r, description="OK")
        except Exception as e:
            log.error(e)
            raise

    """注册图片验证码"""

    # 1. 随机整数获取验证码成功
    def test06_img_code_random_int(self):
        num = random.randint(10000000, 999999999)
        r = self.api.api_img_code(num)
        print("响应状态吗为：", r.status_code)
        log.info("随机整数获取验证码的响应状态码为：".format(r.status_code))
        try:
            common_assert(self, r, status=None)
        except Exception as e:
            log.error(e)

    # 2. 随机数为空
    def test07_img_code_random_null(self):
        num = ""
        r = self.api.api_img_code(num)
        log.info("随机数为空获取验证码的响应状态码为：{}".format(r.status_code))
        try:
            common_assert(self, r, response_code=404, status=None)
        except Exception as e:
            log.error(e)

    # 3. 随机数为字符串
    def test08_img_code_random_str(self):
        num = random.sample("qwerttyuiopasdfghjklzxcvbnm", 8)
        r = self.api.api_img_code("".join(num))
        log.info("随机数为空获取验证码的响应状态码为：{}".format(r.status_code))
        try:
            common_assert(self, r, response_code=400, status=None)
        except Exception as e:
            log.error(e)

    """注册 获取短信验证码"""

    # 1. 手机号为空
    def test09_phone_is_null(self):
        phone = ""
        # 1. 获取图片验证码 目的：使用session对象自动记录cookie
        self.api.api_img_code(random.random())
        # 2. 获取短信验证码
        r = self.api.api_sms_code(phone, imgVerifyCode)
        log.info("手机号为空 响应数据为：{}".format(r.json()))
        print("获取短信验证码 结果为：", r.json())
        try:
            # 调用断言方法
            common_assert(self, r, status=100)
        except Exception as e:
            log.error(e)
            raise

    # 2. 图片验证码为空
    def test10_phone_img_code_is_null(self):
        imgVerifyCode = ""
        # 1. 获取图片验证码 目的：使用session对象自动记录cookie
        self.api.api_img_code(random.random())
        # 2. 获取短信验证码
        r = self.api.api_sms_code(phone, imgVerifyCode)
        log.info("图片验证码为空 响应数据为：{}".format(r.json()))
        print("图片验证码为空 结果为：", r.json())
        try:
            # 调用断言方法
            common_assert(self, r, status=100, description="图片验证码错误")
        except Exception as e:
            log.error(e)
            raise

    # 3. 图片验证码错误
    def test10_phone_img_code_err(self):
        imgVerifyCode = "9977"
        # 1. 获取图片验证码 目的：使用session对象自动记录cookie
        self.api.api_img_code(random.random())
        # 2. 获取短信验证码
        r = self.api.api_sms_code(phone, imgVerifyCode)
        log.info("图片验证码为空 响应数据为：{}".format(r.json()))
        print("图片验证码为空 结果为：", r.json())
        try:
            # 调用断言方法
            common_assert(self, r, status=100, description="图片验证码错误")
        except Exception as e:
            log.error(e)
            raise

    # 4. 不请求图片验证码，获取短信验证码
    def test11_phone_not_img_code_(self):
        # 1. 获取短信验证码
        r = self.api.api_sms_code(phone, imgVerifyCode)
        log.info("不请求图片验证码 响应数据为：{}".format(r.json()))
        print("不请求图片验证码 结果为：", r.json())
        try:
            # 调用断言方法
            common_assert(self, r, status=100, description="图片验证码错误")
        except Exception as e:
            log.error(e)
            raise

    """注册接口 其他用例"""

    # 1. 输入所有参数
    def test12_reg_all_params(self):
        # 1. 获取图片验证码
        self.api.api_img_code(random.random())
        # 2. 获取短信验证码
        self.api.api_sms_code(phone2, imgVerifyCode)
        # 3. 调用注册接口
        r = self.api.api_register(phone2,
                                  password,
                                  imgVerifyCode,
                                  phone_code,
                                  dy_server,
                                  invite_phone)
        print(r.json())
        try:
            # 4. 断言注册信息
            common_assert(self, r, description="注册成功")
        except Exception as e:
            log.error(e)

    # 2. 图片验证码错误
    def test13_reg_img_code_err(self):
        imgVerifyCode = "8899"
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
                                  invite_phone)
        print(r.json())
        log.info("注册 图片验证码错误的结果为：{}".format(r.json()))
        try:
            # 4. 断言注册信息
            common_assert(self, r, status=100, description="验证码错误")
        except Exception as e:
            log.error(e)
            raise

    # 3. 短信验证码错误
    def test14_reg_sms_code_err(self):
        phone_code = "8899"
        # 1. 获取图片验证码
        self.api.api_img_code(random.random())
        # 2. 获取短信验证码
        self.api.api_sms_code(phone5, imgVerifyCode)
        # 3. 调用注册接口
        r = self.api.api_register(phone5,
                                  password,
                                  imgVerifyCode,
                                  phone_code,
                                  dy_server,
                                  invite_phone)
        print(r.json())
        log.info("注册 图片验证码错误的结果为：{}".format(r.json()))
        try:
            # 4. 断言注册信息
            common_assert(self, r, status=100, description="验证码错误")
        except Exception as e:
            log.error(e)
            raise

    # 4. 手机号已存在
    def test15_reg_phone_exist(self):
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
                                  invite_phone)
        print(r.json())
        log.info("注册 图片验证码错误的结果为：{}".format(r.json()))
        try:
            # 4. 断言注册信息
            common_assert(self, r, status=100, description="手机已存在")
        except Exception as e:
            log.error(e)
            raise

    # 5. 密码为空 bug
    def test16_reg_pwd_is_null(self):
        password = ""
        # 1. 获取图片验证码
        self.api.api_img_code(random.random())
        # 2. 获取短信验证码
        self.api.api_sms_code(phone5, imgVerifyCode)
        # 3. 调用注册接口
        r = self.api.api_register(phone5,
                                  password,
                                  imgVerifyCode,
                                  phone_code,
                                  dy_server,
                                  invite_phone)
        print(r.json())
        log.info("注册 图片验证码错误的结果为：{}".format(r.json()))
        try:
            # 4. 断言注册信息
            common_assert(self, r, status=100, description="密码不能为空")
        except Exception as e:
            log.error(e)
            raise

    # 6. 未同意协议 bug
    def test17_reg_not_dy_server(self):
        dy_server = "off"
        # 1. 获取图片验证码
        self.api.api_img_code(random.random())
        # 2. 获取短信验证码
        self.api.api_sms_code(phone6, imgVerifyCode)
        # 3. 调用注册接口
        r = self.api.api_register(phone6,
                                  password,
                                  imgVerifyCode,
                                  phone_code,
                                  dy_server,
                                  invite_phone)
        print(r.json())
        log.info("注册 图片验证码错误的结果为：{}".format(r.json()))
        try:
            # 4. 断言注册信息
            common_assert(self, r, status=100, description="请同意我们协议")
        except Exception as e:
            log.error(e)
            raise

    """登录接口 其他用例"""

    # 1. 用户不存在
    def test18_login_username_not_exists(self):
        r = self.api.api_login(phone7, password)
        print("登陆结果：", r.json())
        log.info("登录·用户不存在结果：{}".format(r.json()))
        try:
            common_assert(self, r, status=100, description="用户不存在")
        except Exception as e:
            log.error(e)
            raise

    # 2. 密码为空
    def test19_login_pwd_is_null(self):
        password = ""
        r = self.api.api_login(phone7, password)
        print("登陆结果：", r.json())
        log.info("登录·用户不存在结果：{}".format(r.json()))
        try:
            common_assert(self, r, status=100, description="密码不能为空")
        except Exception as e:
            log.error(e)
            raise

    # 3. 密码错误1次-3次
    # def test20_login_pwd_err_verify(self):
    #     password = "123eroor"
    #     r = self.api.api_login(phone4, password)
    #     r = self.api.api_login(phone4, password)
    #     r = self.api.api_login(phone4, password)
    #     common_assert(self, r, status=100, description="锁定")
    #     print("登陆结果：", r.json())
    #     log.info("登录·用户不存在结果：{}".format(r.json()))
    #     print("暂停60秒...")
    #     sleep(60)
    #     r = self.api.api_login(phone4, password="q123456")
    #     print("暂停60秒解锁后，登录结果：{}".format(r.json()))
    #     try:
    #         common_assert(self, r, status=200, description="登录成功")
    #     except Exception as e:
    #         log.error(e)
    #         raise

    # 4、登录查询状态 失败
    def test21_login_status_fail(self):
        # 1. 判断是否登录
        r = self.api.api_is_login()
        print("登陆查询结果：", r.json())
        try:
            common_assert(self, r, status=250, description="未登陆")
        except Exception as e:
            log.error(e)
            raise
