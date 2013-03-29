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

def search(url, target):
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    page_index = get_index(soup, target)
    if page_index != -1:
        tr = soup.find_all("tr")[page_index]
        result = {}
        for index, td in enumerate(tr.children):
            if td != "\n":
                if index == 1:
                    result["rank"] = td.string
                elif index == 3:
                    result["page"] = td.a.get("href")
                elif index == 5:
                    result["name"] = td.string
                elif index == 7:
                    result["score"] = td.div.div.string
                elif index == 9:
                    result["counts"] = td.string
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
    print "just wait......"
    while True:
        result = search(get_url(site, page), target)
        if _Done:
            print "Done...but didn't found what you want"
            break
        print "searching page: ", get_url(site, page)
        page += 1
        if result:
            print "site-page:  " + get_url(site, page-1)
            for key in result:
                print key, ":", result[key]
            print "total use time: ",
            print datetime.datetime.now() - start
            break
