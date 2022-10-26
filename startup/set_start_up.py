# https://zhuanlan.zhihu.com/p/445958233
# C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp
#  所有用户 管理员级别自启动
#
# C:\Users\username\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
# 用户级别 自启动
import os

from startup.create_shortcut import create_shortcut
from startup.remove_shortcut import remove_shortcut


def get_startup_path():
    return os.getenv("APPDATA") + r'\Microsoft\Windows\Start Menu\Programs\Startup'


def get_exe_path():
    global application_path
    import os
    import sys

    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', False):
        application_path = os.path.abspath(sys.executable)
    elif __file__:
        application_path = os.path.abspath(os.path.abspath(__file__))

    print(application_path)

    return application_path


def set_startup(name, desc):
    remove_startup(name=name)
    # 有相同名字则移除 没有正常略过
    return create_shortcut(bin_path=get_exe_path(), shortcut_path=get_startup_path(), name=name,
                           desc=desc)


def remove_startup(name):
    # os.path.join
    # 移除开机启动

    path = os.path.join(get_startup_path(), name)

    return remove_shortcut(shortcut_path=path)


def check_startup(name):
    path = os.path.join(get_startup_path(), name)
    return os.path.exists(path=path + '.lnk')
