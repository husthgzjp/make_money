from PyQt5.QtCore import *
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from airtest.cli.parser import cli_setup
from airtest.core.api import *
import airtest.core.android.adb as adb

class XueXi(QThread):
    trigger = pyqtSignal()
    trigger1 = pyqtSignal(str)
    def __init__(self,device_poco):
        super(XueXi, self).__init__()
        self.news_vedios = 1 #0表示看新闻，1表示看视频
        self.poco = device_poco


    def set_flag(self,num):
        self.flag = num

    def restart_xuexi(self):
        # keyevent('APP_SWITCH')
        # time.sleep(0.5)
        # self.poco("com.android.systemui:id/recent_igmbutton_clear_all").click()
        stop_app("cn.xuexi.android")
        time.sleep(1)
        start_app("cn.xuexi.android")# 聚看点的包名，startapp是airtest.core.api中的工具
        time.sleep(5)
        self.flag_restart == 1
        self.trigger1.emit("学习强国重启完成！")

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

    def is_ad(self):
        ad_title = self.poco("com.xiangzi.jukandian:id/tv_tool_bar_title")
        if ad_title.exists():
            if ad_title.get_text() == '邀请收徒':
                self.trigger1.emit("广告，跳过！")
                keyevent('BACK')
                return True
        else:
            return False

    def shoucang(self):
        shouc = self.poco("android.widget.LinearLayout").offspring("android:id/content").child("android.widget.FrameLayout").child("android.widget.FrameLayout")[0].child("android.widget.FrameLayout").child("android.widget.LinearLayout").child("android.widget.LinearLayout")[1].child("android.widget.ImageView")[0]
        try:
            shouc.click()
        except:
            self.trigger1.emit('收藏异常！')

    def comment(self):
        pinglun = self.poco("android.widget.TextView")
        if pinglun.exists():
            pinglun.click()
            text('习主席威武，中国必将更加富强！', enter=True)
            fabu = self.poco(text="发布")
            try:
                fabu.click()
            except:
                self.trigger1.emit("评论异常！")

    def watch_news(self, num):
        num1 = num
        for i in range(0, 5):
            yaowen = self.poco("android.widget.LinearLayout").offspring("cn.xuexi.android:id/ui_common_base_ui_activity_content").child("android.widget.RelativeLayout").child("android.widget.LinearLayout").offspring("cn.xuexi.android:id/view_pager").child("android.widget.FrameLayout").child("android.widget.LinearLayout").child("android.widget.LinearLayout").child("android.view.ViewGroup").child("android.widget.LinearLayout")[1]
            if yaowen.exists():
                if num1==1:
                    yaowen.click()
                break
            else:
                if i == 3:
                    self.restart_xuexi()
                    self.trigger1.emit('重启学习强国！')
                    num1 = 1
                    time.sleep(5)
                    continue
                keyevent('BACK')
                self.trigger1.emit('不在首页，回退！第'+str(i)+'次')
                time.sleep(2)
        news_list =self.poco("android.widget.ListView").children()
        try:
            for news_element in news_list:
                news_title = news_element.offspring("android.widget.TextView")
                if news_title.exists():
                    self.trigger1.emit(news_title.get_text())
                    news_element.click()
                    self.swipe(1,6)
                    self.swipe(2,5)
                    keyevent('BACK')
            self.swipe(1, 1)
            time.sleep(1)
        except:
            self.trigger1.emit("新闻列表异常！")

    def watch_vedios(self,num):
        num1 = num
        for i in range(0, 5):
            vedio_learn = self.poco("cn.xuexi.android:id/home_bottom_tab_button_contact")
            if vedio_learn.exists():
                if num1==1:
                    vedio_learn.click()
                break
            else:
                if i == 3:
                    self.restart_xuexi()
                    self.trigger1.emit('重启学习强国！')
                    num1 = 1
                    time.sleep(5)
                    continue
                keyevent('BACK')
                self.trigger1.emit('不在首页，回退！第'+str(i)+'次')
                time.sleep(2)
        vedios_list =self.poco("android.widget.ListView").children()
        try:
            for news_element in vedios_list:
                news_title = news_element.offspring("android.widget.TextView")
                if news_title.exists():
                    self.trigger1.emit(news_title.get_text())
                    news_element.click()
                    self.swipe(1,2)
                    if num == 2 or num == 5:
                        self.comment()
                        self.shoucang()
                    time.sleep(60)
                    keyevent('BACK')
            self.swipe(1, 2)
            time.sleep(1)
        except:
            self.trigger1.emit("视频列表异常！")

    def run(self):
        self.trigger1.emit('开始学习强国！')
        num = 0
        while True:
            if num >=65530:
                num = 2
            else:
                num += 1
            if self.news_vedios ==0 :
                self.watch_news(num)
                if num > 3:
                    num = 0
                    self.news_vedios = 1
            elif self.news_vedios ==1:
                self.watch_vedios(num)
                if num > 20:
                    num = 0
                    self.news_vedios = 0




