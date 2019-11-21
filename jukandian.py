import os
import time
from PyQt5.QtCore import *
import xml.dom.minidom

class jukandian(QThread):
    trigger = pyqtSignal()
    def __init__(self):
        super(jukandian, self).__init__()

    def click(self,x,y):
        cmd = 'adb shell input tap'+' '+str(x)+' '+str(y)
        os.system(cmd)
        print('tap', cmd)
        time.sleep(0.5)

    def slip_up(self):
        start = str(500)+" "+str(1500)
        end = str(500)+" "+str(1000)
        cmd = 'adb shell input swipe '+start+" "+end
        os.system(cmd)
    def click_power(self):
        os.system("adb shell input keyevent 26")
        time.sleep(0.5)
    def run(self):
        for i in range(0, 10000):
            print('start!')
            for j in range(0,5):
                self.slip_up()
                time.sleep(0.5)
            time.sleep(1)
            os.system('adb shell /system/bin/uiautomator dump --compressed /data/local/tmp/uidump.xml')
            time.sleep(1)
            os.system('adb pull /data/local/tmp/uidump.xml ')
            time.sleep(1)
            DOMTree = xml.dom.minidom.parse("uidump.xml")
            collection = DOMTree.documentElement
            nodes = collection.getElementsByTagName("node")
            for node in nodes:
                content = node.getAttribute("content-desc")
                bounds = node.getAttribute("bounds")
                if '娱乐' in content or '情感' in content :
                    y = int(bounds.split(']')[0].split(',')[1])
                    x = int(bounds.split(']')[0].split(',')[0].split('[')[1])
                    if x>10:
                        print(x,y)
                        self.click(x+10,y+10)
                        print('click_over')
                        time.sleep(1)
                        break
            self.trigger.emit()


