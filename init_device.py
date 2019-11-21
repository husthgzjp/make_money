from PyQt5.QtCore import pyqtSignal, QThread
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from airtest.cli.parser import cli_setup
from airtest.core.api import *
import tools

class init_devices(QThread):
    trigger = pyqtSignal()
    def __init__(self):
        super(init_devices, self).__init__()
        if not cli_setup():
            auto_setup(__file__, logdir=True, devices=[
            "Android://127.0.0.1:5037/FKC4C16629002059?touch_method=ADBTOUCH",
            ])
        self.poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        #"mCurrentFocus=Window{5842cb5 u0 com.xiangzi.jukandian/com.xiangzi.jukandian.activity.MainActivity}"
        self.jukandian_package = "com.xiangzi.jukandian"
        self.jukandian_activity = "com.xiangzi.jukandian.activity.MainActivity"
        #"mCurrentFocus=Window{9916f10 u0 com.jm.video/com.jm.video.ui.main.MainActivity}"
        self.shuabao_package = "com.jm.video"
        self.shuabao_activity = "com.jm.video.ui.main.MainActivity"
        tools.start_my_app(self.shuabao_package, self.shuabao_activity)
