from api import log
from config import HOST_URL


class ApiRegLogin:

    # 1. 初始化
    def __init__(self, session):
        log.info("初始化session对象： {}".format(session))
        # a01
        self.session = session
        # 获取图片验证码url
        self.__url_img_code = HOST_URL + "/common/public/verifycode1/{}"
        # 获取手机验证码url
        self.__url_sms_code = HOST_URL + "/member/public/sendSms"
        # 注册url
        self.__url_reg = HOST_URL + "/member/public/reg"
        # 登录url
        self.__url_login = HOST_URL + "/member/public/login"
        # 是否登录url
        self.__url_is_login = HOST_URL + "/member/public/islogin"

    # 2. 注册-获取图片验证码
    def api_img_code(self, random):
        """
        :param random: 随机数
        :return: 响应对象
        """
        log.info("正在调用注册获取图片验证码接口 请求url: {}".format(self.__url_img_code.format(random)))
        return self.session.get(self.__url_img_code.format(random))

    # 3. 注册-手机验证码
    def api_sms_code(self, phone, imgVerifyCode, type="reg"):
        # 1. 定义请求数据
        data = {
            'phone': phone,
            'imgVerifyCode': imgVerifyCode,
            'type': type
        }
        log.info("正在调用注册获取「手机」验证码接口 请求url: {} 请求数据：{}".format(self.__url_sms_code, data))
        # 2. 调用post方法
        return self.session.post(self.__url_sms_code, data=data)

    # 4. 注册
    def api_register(self, phone, password, verifycode, phone_code, dy_server="on", invite_phone=None):
        # 1. 定义请求数据
        data = {
            "phone": phone,
            "password": password,
            "verifycode": verifycode,
            "phone_code": phone_code,
            "dy_server": dy_server,
            "invite_phone": invite_phone
        }
        log.info("正在调用注册接口 请求url: {} 请求数据：{}".format(self.__url_reg, data))
        # 2. 调用post方法
        return self.session.post(self.__url_reg, data=data)

    # 5. 登录接口
    def api_login(self, keywords, password):
        # 1. 定义请求数据
        data = {
            "keywords": keywords,
            "password": password
        }
        log.info("正在调用登录接口 请求url: {} 请求数据：{}".format(self.__url_login, data))
        # 2. 调用post方法
        return self.session.post(self.__url_login, data=data)

    # 6. 是否登录
    def api_is_login(self):
        log.info("正在调用查询是否登录接口 请求url: {}".format(self.__url_is_login))
        return self.session.post(self.__url_is_login)

    # 注册业务方法
    def api_register_all(self):
        # 1. 获取图片验证码
        self.api_img_code(random=112312312)
        # 2. 获取手机验证码
        self.api_sms_code(phone="13600001111", imgVerifyCode=8888)
        # 3. 注册
        return self.api_register(phone="13600001111",
                                 password="q123456",
                                 verifycode=8888,
                                 phone_code=666666)

    # 登录业务方法
    def api_login_all(self):
        return self.api_login("13600001111", "q123456")
