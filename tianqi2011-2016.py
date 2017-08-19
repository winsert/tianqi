#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 从lishi.tianqi.com下载2011年1月至今的每日气象数据

__author__ = 'winsert@163.com'

import requests, random, lxml, sqlite3

from bs4 import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


class weather():
    
    def __init__(self):

        self.user_agent_list = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]

    # requests页面
    def getUrl(self, url): 
        UA = random.choice(self.user_agent_list) #随机选出一个user_agent
        headers = {'User-Agent': UA} #构造一个完整的user-agent
        try:
            response = requests.get(url, headers=headers)
            return response
        except Exception, e:
            print 'requests：',url, '时发生以下错误：'
            print e
            sys.exit()

    # 解析页面
    def getSoup(self, url):
        content = self.getUrl(url)
        soup = BeautifulSoup(content.text, 'lxml')
        all = soup.find('div', class_="tqtongji2").find_all('ul')
        tmp_list = []
        for ur in all:
            #print ur.get_text()
            day_list = ur.get_text().splitlines()
            #print day_list
            tmp_list.append(day_list)

        #print tmp_list
        return tmp_list

    # 在tianqi.db中创建yyyy表
    def createTable(self, year):
        yyyy = year

        try:
            conn = sqlite3.connect('tianqi.db')
            cursor = conn.cursor()
            cursor.execute('create table %r (date char(12) primary key not null, H_temp real, L_temp real, weather char(40), wind_direction char(40), wind_speed char(40))' %yyyy)
            cursor.close()
            conn.close()
            return
        except:
            return

    # 向yyyy表存储数据
    def save2data(self, year, data):
        yyyy = year
        data_list = data
        tmp_len = len(data_list) # 计算列表的项目数
        for i in range(1, tmp_len): #从1开始取列表，0是无用列表
            date = str(data_list[i][1]).encode('utf-8') #日期
            ht = float(data_list[i][2]) #最高气温
            lt = float(data_list[i][3]) #最低气温
            w =  str(data_list[i][4])  #天气
            wd = str(data_list[i][5]) #风向
            ws = str(data_list[i][6]) #风速
            print date, ht, lt, w, wd, ws

            conn = sqlite3.connect('tianqi.db')
            cursor = conn.cursor()
            cursor.execute('insert into %r values(%r, %r, %r, %r, %r, %r)' %(yyyy, date, ht, lt, w, wd, ws))
            cursor.close()
            conn.commit()
            conn.close()
        return

    # 主程序
    def save2Sqlite(self):
        for yy in range(2011, 2017): # 生成年份

            yyyy = str(yy)
            # 在tianqi.db中创建table
            self.createTable(yyyy)

            for m in range (1, 13): # 生成月份 
                if m < 10:
                    mm = '0'+str(m)
                else:
                    mm = str(m)

                #print u"开始解析%s年%s月份的数据。" %(yyyy, mm)

                url = u"http://lishi.tianqi.com/jinan/"+yyyy+mm+u".html"
                #print "开始解析的页面：", url

                # 获得页面解析后的数据列表
                data_list = self.getSoup(url)
                #print data_list

                # 将数据保存到yyyy表
                self.save2data(yyyy, data_list)

            print u"数据已保存到tianqi.db的%s表。" %yyyy


if __name__ == '__main__':
    
    weather_history = weather() #实例化
    weather_history.save2Sqlite()
