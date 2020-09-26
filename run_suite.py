# coding=UTF-8
# 导包
from lib import HTMLTestRunner_HeiMa
import unittest
import os
from config import BASE_DIR

# 自定义测试套件
from lib.HTMLTestRunner_HeiMa import HTMLTestRunner

suite = unittest.defaultTestLoader.discover("./scripts", pattern="test*.py")

# 获取报告储存文件流并实例化调用
repord_path = BASE_DIR + os.sep + "report" + os.sep + "report.html"
with open(repord_path, "wb") as f:
    HTMLTestRunner(stream=f).run(suite)
