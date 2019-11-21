# -*- encoding=utf8 -*-
__author__ = "asus"

from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from airtest.cli.parser import cli_setup

if not cli_setup():
    auto_setup(__file__, logdir=True, devices=[
            "Android://127.0.0.1:5037/FKC4C16629002059?touch_method=ADBTOUCH",
    ])


# script contentpoco("android.widget.FrameLayout").child("android.widget.FrameLayout")
print("start...")
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
keyevent('BACK')
poco.swipe([0.5, 0.7], [0.5, 0.3], duration=0.5)



# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath=True)