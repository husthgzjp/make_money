import json
from airtest.core.api import *


def kill_app(package_name):
    keyevent('APP_SWITCH')
    time.sleep(0.5)
    # .poco("com.android.systemui:id/recent_igmbutton_clear_all").click()


def start_my_app(package_name, activity_name):
    os.system('adb shell am start -n %s/%s' % (package_name, activity_name))


def kill_all():
    keyevent("HOME")
    keyevent("MENU")


def print_ui_tree(poco):
    print('打印整个UI树')
    print('==' * 30)
    print(json.dumps(poco.agent.hierarchy.dump(), indent=4))


def write_ui_tree(poco):
    str = json.dumps(poco.agent.hierarchy.dump(), indent=4)
    with open('log.txt', 'w', encoding='utf-8') as file:
        file.write(str)