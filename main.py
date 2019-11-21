from PyQt5 import QtWidgets, QtCore, QtGui
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from airtest.cli.parser import cli_setup
from airtest.core.api import *
import airtest.core.android.adb as adb
import main_window
import sys
import shuabao
import jukandian_new
import tst_device
import tools
import dongfangtoutiao
import xuexi
import time
from time import localtime, strftime


class mainwindow(QtWidgets.QWidget, main_window.Ui_Form):
    def __init__(self):
        super(mainwindow, self).__init__()
        self.setupUi(self)
        self.timer = QtCore.QTimer()
        self.timer.start(500)
        self.buttonGroup.setId(self.radioButton, 1)
        self.buttonGroup.setId(self.radioButton, 0)
        devices_adb = adb.ADB()
        devices_list = devices_adb.devices()
        # devices_list = device()
        self.ser_num = ""
        if devices_list is None:
            self.textBrowser.append("设备没有连接好，请先保证手机驱动安装正确！")
        else:
            for phone in devices_list:
                self.textBrowser.append('ID:'+phone[0]+',   state:'+phone[1])
                self.ser_num = phone[0]


    def tst_adb(self):
        self.refreash_textarea_text("设备开始初始化，请耐心等待！")
        self.refreash_textarea_text("请勿点击其他按钮，可能会出错，我也懒得改了！")
        if not cli_setup():
            auto_setup(__file__, logdir=None, devices=[
                "Android://127.0.0.1:5037/"+self.ser_num+"?touch_method=ADBTOUCH",
                ])
        device_poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        self.shuabao_run = shuabao.shuabao(device_poco)
        self.tst_device_run = tst_device.Shell()
        self.tst_device_run.trigger.connect(self.refreash_textarea_text)
        self.jukandian_run = jukandian_new.jukandian(device_poco)
        self.dongfangtoutiao_run = dongfangtoutiao.DongFangTouTiao(device_poco)
        self.dongfangtoutiao_run.trigger.connect(self.refreash_textarea_text)
        self.xuexi_run = xuexi.XueXi(device_poco)
        self.refreash_textarea_text("设备初始化完成，可以开始赚钱了！")

    def click_xuexi(self):
        start_app("cn.xuexi.android")
        time.sleep(3)
        self.xuexi_run.trigger1.connect(self.refreash_textarea_text)
        self.xuexi_run.start()

    def click_shuabao(self):
        start_app("com.jm.video")
        time.sleep(3)
        self.shuabao_run.trigger.connect(self.refreash_textarea)
        self.shuabao_run.start()

    def click_jukandian(self):
        start_app("com.xiangzi.jukandian")
        flag = self.buttonGroup.checkedId()
        self.jukandian_run.trigger1.connect(self.refreash_textarea_text)
        self.jukandian_run.trigger.connect(self.refreash_textarea)
        self.jukandian_run.set_flag(int(flag))
        self.jukandian_run.start()

    def restart_jukandian(self):
        self.jukandian_run.trigger1.connect(self.refreash_textarea_text)
        self.jukandian_run.flag_restart = 0
        self.jukandian_run.restart_jukandian()

    def df_xw(self):
        self.dongfangtoutiao_run.stop_xsp = False
        self.dongfangtoutiao_run.stop_xw = True
        self.dongfangtoutiao_run.flag = 0
        self.dongfangtoutiao_run.start()

    def df_xsp(self):
        self.dongfangtoutiao_run.stop_xw = False
        self.dongfangtoutiao_run.stop_xsp = True
        self.dongfangtoutiao_run.flag = 1
        self.dongfangtoutiao_run.start()

    def refreash_textarea(self):
        self.textBrowser.append(strftime('%Y-%m-%d %H:%M:%S',localtime()))

    def refreash_textarea_text(self, text):
        self.textBrowser.append(text)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myshow = mainwindow()
    myshow.setWindowFlag(0x00040000)  # Qt::WindowStaysOnTopHint,将mainwindow永远置于最前端
    myshow.show()
    sys.exit(app.exec_())