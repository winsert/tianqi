#!/usr/bin/env python
# -*- coding: UTF-8 -*-
## 对soup.txt进行步步解析

import requests
from bs4 import BeautifulSoup
import os
 
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

sp = open('./soup.txt', 'r')

soup = BeautifulSoup(sp.read(), 'lxml')

all = soup.find('div', class_="tqtongji2").find_all('ul')

for ur in all:
    #print ur.get_text()
    day_list = ur.get_text().splitlines()
    print day_list


sp.close() # 关闭文件
