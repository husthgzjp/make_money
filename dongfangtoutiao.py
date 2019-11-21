#!/usr/bin/env python
# encoding: utf-8
__author__ = "pascal"

from airtest.core.api import *
from poco.exceptions import PocoNoSuchNodeException
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
import random
import datetime
from myutils.device_utils import *
from PyQt5.QtCore import *
import random

# 应用包名和启动Activity
package_name = 'com.songheng.eastnews'
activity = 'com.oa.eastfirst.activity.WelcomeActivity'

# 新闻父节点
btn_news_root="com.songheng.eastnews:id/go"
# 新闻标题
btn_news_node_title='com.songheng.eastnews:id/pn'
# 新闻作者
btn_news_node_author='com.songheng.eastnews:id/a5a'
# 视频页签按钮
btn_video='com.songheng.eastnews:id/js'
# 视频父节点
btn_video_root='com.songheng.eastnews:id/a0j'
# 视频标题
btn_video_node_title='com.songheng.eastnews:id/or'
# 视频播放按钮
btn_video_node_play='com.songheng.eastnews:id/pd'
# 视频标签
vedio_flag='com.songheng.eastfirst.business.video.view.widget.ijkplayer.h'
# 继续赚钱
btn_continue='com.songheng.eastnews:id/x1'
# 领取顶部金币
btn_receive='com.songheng.eastnews:id/asd'
#转圈圈的红包标志
hongbao_flag = 'com.songheng.eastnews:id/aq5'

#无线连接手机
#device_1 = connect_device('android:///192.168.3.2:8888?cap_method=javacap&touch_method=adb')

#usb连接手机
#设备id
# device_id = 'cb49d48'
# device_1 = Android(device_id)

