# -*- coding: utf-8 -*-

from time import localtime, strftime, strptime


def formatTimestamp(timestamp):
    time_local = localtime(timestamp)
    # 转换成新的时间格式(2016-05-05 20:28:54)
    return strftime("%Y-%m-%d %H:%M:%S", time_local)


def formatTime(str_time):
    str_time = strptime(str_time, "%Y-%m-%d %H:%M")
    return strftime("%Y-%m-%d %H:%M:%S", str_time)
    pass
