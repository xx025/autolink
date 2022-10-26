#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/10/10 8:30 下午
# @Author : LeiXueWei
# @CSDN/Juejin/Wechat: 雷学委
# @XueWeiTag: CodingDemo
# @File : shortcut.py.py
# @Project : absentee


import os


def create_shortcut(bin_path: str, shortcut_path: str, name: str, desc: str):
    """

    :param bin_path: 可执行文件路径
    :param shortcut_path: 设置快捷方式的路径
    :param name: 快捷方式名字
    :param desc: 快捷方式描述
    :return:
    """
    """
    Path – As what file should the shortcut be created?
    Target – What command should the desktop use?
    Arguments – What arguments should be supplied to the command?
    StartIn – What folder should the command start in?
    Icon – (filename, index) What icon should be used for the shortcut?
    Description – What description should the shortcut be given?    
    """
    """
    这里学委调用了winshell的CreateShortcut函数。
    传入4个参数，分别为：快捷方式的路径，exe文件的路径，图标路径，还有描述信息。
    """
    try:
        import winshell
        shortcut = os.path.join(shortcut_path, name + ".lnk")
        winshell.CreateShortcut(
            Path=shortcut,
            Target=bin_path,
            Icon=(bin_path, 0),
            Description=desc
        )
        print("创建快捷方式成功")
        return True
    except ImportError as err:
        print(err)

    return False