class DongFangTouTiao(QThread):
    """
    东方头条
    """
    trigger = pyqtSignal(str)
    def __init__(self,device_poco):
        super(DongFangTouTiao, self).__init__()
        # 保留最新的5条新闻标题
        self.poco = device_poco
        self.news_titles = []
        # 视频播放时间
        self.video_play_time = 32
        # 间隔获取标题栏的金币
        self.interval_time = 5
        # 跳过的页数
        self.skip_page = 0
        self.flag = 0
        self.stop_xw = True
        self.stop_xsp = True

    def run(self):
        # 1.预加载 等待应用打开
        sleep(6)
        if self.flag == 0:
            # 2.获取顶部的金币
            self.get_top_title_coin()
            # 3.查看推荐的新闻
            self.__skip_same_pages()
            self.watch_nuws()
            # 4.看视频
            # self.__video()
        elif self.flag == 1:
            # 5.看小视频
            self.mini_video()
    def watch_nuws(self):
        try:
            while self.stop_xw:
                self.watch_news_recommend()
                main_page = self.poco("com.songheng.eastnews:id/kh")
                if not main_page.exists():
                    print('不是首页!')
                    self.__back_to_list()
                    main_page.click()

                print('查看一页完成，继续查看下一页的新闻。')
                # 继续赚钱
                self.skip_window()
                # 顶部金币领取
                self.get_top_title_coin()
                # 滑动下一页的新闻
                self.poco.swipe([0.5, 0.8], [0.5, 0.3], duration=1)
        except Exception as e:
            print('error')

    def skip_window(self):
        '''如果弹出窗口是否继续赚钱时，点击继续赚钱'''
        window = self.poco(btn_continue)
        if window.exists():
            window.click()

    def watch_news_recommend(self):
        """
        查看新闻
        :return:
        """
        # 1.推荐的所有新闻元素
        lv_elements = self.poco(btn_news_root).children()
        if not lv_elements.exists():
            print('新闻列表不存在')
            return
        # 下面的循环经常会报错：PocoNoSuchNodeException
        # 遍历每一条新闻
        for news_element in lv_elements:
            # 1.查看要闻
            self.__read_key_news()
            # 2.新闻标题
            news_title = news_element.offspring(btn_news_node_title)
            # 作者
            author_element = news_element.offspring(btn_news_node_author)
            # 3.注意：必须保证元素加载完全
            # 下面会报错：hrpc.exceptions.RpcRemoteException: java.lang.IndexOutOfBoundsException
            try:
                if not news_title.exists() or not author_element.exists():
                    print("【标题】元素加载不完全" if not news_title.exists() else "【发布者】元素加载不完全")
                    continue
            except Exception as e:
                print("******注意注意注意！exist()方法报错******")
                print("判断下面两个东西是否存在")
                print(e)
                self.__back_to_list()
                print('回到首页')
                return
            # 4.过滤广告
            # 到这里标识此条新闻：是一条有效的新闻【包含广告】
            # 注意：部分广告【包含点击标题就自动下载，左下角显示广告字眼等】要过滤掉
            # 场景一：
            if news_element.attr('name') == 'android.widget.FrameLayout':
                print('广告！这是一个FrameLayout广告，标题是:%s' % news_title.get_text())
                continue
            # 常见二：点击标题直接下载其他应用
            ads_tips_element = news_element.offspring(name='com.songheng.eastnews:id/a4f', text='广告通')
            if ads_tips_element.exists():
                print('广告！这是一个【广点通】广告，标题是:%s' % news_title.get_text())
                continue
            # 常见三：有效角标识是广告的图标【奇虎广告】
            ads_tips_element2 = news_element.offspring('com.songheng.eastnews:id/q5')
            if ads_tips_element2.exists():
                print('广告！广告标题是：%s' % news_title.get_text())
                continue
            # 已经查看过了，过滤掉
            if news_title.get_text() in self.news_titles:
                print('已经看过了，不看了！')
                continue
            # ==========================================================================
            # 5.查看新闻
            # 下面是一条有效的新闻
            # 新闻类型
            # 文字0、视频1、图片2
            news_type = self.get_news_type(news_element)
            if 5 == len(self.news_titles):
                self.news_titles.pop()
            self.news_titles.insert(0, news_title.get_text())
            print('准备点击刷新闻，这条新闻的标题是:%s' % news_title.get_text())
            # 以上还在主界面
            # 如果是正常的新闻就点击进去
            news_title.click()
            # 等待新闻元素都加载完全
            sleep(2)
            # 评论拿金币和发表按钮
            comments_with_coins = self.poco('com.songheng.eastnews:id/mh')
            submit_btn_element = self.poco("com.songheng.eastnews:id/m6").offspring('com.songheng.eastnews:id/vw')
            # 记录时长的标识
            # 不存在就直接返回
            red_coin_element = self.poco(hongbao_flag)
            if not red_coin_element.exists():
                print('当前新闻没有红包，返回！')
                self.__back_keyevent()
                continue
            if comments_with_coins.exists() and comments_with_coins.get_text() == '评论拿金币':
                oldtime = datetime.datetime.now()
                # 文字
                if news_type == 0:
                    while True:
                        print("循环-滑动查看内容")
                        self.__swipe(True if random.randint(0, 10) > 3 else False)
                        # 如果发现有【点击查看全文】按钮，点击查看全文
                        see_all_article_element = self.poco('点击查看全文')
                        if see_all_article_element.exists():
                            print('点击展开全文内容...')
                            see_all_article_element.focus('center').click()
                            # 注意：有的时候点击展开全文，会点击到图片，需要规避一下
                            # while self.poco('com.songheng.eastnews:id/lz').exists():
                            #     print('不小心点到图片了，返回到新闻详情页面')
                            #     self.__back_keyevent()
                        newtime = datetime.datetime.now()
                        interval_time = (newtime - oldtime).seconds
                        if interval_time >= 30:
                            print('阅读30秒新闻完成')
                            break
                        self.__read_key_news()
                # 视频
                elif news_type == 1:
                    while True:
                        print("循环-滑动查看视频")
                        newtime = datetime.datetime.now()
                        interval_time = (newtime - oldtime).seconds
                        if interval_time >= 30:
                            print('观看30秒视频完成')
                            break
                        self.__read_key_news()
            else:
                print('这是一篇没有金币的文章！')
            self.__back_to_list()

    def __video(self):
        """
        查看视频
        :return:
        """
        self.poco(btn_video).click()
        while True:
            # 视频列表
            self.poco(btn_video_root).wait_for_appearance()
            sleep(2)
            self.__read_key_news()
            video_elements = self.poco(btn_video_root).children()
            print('video items是否存在：')
            print(video_elements.exists())
            # 遍历视频
            # 注意：视频播放完全可以提前返回
            for video_element in video_elements:
                try:
                    # 1.标题元素
                    video_title_element = video_element.offspring(btn_video_node_title)
                    # 播放按钮
                    video_play_element = video_element.offspring(btn_video_node_play)
                    # 2.必须保证【视频标题】和【播放按钮】都可见
                    if not video_title_element.exists() or not video_play_element.exists():
                        continue
                    # 3.标题
                    video_title = video_element.offspring(btn_video_node_title).get_text()
                    print('当前视频的标题是:%s,播放当前视频' % video_title)
                    # 点击播放视频
                    video_play_element.focus("center").click()
                    # 4.播放视频
                    self.play_video()
                    print('播放下一个视频')
                    self.__back_keyevent()
                except Exception:
                    print('发生异常，继续下一个视频播放')
                    continue
            # 滑动到下一页的视频
            if not self.poco(btn_video).exists():
                self.__back_keyevent()
            self.poco.swipe([0.5, 0.8], [0.5, 0.3], duration=0.2)

    def mini_video(self):
        """
        查看小视频
        :return:
        """
        sp_button = self.poco('com.songheng.eastnews:id/km')
        if not sp_button.exists():
            self.__back_to_list
        else:
            sp_button.click()
            xsp_button = self.poco("com.songheng.eastnews:id/aju").children()[1]
            xsp_button.click()

        # 加载出列表元素,点击第一项进入
        first_xsp = self.poco('com.songheng.eastnews:id/go').children()[0]
        first_xsp.click()
        while self.stop_xsp:
            sleep(random.randint(8,15))
            # 向上滑动
            self.poco.swipe([0.5, 0.7], [0.5, 0.3], duration=0.5)

    def __swipe(self, up_or_down):
        """
        滑动单条新闻
        :param up_or_down: true：往上滑动；false：往下滑动【慢慢滑动】
        :return:
        """
        if up_or_down:
            self.poco.swipe([0.5, 0.7], [0.5, 0.3], duration=0.5)
        else:
            self.poco.swipe([0.5, 0.3], [0.5, 0.7], duration=0.5)

    def get_news_type(self, news_element):
        """
        获取新闻的类型【文字0、视频1、图片2】
        :param news_element:
        :return:
        """
        # 默认是文字新闻
        type = 0
        video_element = self.poco(vedio_flag)
        if video_element.exists():
            type = 1
        return type

    def __wait_for_element_exists(self, elements):
        """
        一直等待元素出现
        :param elements: 元素列表
        :return:
        """
        try:
            while True:
                # 元素是否存在
                element_exists = True
                # 元素列表
                for element in elements:
                    if not element.exists():
                        element_exists = False
                        break
                    else:
                        continue
                if element_exists:
                    break
                else:
                    print('元素暂时找不到，继续等待')
                    continue
        except PocoNoSuchNodeException as e:
            print('找不到这个元素异常')

    def __remove_disturb(self):
        # 退出对话框元素
        exit_dialog_tips_element = self.poco('com.songheng.eastnews:id/xm')
        if exit_dialog_tips_element.exists():
            self.__back_keyevent()


    def __read_key_news(self):
        """
        处理【要闻】对话框，需要阅读
        :return:
        """
        # 对于弹出来的要闻对话框，需要处理
        key_news_element = self.poco(name='com.songheng.eastnews:id/xj', text='立即查看')
        if key_news_element.exists():
            print('要闻推送！需要看一下')
            key_news_element.click()

            # TODO  需不需要另外停留
            sleep(3)
            self.__back_keyevent()

    def norm_task(self):
        """
        普通任务领取金币【包含：签到、大转盘】
        :return:
        """
        self.__sign_in()
        self.__lottery()

    def play_video(self):
        """
        播放一个视频
        :return:
        """
        video = self.poco(vedio_flag)
        if not video.exists():
            return
        # 开始时间
        start_time = datetime.datetime.now()

        while True:
            # 视频播放结束或者超过30秒
            scale_element = self.poco('com.songheng.eastnews:id/aq0')

            if scale_element.exists():
                print('视频播放完了，结束播放。')
                break

                # 结束时间
            end_time = datetime.datetime.now()

            # 时间间隔
            interval_time = (end_time - start_time).seconds

            if interval_time > 30:
                print('播放超过30秒，结束播放。')
                break

    def get_top_title_coin(self):
        """
        顶部金币领取
        仅仅在新闻首页的时候才可以领取
        :return:
        """
        get_coin_element = self.poco(name=btn_receive, text="领取")
        if get_coin_element.exists():
            print('顶部有金币可以领取！')
            get_coin_element.click()
            print('领完金币后可以关闭对话框！')
            # 关掉对话框
            self.__back_keyevent()
        else:
            print('顶部没有金币或者不在首页')

    def __skip_same_pages(self):
        """
        往下滑动【跳过】几页
        :param num:
        :return:
        """
        current_page = 0
        while current_page < self.skip_page:
            self.poco.swipe([0.5, 0.8], [0.5, 0.3], duration=1)
            current_page += 1
        print('跳过结束，继续获取金币')

    def __back_keyevent(self):
        """
        返回的时候可能会出现关键要闻
        :return:
        """
        self.__read_key_news()
        keyevent('BACK')

    def __back_to_list(self):
        """
        回退到首页
        :return:
        """
        print('准备回到首页')
        for i in range(0, 5):
            if not self.poco(btn_news_root).exists():
                print('回退一次')
                self.__back_keyevent()
            else:
                return
        if not self.poco(btn_news_root).exists():
            self.restart_toutiao()


    def restart_toutiao(self):
        keyevent('APP_SWITCH')
        time.sleep(0.5)
        self.poco("com.android.systemui:id/recent_igmbutton_clear_all").click()
        time.sleep(1)
        start_app(package_name)# 聚看点的包名，startapp是airtest.core.api中的工具
        time.sleep(5)
        self.trigger.emit("头条重启完成！")


if __name__ == "__main__":
    dftt = DongFangTouTiao()
    dftt.run()
