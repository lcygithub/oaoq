#!/usr/bin/env python
#-*- coding:utf8 -*-
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
import re
import urllib2
import sys
import datetime

_Done = 0

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

def deal_target(target):
    return UnicodeDammit(target).unicode_markup

def get_index(soup, target):
    target_list = soup.find_all("td", class_="mc")
    if len(target_list) == 0:
        global _Done
        _Done = 1
        return -1
    for index, name in enumerate(target_list):
        if name.find(text=re.compile(target)):
        # if name.string == target:
            return index + 1
    return -1

def search_userinfo(url):
    doc_html = urllib2.urlopen(url).read()
    _soup = BeautifulSoup(doc_html)
    info = _soup.select("div[class=ucb_grxx]")[1]
    res = {}
    pattern = re.compile(UnicodeDammit("：").unicode_markup)
    for i in range(1,5):
        _res = UnicodeDammit(map(lambda x:re.sub(r"\s","",x),info.contents[i].string.split(":"))[0]).unicode_markup
        _res = pattern.sub(":", _res).split(":")
        res[_res[0]] = _res[1]
    return res

def search(url, target):
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    page_index = get_index(soup, target)
    if page_index != -1:
        tr = soup.find_all("tr")[page_index]
        userinfo = {}
        result = {}
        for index, td in enumerate(tr.children):
            if td != "\n":
                if index == 1:
                    result["排名"] = td.string
                elif index == 3:
                    result["personal-page"] = td.a.get("href")
                    userinfo = search_userinfo(result["personal-page"])
                elif index == 5:
                    result["姓名"] = td.string
                elif index == 7:
                    result["得分"] = td.div.div.string
                elif index == 9:
                    result["答题数"] = td.string
        result.update(userinfo)
        return result
    return False

if __name__ == '__main__':
    start = datetime.datetime.now()
    site = chose_site(sys.argv[1])
    target = deal_target(sys.argv[2])
    try:
        page = int(sys.argv[3])
    except:
        page = 0
    print "请等待......"
    while True:
        result = search(get_url(site, page), target)
        if _Done:
            print "完成搜索 未找到此人的排名信息."
            break
        print "搜索:", get_url(site, page)
        page += 1
        if result:
            print "排名页:" + get_url(site, page-1)
            for key in result:
                print key, ":", result[key]
            print "总耗时:",
            print datetime.datetime.now() - start
            break
