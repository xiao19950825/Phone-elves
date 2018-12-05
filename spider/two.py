import sqlite3
import pymysql
import requests
from lxml import etree
import json
import jsonpath
import time
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
}


def pinglun(pid,kw):
    # print(pid)
    page=0
    # cursor=db.cursor()
    try:
        while True:
            print('这是第%s页...'%page)
            url1 = 'https://sclub.jd.com/comment/productPageComments.action?productId={}&score=0&sortType=5&page={}&pageSize=10&isShadowSku=0&fold=1'.format(
                pid, page)
            r = requests.get(url=url1,headers=headers)
            jj=json.loads(r.text)
            # print(jj)
            content = jsonpath.jsonpath(jj,'$.comments[*]')
            # print(content)
            # ping=jsonpath.jsonpath(jj,'$.comments[*].content')
            # referenceName = jsonpath.jsonpath(jj,'$.comments[*].referenceName')

            for juti in content:
                ping = juti['content']
                referenceName = juti['referenceName']
                # print(ping)
                # print(pid)
                item = {
                    'pinglun':ping,
                    'pid':pid,
                    'referenceName':referenceName
                }
                save_to_mysql(db,item)
                # print(item)
                if ping == False:
                    # fp.write('%s手机评论结束------------------' % kw + '\n' + '\n')
                    # cursor.execute("Insert into phone(评论) values ('%s手机已经爬取结束------------------')"%kw)
                    # print('该手机评论结束-------------------------------------\n\n\n')
                    break
            # for juti in ping:
            #     item = {
            #         '评论':juti
            #     }

            page += 1

    except Exception as e:
        print(e)

def save_to_mysql(db, item):
	# 获取cursor
	cursor = db.cursor()
	# 拼接sql语句
	sql = "insert into phone_pinglun(pinglun, pid, referenceName) VALUES ('{}','{}','{}')".format(item['pinglun'],item['pid'],item['referenceName'])
	# 执行sql语句
	try:
		cursor.execute(sql)
		db.commit()
	except Exception as e:
		print(e)
		db.rollback()



with open("shouji.json",'rb') as shouji:
    # 将json文件中的信息加载过来
    result = json.load(shouji)
    fp = open('pinglun33.json','w',encoding='utf-8')
    db = pymysql.Connect(host='localhost', port=3306, user='root', password='123456', database='xiangmu', charset='utf8')
    try:
        for i in result:
            kw=i['phone_name']
            print('正在爬取----%s--'%kw)
            url = 'https://search.jd.com/Search?keyword={}&enc=utf-8'.format(kw)
            r = requests.get(url=url,headers=headers)
            tree = etree.HTML(r.text)
            pid_list = tree.xpath('//div[@id="J_goodsList"]/ul/li[1]/@data-sku')
            for pid in pid_list:
                pinglun(pid,kw)
            print('结束爬取---%s--'%kw)
    except Exception as e:
        print(e)
    # fp.close()
    db.close()








