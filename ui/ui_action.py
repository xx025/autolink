from __future__ import print_function

import base64
import datetime
import json
import re

import requests
from PyQt5 import QtWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QMessageBox

from setting_file.load_setting_file import Setting
from startup.set_start_up import set_startup, remove_startup, check_startup
from ui.win_ui import Ui_MainWindow


class Ui(Ui_MainWindow):

    def __init__(self):

        self.name = '校园网自动连接'

        self.input_count = 0
        self.json_file = {
            "zhangHao": "",
            "miMa": "",
            "baoChiHouTai": True,
            "ziDongRenZheng": True,
            "kaiJiQiDong": True
        }

        self.setting = Setting(json_file=self.json_file)
        self.setting_abs, self.json_file = self.setting.read_setting_file()

    def init_ui(self):
        self.miMaInput.setEchoMode(QtWidgets.QLineEdit.Password)
        # self.zhangHaoInput.setEchoMode(QtWidgets.QLineEdit.Password)

        self.dengLuBtn.clicked.connect(self.check_login)
        # 登录按钮

        self.shengChengPeiZhi.clicked.connect(self.save_setting)

        self.kaiJiQiDong.setChecked(check_startup(self.name))
        # 先设置初始化状态，再绑定事件
        self.kaiJiQiDong.stateChanged.connect(self.she_zhi_zi_qi)
        # 开机自启复选框 绑定事件

        self.fanKui.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl('https://github.com/xx025/autolink/issues/new/choose')))

        self.baoChiHouTai.setVisible(False)

        self.dengLuZhuangTai.setVisible(False)

        self.get_local_setting()
        # 加载本地配置文件

        # 事件触发绑定 设置在加载配置文件之后 否则 设置的同时 会触发更新
        self.ziDongRenZheng.stateChanged.connect(self.update_json_file)
        self.zhangHaoInput.textChanged.connect(self.update_json_file)
        self.miMaInput.textChanged.connect(self.update_json_file)

        if self.ziDongRenZheng.isChecked():
            self.check_login()

    def she_zhi_zi_qi(self):
        """
        开机启动项设置

        :return:
        """

        name = self.name
        desc = '开机自启动连接校园网'

        if self.kaiJiQiDong.isChecked():
            # 删除开机启动
            if not check_startup(name=name):
                if set_startup(name=name, desc=desc):
                    self.textBrowser.append('设置开机启动成功')
        else:
            if remove_startup(name=name):
                self.textBrowser.append('取消开机启动')

    def save_setting(self):
        # 生成配置
        self.setting.generate_file(json_file=self.json_file)
        QMessageBox.information(QtWidgets.QMainWindow(), "导出完成",
                                '请将配置文件和程序放在一块，复制到移动设备中', QMessageBox.Yes)

    def get_local_setting(self):
        self.zhangHaoInput.setText(self.json_file['zhangHao'])
        self.miMaInput.setText(self.json_file['miMa'])
        self.baoChiHouTai.setChecked(self.json_file["baoChiHouTai"])
        self.ziDongRenZheng.setChecked(self.json_file['ziDongRenZheng'])
        self.kaiJiQiDong.setChecked(self.json_file['kaiJiQiDong'])
        self.shengChengPeiZhi.setVisible(self.setting_abs)
        # 如果路径为绝对路径则显示导出按钮

    def update_json_file(self):
        self.json_file['zhangHao'] = self.zhangHaoInput.text()
        self.json_file['miMa'] = self.miMaInput.text()
        self.json_file["baoChiHouTai"] = self.baoChiHouTai.isChecked()
        self.json_file['ziDongRenZheng'] = self.ziDongRenZheng.isChecked()
        self.json_file['kaiJiQiDong'] = self.kaiJiQiDong.isChecked()
        self.setting.save_setting_file(json_file=self.json_file)

    def deng_lu(self):

        self.textBrowser.append(f'{datetime.datetime.now()}:尝试登录')

        user_account = self.zhangHaoInput.text()
        user_password = self.miMaInput.text()

        header = {"Accept-Encoding": "gzip, deflate",
                  "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                  # "Cookie": "PHPSESSID=",
                  "DNT": "1",
                  "Host": "10.10.252.1:801",
                  "Referer": "http://10.10.252.1/",
                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52"}
        data = {'c': "Portal",
                'a': "login",
                # "callback": "dr****",
                "login_method": 1,
                "user_account": user_account,
                "user_password": user_password,
                # "wlan_user_ip": "10.126.**.**",
                "wlan_user_ipv6": "",
                "wlan_user_mac": "000000000000",
                "wlan_ac_ip": "",
                "wlan_ac_name": "",
                "jsVersion": 3.1,
                # "_": 166****\
                }

        res = requests.get('http://10.10.252.1:801/eportal/', params=data, headers=header).text

        p1 = re.compile(r"[(](.*?)[)]", re.S)  # 最小匹配

        ls = re.findall(p1, res)
        if ls.__len__() > 0:
            msg = json.loads(ls[0])
            result = msg.get('result')
            mseg = msg.get('msg')
            if result == '1' and mseg == '认证成功':
                self.dengLuZhuangTai.setText('注销登录')
            else:
                if mseg == "":
                    mseg = "没有消息"
                else:

                    try:
                        mseg = base64.b64decode(mseg)
                    except Exception as e:
                        mseg = "解码出错"
            self.textBrowser.append(f'{datetime.datetime.now()}:{mseg}')
        else:

            print(res)

    def check_login(self):
        import bs4
        import requests

        self.textBrowser.append(f'{datetime.datetime.now()}:检查登录状态')

        header = {"Accept-Encoding": "gzip, deflate",
                  "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52"}

        res = requests.get('http://10.10.252.1/', headers=header)
        soup = bs4.BeautifulSoup(res.text, "html.parser")

        title_text = soup.select_one('title').text

        if title_text == '上网登录页':
            info = '未认证登录，正在登录'
            self.textBrowser.append(f'{datetime.datetime.now()}:{info}')

            self.deng_lu()
        else:
            if title_text == '注销页':
                # 已经认证登录
                info = '已经认证登录'
            else:
                info = '未知状态'
            self.textBrowser.append(f'{datetime.datetime.now()}:{info}')
