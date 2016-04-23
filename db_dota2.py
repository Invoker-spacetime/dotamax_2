#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import re
import os
import json
from hero_rate import list_dict

#httpHandler = urllib2.HTTPHandler(debuglevel=1)
#httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
#opener = urllib2.build_opener(httpHandler, httpsHandler)

#urllib2.install_opener(opener)
request_headers = {'User-Agent':r'''Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0
		Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8''','Accept-Encoding': '''deflate'''
		}#要注意编码方式
#从dota2.db获取各英雄的URL

def  get_dota2_db_all_hero_url_list():  

	request = urllib2.Request(url = 'http://www.dota2.com.cn/heroes/index.htm',
					headers = request_headers)

	content = urllib2.urlopen(request).read() 

	re_url = re.compile('http://db.dota2.com.cn/hero/[a-zA-Z\_]+/')

	url_list = re.findall(re_url,content)#搜寻所有英雄的url

	return url_list
	
#1英文名称列表，2英雄所有名称列表
def  get_two_list(url_list):

	re_eng_name = re.compile(u'<title>[\u4e00-\u9fa5]+\s([a-zA-Z\s]+)\s')#匹配标题的英文名称
	re_ch_name = re.compile(u'<title>([\u4e00-\u9fa5]+)\s[a-zA-Z\s]+\s')#
	re_other_name_str = re.compile(u'''<p class="info_p">(.+)</p></li>''') #获取别名的字符串
	re_other_name_list = re.compile(u'[\u4e00-\u9fa5A-Za-z]+') #将字符串转换为list

	eng_list    = []
	all_name_list_list   = []

	for url_this_hero in url_list:
		print url_this_hero

		request = urllib2.Request(url = url_this_hero,
				headers = request_headers)
	
		
		#1.只需要读取5000个字符，全读会报IncompleteError
		#2.只读5000个字符有可能会出现，utf-8码无法转义的情况，通过排查，发现只有这两个URL    
		if ((url_this_hero == 'http://db.dota2.com.cn/hero/lich/')|(url_this_hero == 'http://db.dota2.com.cn/hero/slark/')):
			content = urllib2.urlopen(request).read(6000) 
			content = content.decode('utf-8')

		else:
			try:
				content = urllib2.urlopen(request).read(5000) 
				content = content.decode('utf-8')
				#print [content]
			except Exception, e:
				print 'error'
				eng_list.append(url_this_hero)
				continue    
	
	
		eng_name = re.findall(re_eng_name,content) #找到该英雄的英文名称
		#assert 0
		print eng_name
		ch_name = re.findall(re_ch_name,content) #中文名
		other_name_str = re.findall(re_other_name_str,content)#别名字符串
		print other_name_str
		
		other_name_list = re.findall(re_other_name_list,other_name_str[0])#解析别名字符串得到别名列表

		all_name_list = ch_name+ eng_name + other_name_list
	
		eng_list.append(eng_name[0])   
		all_name_list_list.append(all_name_list)

	#print eng_list
	#print all_name_list
	return eng_list,all_name_list_list

#将unicode编码的英文字母变成小写    
def unicode_lower(a): 
	b = a.encode('utf-8')
	return str.lower(b)

#将英雄的所有名称和他们的英雄名称建立Dict关系，用与鉴别用户的所有名称输入。
def creat_allname_relate():

	url_list = get_dota2_db_all_hero_url_list()

	eng_name_list,all_name_list = get_two_list(url_list)


	eng_allname_dict = list_dict(eng_name_list,all_name_list)#建立英文名称和所有名称的一一对应关系

	#print eng_allname_dict

	with open('database/hero_list.txt','rb') as f:
		text = f.read()
	hero_list = json.loads(text)#获取英雄名称列表

	sort_hero_list = sorted(hero_list,key = unicode_lower)#排序
	#print 'sort_hero_list',sort_hero_list
	sort_hero_eng_list = sorted(eng_name_list,key = unicode_lower)
	#print 'sort_hero_eng_list',sort_hero_eng_list
	eng_hero_dict = list_dict(sort_hero_eng_list,sort_hero_list)#建立英文名称和英雄名称的一一对应关系


	allname_hero_dict = dict()#英雄的所有名称 对应 英雄名称

	#print  eng_allname_dict[u'Abaddon']
	for eng_name in sort_hero_eng_list:
		for name in eng_allname_dict[eng_name]:
			allname_hero_dict[name]  =  eng_hero_dict[eng_name]
			print name,allname_hero_dict[name]
			

	with open('database/othername.txt','w') as f:
		f.write(json.dumps(allname_hero_dict))    


if __name__ == '__main__':
	creat_allname_relate()