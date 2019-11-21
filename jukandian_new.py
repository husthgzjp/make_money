from PyQt5.QtCore import *
from airtest.core.api import *

class jukandian(QThread):
    trigger = pyqtSignal()
    trigger1 = pyqtSignal(str)
    def __init__(self,device_poco):
        super(jukandian, self).__init__()
        self.flag = 1  # 0表示看推荐，1表示看视频
        self.flag_restart = 1 #0表示重启
        self.poco = device_poco
        self.recommends_button = "com.xiangzi.jukandian:id/ll_tab1_layout"
        self.recommends_list = "com.xiangzi.jukandian:id/rv_artical_list_view"
        self.vedio_button = "com.xiangzi.jukandian:id/ll_tab2_layout"
        self.vedio_list = "com.xiangzi.jukandian:id/rv_video_list_view"

    def set_flag(self,num):
        self.flag = num

    def restart_jukandian(self):
        # keyevent('APP_SWITCH')
        # time.sleep(0.5)
        # # self.poco("com.android.systemui:id/recent_igmbutton_clear_all").click()
        # # time.sleep(1)
        # start_app("com.xiangzi.jukandian") # 聚看点的包名，startapp是airtest.core.api中的工具
        # time.sleep(5)
        # self.flag_restart == 1
        stop_app("com.xiangzi.jukandian")
        time.sleep(1)
        start_app("com.xiangzi.jukandian")
        time.sleep(5)
        self.flag_restart == 1
        self.trigger1.emit("聚看点重启完成！")

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

    def lingqu_jiangli(self):
        lingqu_button = self.poco("com.xiangzi.jukandian:id/rl_lingqu_par")
        if lingqu_button.exists():
            lingqu_button.click()
            time.sleep(0.5)
            keyevent('BACK')
            time.sleep(0.5)
        # shall_window = self.poco("com.xiangzi.jukandian:id/dialog_share_layout")
        # if shall_window.exists():
        #     self.poco("com.xiangzi.jukandian:id/close_dialog_layout").click()


    def refreash_recommends(self):  # 点击一下主页下的推荐小图标
        try:
            self.poco(self.recommends_button).click()
        except:
            print('刷新推荐页异常！')
            time.sleep(3)
            return

    def watch_recommends(self):  # 看推荐
        recommends_page = self.poco(self.recommends_button)#得到推荐页
        if not recommends_page.exists():  # 判断推荐页在不在，如果不在的话重启聚看点
            self.restart_jukandian()
            time.sleep(3)
            self.refreash_recommends()
        lv_elements = self.poco(self.recommends_list).children()  #得到推荐页的新闻列表
        if not lv_elements.exists():  # 如果新闻列表不存在，那么有可能到了退出界面，页可能到了其他界面
            print('新闻列表不存在')
            quit_page = self.poco("com.xiangzi.jukandian:id/cancel_quit")  # 退出界面是否存在
            if quit_page.exists():
                quit_page.click()  # 点击继续啊赚钱
                time.sleep(1)
            else:
                keyevent('BACK')
                time.sleep(1)
            return
        try:
            self.lingqu_jiangli()
            for news_element in lv_elements:
                news_title = news_element.offspring("com.xiangzi.jukandian:id/item_artical_three_title_tv")
                if news_title.exists():
                    print(news_title.get_text())
                    news_element.click()
                    self.is_ad()
                    self.swipe(1, 10)
                    self.swipe(2, 8)
                    keyevent('BACK')
                    time.sleep(0.5)
            self.trigger.emit()
            self.swipe(1,1)
            time.sleep(2)
        except Exception as e:
            print('error')

    def refreash_videos(self):
        try:
            self.poco(self.vedio_button).click()
        except:
            print('启动异常！')
            time.sleep(3)
            return
    def watch_vedios(self):
        vedio_page = self.poco(self.vedio_button)
        if not vedio_page.exists():
            self.restart_jukandian()
            time.sleep(3)
            self.refreash_videos()

        lv_elements = self.poco(self.vedio_list).children()
        if not lv_elements.exists():
            print('新闻列表不存在')
            quit_page = self.poco("com.xiangzi.jukandian:id/cancel_quit")
            if quit_page.exists():
                quit_page.click()
                time.sleep(2)
            else:
                keyevent('BACK')
                time.sleep(1)
        try:
            for news_element in lv_elements:
                news_title = news_element.offspring("com.xiangzi.jukandian:id/item_video_title")
                if news_title.exists():
                    print(news_title.get_text())
                    news_element.click()
                    if self.is_ad():
                        continue
                    time.sleep(10)
                    self.swipe(1, 5)
                    self.swipe(2, 10)
                    keyevent('BACK')
                    time.sleep(0.5)
            self.trigger.emit()
            self.swipe(1,1)
            time.sleep(2)
        except Exception as e:
            print('error')

    def run(self):
        while True:
            if self.flag_restart == 0:#重启聚看点
                self.restart_jukandian()
            else:
                if self.flag == 0:
                    self.watch_recommends()
                else:
                    self.watch_vedios()



if __name__ == '__main__':
    jukandian_run= jukandian()
    jukandian_run.watch_recommends()
