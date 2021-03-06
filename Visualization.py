#!/usr/bin/env python
#-*- coding:utf8 -*-
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
import re
import urllib2
import sys
import datetime

_Done = 0
_res = {}

def chose_site(choice):
    if choice.lower() == "python":
        return "http://wenda60.com/testdetail/leaderboard/tid-29"
    if choice.lower() == "c++":
        return "http://wenda60.com/testdetail/leaderboard/tid-28"
    if choice.lower() == "c":
        return "http://wenda60.com/testdetail/leaderboard/tid-27"
    return -1

def get_url(site, page=0):
    if page == 0:
        return site + ".html"
    else:
        return site + "/page-" + str(page) + ".html"

def get_data(url):
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    score = soup.find_all("div", class_="seconds2")
    global _res
    if len(score) == 0:
        global _Done
        _Done = 1
        return -1
    for dot in score:
        int_dot = int(dot.string)
        if int_dot in _res.keys():
            _res[int_dot] += 1
        else:
            _res[int_dot] = 1
    return 1

if __name__ == '__main__':
    start = datetime.datetime.now()
    site = chose_site(sys.argv[1])
    try:
        page = int(sys.argv[2])
    except IndexError:
        page = 0
    print "请等待......"
    while True:
        get_data(get_url(site, page))
        if _Done:
            print "完成搜索"
            break
        print "搜索:", get_url(site, page)
        print _res
        page += 1
    data = open("data", "a")
    for key in _res:
        data.write(str(key)+" "+str(_res[key])+"\n")
    data.close()
    print datetime.datetime.now() - start
