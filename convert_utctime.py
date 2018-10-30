#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import datetime


def iso_utc_to_tz(utcstr, iso_tz):
    """
    :param utcstr: utc时间(str)
    :param iso_tz: 时区(int)
    :return: 相应时区的时间
    """
    utc_time = datetime.datetime.strptime(utcstr, '%Y-%m-%d %H:%M:%S')
    td = datetime.timedelta(hours=iso_tz)
    iso_time = (utc_time + td).strftime('%Y-%m-%d %H:%M:%S')
    return iso_time


def local2utc(local_str, iso_tz=-8):
    """
    :param local_str: 北京时间(str)
    :param iso_tz: 时区(int)
    :return: 相应时区的时间
    """
    local_time = datetime.datetime.strptime(local_str, '%Y-%m-%d %H:%M:%S')
    td = datetime.timedelta(hours=iso_tz)
    utc_time = (local_time + td).strftime('%Y-%m-%d %H:%M:%S')
    return utc_time


if __name__ == '__main__':
    print(type(iso_utc_to_tz(utcstr='2018-09-10 00:10:00', iso_tz=8)))
    utc_time = local2utc(local_str='2018-09-19 10:05:00')
    print(utc_time)
    print(type(utc_time))
