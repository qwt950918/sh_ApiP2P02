import logging.handlers
import os
import json

import pymysql

from config import BASE_DIR
from bs4 import BeautifulSoup


# status description status_code断言
def common_assert(self, response, response_code=200, status=None, description=None):
    self.assertEqual(response_code, response.status_code)
    if status:  # staus不为None执行
        self.assertEqual(status, response.json().get("status"))
    if description:  # 不为None条件成立
        self.assertIn(description, response.json().get("description"))


# 读取json工具
def read_json(filename, case_name):
    file_path = BASE_DIR + os.sep + "data" + os.sep + filename
    arrs = []
    with open(file_path, "r", encoding="utf-8") as f:
        for data in json.load(f).get(case_name):
            arrs.append(tuple(data.values())[1:])
        return arrs


# 提取三方请求工具
def parser_html(response):
    # 提取html
    html = response.json().get("description").get("form")
    print("html提取内容为：", html)
    # 使用sp4进行解析
    bs = BeautifulSoup(html, "html.parser")
    # 提取url
    url = bs.form.get("action")
    print("提取的url:", url)
    # 提取所有input标签name属性和value 并存储到字典中
    data = {}
    for input in bs.find_all("input"):
        data[input.get("name")] = input.get("value")
    # 返回 url 和 字典数据
    return url, data


# 连接数据库工具
class DBUtil:

    # 1. 获取连接
    @classmethod
    def __get_conn(cls):
        return pymysql.connect(host="52.83.144.39",
                               user="root",
                               password="Itcast_p2p_20191228",
                               port=3306,
                               database="czbk_member",
                               charset="utf8")

    # 2. 执行sql语句
    @classmethod
    def execut_sql(cls, sql):
        # 1. 获取连接对象
        conn = cls.__get_conn()
        # 2. 获取游标对象
        cursor = conn.cursor()
        # 3. 执行sql
        cursor.execute(sql)
        # 如果sql语句第一个单词不是select就提交事务，并返回受影响的行数
        try:
            if sql.lower().split(" ")[0] != "select":
                # 提交事务
                conn.commit()
                # 返回受影响的行数
                return cursor.rownumber
            else:
                # 否则为查询语句，返回所有的结果
                return cursor.fetchall()
        except:
            # 回滚事务
            conn.rollback()
        finally:
            # 关闭连接
            cls.__close(cursor, conn)

    # 3. 关闭方法
    @classmethod
    def __close(cls, cursor=None, conn=None):
        # 1. 先关闭游标
        if cursor:
            cursor.close()

        # 2. 关闭连接
        if conn:
            conn.close()


# 清除数据方法
def clear_test_data():
    # 清除登录日志表
    sql = """delete l.* from mb_member_login_log l INNER JOIN mb_member m on l.member_id = m.id WHERE m.phone in ("13600001111", "13600001112","13600001113","13600001114","13600001115","13600001116");"""
    result = DBUtil.execut_sql(sql)
    print("sql执行结果：{}".format(result))
    GetLogger.get_log().info("sql执行结果：{}".format(result))

    # 清除会员信息表
    sql = """DELETE i.* from mb_member_info i INNER JOIN mb_member m on i.member_id = m.id WHERE m.phone in ("13600001111", "13600001112","13600001113","13600001114","13600001115","13600001116");"""
    result = DBUtil.execut_sql(sql)
    print("sql执行结果：{}".format(result))
    GetLogger.get_log().info("sql执行结果：{}".format(result))

    # 清除会员主表
    sql = """delete from mb_member where phone in ("13600001111", "13600001112","13600001113","13600001114","13600001115","13600001116");"""
    result=DBUtil.execut_sql(sql)
    print("sql执行结果：{}".format(result))
    GetLogger.get_log().info("sql执行结果：{}".format(result))

    # 清除注册日志表
    sql = """DELETE from mb_member_register_log where phone in ("13600001111", "13600001112","13600001113","13600001114","13600001115","13600001116");"""
    result=DBUtil.execut_sql(sql)
    print("sql执行结果：{}".format(result))
    GetLogger.get_log().info("sql执行结果：{}".format(result))


# 日志工具
class GetLogger:
    # 声明日志器
    logger = None

    @classmethod
    def get_log(cls):
        if cls.logger is None:
            # 获取日志器
            cls.logger = logging.getLogger()
            # 设置级别 总开关
            cls.logger.setLevel(logging.INFO)
            filename = BASE_DIR + os.sep + "log" + os.sep + "p2p.log"
            # 获取文件处理器
            fh = logging.handlers.TimedRotatingFileHandler(filename=filename,
                                                           when="midnight",
                                                           interval=1,
                                                           backupCount=3,
                                                           encoding="utf-8"
                                                           )
            # 获取格式器
            fm = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s (%(funcName)s:%(lineno)d] - %(message)s"
            fmt = logging.Formatter(fm)
            # 将格式器添加到处理器
            fh.setFormatter(fmt)
            # 将处理器添加到日志器
            cls.logger.addHandler(fh)
        return cls.logger


if __name__ == '__main__':
    # print(read_json("register_login.json", "is_login_case"))
    # sql = "SELECT * FROM mb_member"
    # print(sql.lower().split(" ")[0])
    # r = DBUtil.execut_sql(sql)
    # print("执行结果为：", r)
    clear_test_data()