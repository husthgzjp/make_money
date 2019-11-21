import os
import random
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class shuabao(QThread):
    trigger = pyqtSignal()
    def __init__(self,device_poco):
        super(shuabao, self).__init__()
        self.poco = device_poco
    def click(self):
        self.poco.click()
        os.system('adb shell input swipe 1000 850 1000 850')

    def click_power(self):
        os.system("adb shell input keyevent 26")
        time.sleep(0.5)
    def run(self):
        for i in range(0, 10000):
            sleep_time = random.randint(5, 15)
            print(sleep_time)
            time.sleep(0.5)
            # if sleep_time > 3:
            #     self.click()
            time.sleep(sleep_time)
            self.swipe(1,1)
            self.trigger.emit()

    def swipe(self,up_down=1,num=3):#up_down=1表示上滑，2表示下滑，其他不操作，num表示滑动次数
        for i in range(0, num):
            if up_down == 1:
                self.poco.swipe([0.5, 0.7], [0.5, 0.3], duration=0.5)
                time.sleep(0.5)
            elif up_down == 2:
                self.poco.swipe([0.5, 0.3], [0.5, 0.7], duration=0.5)
                time.sleep(0.5)
            else:
                pass


