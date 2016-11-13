#!/usr/bin/python
# coding=UTF-8

import re
import requests
import urllib
from bs4 import BeautifulSoup
import sqlite3
import json


url = "http://opendata.baidu.com/api.php?resource_id=28226&from_mid=1&&format=json&ie=utf-8&oe=utf-8&query=%E6%98%8E%E6%98%9F&"
parm = "sort_key=&sort_type=1&stat0=&stat1=&stat2=&stat3=&pn=%d&rn=12&cb=jQuery110209454973743230939_1478484139757&_=%d"
baidu = requests.session()
baidu.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0'

try:
    conn = sqlite3.connect("star.db", check_same_thread = False)
    conn.execute("""
      CREATE TABLE IF NOT EXISTS star(
      NAME TEXT PRIMARY KEY,
      头像 BLOB,
      中文名 TEXT,
      别名 TEXT,
      国籍 TEXT,
      民族 TEXT,
      星座 TEXT,
      血型 TEXT,
      身高 TEXT,
      体重 TEXT,
      出生地 TEXT,
      出生日期 TEXT,
      职业 TEXT,
      毕业院校 TEXT,
      经纪公司 TEXT,
      代表作品 TEXT,
      主要成就 TEXT,
      生肖 TEXT,
      粉丝名 TEXT,
      官网 TEXT,
      配偶 TEXT,
      丈夫 TEXT,
      女儿 TEXT
      );""")
    conn.commit()
    cursor = conn.cursor()
except:
    print ("can't connect to table")

"""
#####first part :get NAME
count = 0
for i in range(1493,2000):
    _ = url+parm % (i*12, 1478484139757+i)
    try:
        s = requests.get(_).content
    except:
        print "##############################################################################################################3"
        print "_"
        exit(0)
    s = s[s.index('(')+1:-1]
    data = json.loads(s)
    try:
        for ii in data['data'][0]['result']:
            count+=1
            print ii['ename'],count
            sql = "insert into star(NAME )values(?)"
            cursor.execute(sql, (ii['ename'],))
        conn.commit()
    except:
        print "##############################################################################################################3"
        print sql
        print
print 'doooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooone'
"""
"""
#####second part :get DATA
columns = [ u'头像', u'中文名', u'别名',u'国籍',u'民族' , u'星座' , u'血型' , u'身高' ,
           u'体重' , u'出生地' , u'出生日期' , u'职业' , u'毕业院校' , u'经纪公司' , u'代表作品' ,
            u'主要成就' , u'生肖' , u'粉丝名' , u'官网' , u'配偶' , u'丈夫' , u'女儿' ,]
HAERD_SQL = "select NAME from star where 中文名 is NULL and 别名 is NULL and 国籍 is NULL and 民族 is NULL and 星座 is NULL and 血型 is NULL and 身高 is NULL and 体重 is NULL and 出生地 is NULL and 出生日期 is NULL and 职业 is NULL and 毕业院校 is NULL and 经纪公司 is NULL and 代表作品 is NULL and 主要成就 is NULL and 生肖 is NULL and 粉丝名 is NULL and 官网 is NULL and 配偶 is NULL and 丈夫 is NULL and 女儿 is NULL LIMIT 0, 10"
while True:
    stars = cursor.execute(HAERD_SQL).fetchall()
    if len(stars) <1:   break
    for i in stars:
        name = unicode(i[0]).encode('utf-8')
        try:
            result = baidu.get('http://baike.baidu.com/item/%s' % (name)).content.replace('&nbsp;', '')
            match1 = re.compile(r'<dt class="basicInfo-item name">(.+?)</dt>.<dd class="basicInfo-item value">(.+?)</dd>', re.S)
            #match2 = re.compile(r'<img src="([^<]+?)" />')
            #img = match2.findall(result)
            sn = ''
            sv = []
            for ii in match1.findall(result):
                (n, v) = (BeautifulSoup.BeautifulSoup(ii[0]).text, BeautifulSoup.BeautifulSoup(ii[1]).text)
                if n in columns:
                    sn+=n+' = ?,'
                    sv.append(v)
            if sn != '':
                _ = "update star set "+sn[:-1]+" where NAME='"+unicode(name,'utf-8')+"'"
            else:
                _ = "update star set "+u'中文名'+ " = '1' where NAME='"+unicode(name,'utf-8')+"'"
            cursor.execute(_, sv)
            #print _
            #print sv
            conn.commit()
        except Exception, e:
            print e, unicode(name, 'utf-8')
print "done",
"""
match1 = re.compile(r'http://[\w\./]+\.jpg')
while True:
    stars = cursor.execute(u"select NAME from star where 头像 is NULL limit 0, 50").fetchall()
    if len(stars) <1:   break
    for i in stars:
        name = unicode(i[0])
        #大图片
        #_ = 'http://cn.bing.com/images/search?q=%s&qft=+filterui:imagesize-large&FORM=R5IR2' % (name.encode('utf-8'))
        #中图片
        _ = 'http://cn.bing.com/images/search?q=%s&qft=+filterui:imagesize-medium&FORM=R5IR2' % (name.encode('utf-8'))
        try:
            _ = match1.findall(baidu.get(_).content)
        except Exception as e :
            print(e)
        for ii in range(5):
            try:
                filename = r"img\\%s%d.jpg" % (name, ii)
                with open(filename, 'wb')as f:
                    f.write(baidu.get(_[ii]).content)
            except Exception as e :
                 print (e)
        cursor.execute(u"update star set 头像 = '1'where NAME = '"+name+"'")
    conn.commit()
