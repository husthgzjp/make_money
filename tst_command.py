# datals=[]
# f= open("1.txt")
# for line in f:
#     line = line.replace("\n","")
#     print(line)
# f.close()
# # line=line.replace("\n","")
# # datals.append(list(map(eval,line.split(","))))
#
# # from airtest.core.api import *
# # from poco.exceptions import PocoNoSuchNodeException
# # import random
# # import datetime
# #
# # from poco.drivers.android.uiautomation import AndroidUiautomationPoco
# # poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
# #
# # # elements_pass = poco("com.songheng.eastnews:id/xw")
# # # elements_pass.click()
# # def swipe(up_down=1,num=3):
# #     for i in range(0, num):
# #         if up_down==1:
# #             poco.swipe([0.5, 0.7], [0.5, 0.3], duration=0.5)
# #             time.sleep(0.5)
# #         else:
# #             poco.swipe([0.5, 0.3], [0.5, 0.7], duration=0.5)
# #             time.sleep(0.5)
# # try:
# #     while True:
# #         lv_elements = poco("com.xiangzi.jukandian:id/rv_artical_list_view").children()
# #         if not lv_elements.exists():
# #             print('新闻列表不存在')
# #         for news_element in lv_elements:
# #             news_title = news_element.offspring("com.xiangzi.jukandian:id/item_artical_three_title_tv")
# #             if news_title.exists():
# #                 print(news_title.get_text())
# #                 news_element.click()
# #                 swipe(1, 10)
# #                 keyevent('BACK')
# #                 time.sleep(0.5)
# #                 swipe(1,1)
# #                 time.sleep(2)
# # except Exception as e:
# #     print('error')
# #


print(device_list)